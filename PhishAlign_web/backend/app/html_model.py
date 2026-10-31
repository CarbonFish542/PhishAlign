from pathlib import Path
import json
import re

import joblib
from bs4 import BeautifulSoup


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "html_xgboost_model.joblib"
FEATURE_NAMES_PATH = MODEL_DIR / "html_feature_names.json"


# ============================================================
# Load frozen model + feature names
# ============================================================

model = joblib.load(MODEL_PATH)

with open(FEATURE_NAMES_PATH, "r", encoding="utf-8") as f:
    FEATURE_NAMES = json.load(f)


# ============================================================
# Frozen research configuration
# ============================================================

MAX_HTML_BYTES = 2 * 1024 * 1024

TAGS = [
    "a", "area", "base", "button", "form", "input", "textarea",
    "select", "option", "iframe", "frame", "img", "script", "link",
    "meta", "style", "div", "span", "p", "h1", "h2", "h3",
    "table", "tr", "td", "th", "svg", "object", "embed",
]

SUSPICIOUS_TERMS = [
    "login", "signin", "sign in", "log in", "verify", "verification",
    "password", "account", "bank", "secure", "security", "update",
    "confirm", "billing", "payment", "wallet", "suspended",
    "unusual activity", "authentication", "recover",
]


# ============================================================
# Exact frozen extractor
# ============================================================

def _extract_from_raw(raw: bytes, original_size: int):
    """
    Extract the exact 64 HTML features used by the frozen
    research HTML baseline.

    `original_size` is kept separate from len(raw) so that
    html_truncated exactly matches the research implementation.
    """

    features = {}

    # --------------------------------------------------------
    # Decode exactly as research extractor
    # --------------------------------------------------------

    html = raw.decode("utf-8", errors="replace")

    # Built-in html.parser.
    # No browser, JavaScript, or network requests.
    soup = BeautifulSoup(html, "html.parser")

    # --------------------------------------------------------
    # Basic document and text characteristics
    # --------------------------------------------------------

    text = soup.get_text(" ", strip=True)
    text_lower = text.lower()

    features["html_bytes_read"] = len(raw)

    features["html_truncated"] = int(
        original_size > MAX_HTML_BYTES
    )

    features["text_length"] = len(text)

    features["word_count"] = len(text.split())

    features["unique_word_count"] = len(
        set(text_lower.split())
    )

    features["average_word_length"] = (
        sum(len(word) for word in text.split())
        / max(1, len(text.split()))
    )

    # --------------------------------------------------------
    # Tag counts
    # --------------------------------------------------------

    for tag in TAGS:
        features[f"tag_{tag}_count"] = len(
            soup.find_all(tag)
        )

    # --------------------------------------------------------
    # Forms and input characteristics
    # --------------------------------------------------------

    inputs = soup.find_all("input")

    input_types = [
        str(element.get("type", "")).lower()
        for element in inputs
    ]

    features["input_count"] = len(inputs)

    features["password_input_count"] = (
        input_types.count("password")
    )

    features["hidden_input_count"] = (
        input_types.count("hidden")
    )

    features["email_input_count"] = (
        input_types.count("email")
    )

    features["submit_input_count"] = (
        input_types.count("submit")
    )

    features["form_count"] = len(
        soup.find_all("form")
    )

    features["form_with_action_count"] = sum(
        bool(form.get("action"))
        for form in soup.find_all("form")
    )

    # --------------------------------------------------------
    # Link and resource characteristics
    # --------------------------------------------------------

    links = soup.find_all("a")

    hrefs = [
        str(a.get("href", ""))
        for a in links
    ]

    features["anchor_count"] = len(links)

    features["empty_href_count"] = sum(
        not href.strip()
        for href in hrefs
    )

    features["javascript_href_count"] = sum(
        href.strip().lower().startswith("javascript:")
        for href in hrefs
    )

    features["data_href_count"] = sum(
        href.strip().lower().startswith("data:")
        for href in hrefs
    )

    # --------------------------------------------------------
    # Images
    # --------------------------------------------------------

    features["image_count"] = len(
        soup.find_all("img")
    )

    features["image_missing_src_count"] = sum(
        not str(img.get("src", "")).strip()
        for img in soup.find_all("img")
    )

    # --------------------------------------------------------
    # Scripts
    # --------------------------------------------------------

    features["script_count"] = len(
        soup.find_all("script")
    )

    features["external_script_reference_count"] = sum(
        bool(script.get("src"))
        for script in soup.find_all("script")
    )

    features["inline_script_count"] = sum(
        not script.get("src")
        for script in soup.find_all("script")
    )

    # --------------------------------------------------------
    # Event/style attributes
    # --------------------------------------------------------

    all_tags = soup.find_all(True)

    event_attributes = [
        attr
        for tag in all_tags
        for attr in tag.attrs
        if str(attr).lower().startswith("on")
    ]

    features["event_handler_attribute_count"] = len(
        event_attributes
    )

    features["style_attribute_count"] = sum(
        "style" in tag.attrs
        for tag in all_tags
    )

    features["iframe_count"] = len(
        soup.find_all("iframe")
    )

    features["meta_refresh_count"] = sum(
        str(meta.get("http-equiv", "")).lower() == "refresh"
        for meta in soup.find_all("meta")
    )

    # --------------------------------------------------------
    # Text-based indicators
    # --------------------------------------------------------

    features["title_length"] = len(
        soup.title.get_text(" ", strip=True)
        if soup.title
        else ""
    )

    features["suspicious_term_count"] = sum(
        text_lower.count(term)
        for term in SUSPICIOUS_TERMS
    )

    features["https_text_count"] = text_lower.count(
        "https://"
    )

    features["http_text_count"] = text_lower.count(
        "http://"
    )

    # --------------------------------------------------------
    # HTML attribute patterns
    # --------------------------------------------------------

    features["external_style_reference_count"] = sum(
        bool(link.get("href"))
        for link in soup.find_all("link")
        if "stylesheet" in str(
            link.get("rel", "")
        ).lower()
    )

    features["target_blank_count"] = sum(
        str(a.get("target", "")).lower() == "_blank"
        for a in links
    )

    # --------------------------------------------------------
    # Character-level indicators
    # --------------------------------------------------------

    html_lower = html.lower()

    features["at_symbol_count"] = html.count("@")

    features["encoded_entity_count"] = len(
        re.findall(
            r"&#(?:x[0-9a-f]+|\d+);",
            html_lower
        )
    )

    features["base64_marker_count"] = html_lower.count(
        "base64"
    )

    # --------------------------------------------------------
    # Verify feature set
    # --------------------------------------------------------

    missing = [
        name
        for name in FEATURE_NAMES
        if name not in features
    ]

    if missing:
        raise RuntimeError(
            f"Missing HTML features: {missing}"
        )

    if len(features) != 64:
        raise RuntimeError(
            f"Expected 64 extracted features, got {len(features)}"
        )

    # Return strictly in frozen model order.
    return [
        features[name]
        for name in FEATURE_NAMES
    ]


