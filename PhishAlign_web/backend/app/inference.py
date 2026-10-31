from __future__ import annotations

import io
from pathlib import Path

import joblib
import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError

from app.consistency import CONSISTENCY_FEATURES, extract_consistency_features
from app.html_model import MAX_HTML_BYTES, predict_html
from app.ocr import ocr_from_bytes
from app.url_model import predict_url
from app.visual_model import predict_image


# ============================================================
# Paths — relative to this file, never D:\Phish360
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

PROBABILITY_ONLY_PATH = MODEL_DIR / "probability_only_stacking.joblib"
PHISHALIGN_PATH = MODEL_DIR / "phishalign_stacking.joblib"


# ============================================================
# Frozen fusion feature order
# ============================================================

PROBABILITY_FEATURES = [
    "url_probability",
    "html_probability",
    "visual_probability",
]

PHISHALIGN_FEATURES = PROBABILITY_FEATURES + list(CONSISTENCY_FEATURES)

THRESHOLD = 0.5

if len(PHISHALIGN_FEATURES) != 28:
    raise RuntimeError(
        f"Expected 28 PhishAlign features, got {len(PHISHALIGN_FEATURES)}"
    )


# ============================================================
# Frozen stacking models
# ============================================================

probability_only_model = joblib.load(PROBABILITY_ONLY_PATH)
phishalign_model = joblib.load(PHISHALIGN_PATH)

if getattr(probability_only_model, "n_features_in_", None) != 3:
    raise RuntimeError(
        "probability_only_stacking.joblib does not expect 3 features"
    )

if getattr(phishalign_model, "n_features_in_", None) != 28:
    raise RuntimeError(
        "phishalign_stacking.joblib does not expect 28 features"
    )


class InferenceError(Exception):
    """Raised when a required live-inference modality cannot be scored."""


# ============================================================
# Helpers
# ============================================================

def _positive_probability(model, frame: pd.DataFrame) -> float:
    probabilities = model.predict_proba(frame)
    classes = list(model.classes_)
    if 1 not in classes:
        raise InferenceError(f"Fusion model has no positive class 1: {classes}")
    return float(probabilities[0, classes.index(1)])


def _label_from_probability(probability: float) -> str:
    return "phishing" if probability >= THRESHOLD else "legitimate"


def _html_text_for_consistency(html_bytes: bytes) -> str:
    """
    Visible/static HTML text in the same decode + get_text
    convention used by app.html_model._extract_from_raw.
    consistency.py expects html_text, not raw markup.
    """
    if not html_bytes:
        return ""

    raw = html_bytes[:MAX_HTML_BYTES]
    html = raw.decode("utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ", strip=True)


def _load_screenshot(screenshot_bytes: bytes) -> Image.Image:
    if screenshot_bytes is None or len(screenshot_bytes) == 0:
        raise InferenceError("Screenshot bytes are missing; visual analysis cannot run.")

    try:
        with Image.open(io.BytesIO(screenshot_bytes)) as image:
            return image.convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise InferenceError(
            f"Screenshot could not be decoded for visual analysis: {exc}"
        ) from exc


# ============================================================
# Public orchestrator
# ============================================================

def analyze_page(
    url: str,
    html_bytes: bytes,
    screenshot_bytes: bytes,
    page_title: str = "",
    final_url: str | None = None,
) -> dict:
    """
    Run live PhishAlign inference on already-captured page data.

    This function does not fetch URLs. The caller (eventually FastAPI)
    must obtain HTML and screenshot bytes via page_capture.py.
    """

    requested_url = (url or "").strip()
    if not requested_url:
        raise InferenceError("A URL is required for live inference.")

    resolved_final_url = (final_url or requested_url).strip() or requested_url

    if html_bytes is None:
        html_bytes = b""
    elif not isinstance(html_bytes, (bytes, bytearray)):
        raise InferenceError("html_bytes must be raw bytes.")
    else:
        html_bytes = bytes(html_bytes)

    screenshot = _load_screenshot(screenshot_bytes)

    # --------------------------------------------------------
    # URL model
    # --------------------------------------------------------

    url_result = predict_url(requested_url)
    url_probability = float(url_result["phishing_probability"])

    # --------------------------------------------------------
    # HTML model — empty bytes are scored by the frozen module
    # --------------------------------------------------------

    html_probability = float(predict_html(html_bytes))

    # --------------------------------------------------------
    # Visual model
    # --------------------------------------------------------

    try:
        visual_probability = float(predict_image(screenshot))
    except Exception as exc:
        raise InferenceError(
            f"Visual model inference failed: {exc}"
        ) from exc

    # --------------------------------------------------------
    # OCR — failure yields empty text, never invented text
    # --------------------------------------------------------

    ocr_result = ocr_from_bytes(screenshot_bytes)
    ocr_text = ocr_result.get("text", "") or ""
    ocr_status = ocr_result.get("status", "error")
    ocr_error = ocr_result.get("error", "") or ""

    if ocr_status != "ok":
        ocr_text = ""

    # --------------------------------------------------------
    # Consistency features (frozen extractor)
    # --------------------------------------------------------

    html_text = _html_text_for_consistency(html_bytes)
    html_title = page_title if page_title is not None else ""

    consistency_features = extract_consistency_features(
        url=requested_url,
        html_text=html_text,
        html_title=html_title,
        ocr_text=ocr_text,
    )

    consistency_values = [
        consistency_features[name] for name in CONSISTENCY_FEATURES
    ]

    if len(consistency_values) != 25:
        raise InferenceError(
            f"Expected 25 consistency features, got {len(consistency_values)}"
        )

    # --------------------------------------------------------
    # Fusion vectors
    # --------------------------------------------------------

    equal_weight_probability = (
        url_probability + html_probability + visual_probability
    ) / 3.0

    probability_frame = pd.DataFrame(
        [[url_probability, html_probability, visual_probability]],
        columns=PROBABILITY_FEATURES,
    )

    phishalign_vector = [
        url_probability,
        html_probability,
        visual_probability,
        *consistency_values,
    ]

    if len(phishalign_vector) != 28:
        raise InferenceError(
            f"Expected 28 PhishAlign features, got {len(phishalign_vector)}"
        )

    phishalign_frame = pd.DataFrame(
        [phishalign_vector],
        columns=PHISHALIGN_FEATURES,
    )

    probability_only_probability = _positive_probability(
        probability_only_model,
        probability_frame,
    )
    phishalign_probability = _positive_probability(
        phishalign_model,
        phishalign_frame,
    )

    prediction = _label_from_probability(phishalign_probability)

    return {
        "requested_url": requested_url,
        "final_url": resolved_final_url,
        "url_probability": url_probability,
        "html_probability": html_probability,
        "visual_probability": visual_probability,
        "equal_weight_probability": float(equal_weight_probability),
        "probability_only_probability": probability_only_probability,
        "phishalign_probability": phishalign_probability,
        "prediction": prediction,
        "threshold": THRESHOLD,
        "ocr_text": ocr_text,
        "ocr_status": ocr_status,
        "ocr_error": ocr_error,
        "html_text": html_text,
        "html_title": html_title,
        "consistency_features": consistency_features,
        **consistency_features,
        "phishalign_feature_vector": phishalign_vector,
        "modality_predictions": {
            "url": url_result,
            "html": {"phishing_probability": html_probability},
            "visual": {"phishing_probability": visual_probability},
        },
    }