# ============================================================
# File-based extraction
# ============================================================

def extract_html_features_from_path(html_path):
    """
    Exact research-compatible extraction from an HTML file.

    This preserves the original file size so html_truncated
    exactly matches the frozen research implementation.
    """

    path = Path(str(html_path))

    if not path.is_file():
        return None

    original_size = path.stat().st_size

    with path.open("rb") as file:
        raw = file.read(MAX_HTML_BYTES)

    return _extract_from_raw(
        raw,
        original_size
    )


# ============================================================
# Bytes-based extraction for live web pages
# ============================================================

def extract_html_features(html_bytes):
    """
    Extract features from raw HTML bytes.

    For live pages, the supplied bytes represent the fetched
    document, so len(html_bytes) is used as the original size.
    """

    if html_bytes is None:
        html_bytes = b""

    original_size = len(html_bytes)

    raw = html_bytes[:MAX_HTML_BYTES]

    return _extract_from_raw(
        raw,
        original_size
    )


# ============================================================
# Prediction
# ============================================================

def predict_html(html_bytes):
    """
    Return phishing probability for raw HTML bytes.
    """

    features = extract_html_features(html_bytes)

    probability = float(
        model.predict_proba([features])[0][1]
    )

    return probability


def predict_html_from_path(html_path):
    """
    Research-compatible prediction directly from an HTML file.
    """

    features = extract_html_features_from_path(html_path)

    if features is None:
        raise FileNotFoundError(
            f"HTML file not found: {html_path}"
        )

    probability = float(
        model.predict_proba([features])[0][1]
    )

    return probability