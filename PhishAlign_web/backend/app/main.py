from __future__ import annotations
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from app.inference import InferenceError, analyze_page
from app.page_capture import capture_url

import pandas as pd
try:
    import shap
except ImportError:
    shap = None

from app.url_model import FEATURE_NAMES, extract_url_features, model as url_model


# ============================================================
# FastAPI application
# ============================================================

app = FastAPI(
    title="PhishAlign API",
    description="Live multimodal phishing website detection API",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ============================================================
# Request model
# ============================================================

class AnalyzeRequest(BaseModel):
    url: str = Field(..., min_length=1)


# ============================================================
# Health check
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
    }


def extract_html_display_metrics(raw_html: bytes, page_url: str) -> dict:
    """Extract descriptive HTML statistics for the analysis UI."""

    html = bytes(raw_html or b"")[: 2 * 1024 * 1024].decode(
        "utf-8", errors="replace"
    )
    soup = BeautifulSoup(html, "html.parser")
    page = urlparse(page_url)

    def is_external(target: str) -> bool:
        if not target or not target.strip():
            return False

        resolved = urlparse(urljoin(page_url, target.strip()))

        return (
            resolved.scheme in ("http", "https")
            and resolved.hostname is not None
            and resolved.hostname.lower() != (page.hostname or "").lower()
        )

    forms = soup.find_all("form")
    links = soup.find_all("a")
    inputs = soup.find_all("input")
    scripts = soup.find_all("script")
    all_tags = soup.find_all(True)

    password_fields = sum(
        str(element.get("type", "")).lower() == "password"
        for element in inputs
    )

    event_handler_count = sum(
        str(attribute).lower().startswith("on")
        for element in all_tags
        for attribute in element.attrs
    )

    javascript_links = sum(
        str(link.get("href", "")).strip().lower().startswith("javascript:")
        for link in links
    )

    external_form_submission = any(
        is_external(str(form.get("action", "")))
        for form in forms
    )

    return {
        "form_count": len(forms),
        "password_fields": password_fields,
        "external_links": sum(
            is_external(str(link.get("href", ""))) for link in links
        ),
        "iframe_count": len(soup.find_all("iframe")),
        "script_count": len(scripts),
        "event_handler_attribute_count": event_handler_count,
        "javascript_link_count": javascript_links,
        "suspicious_javascript_heuristic": (
            event_handler_count > 0 or javascript_links > 0
        ),
        "external_form_submission": external_form_submission,
    }

# ============================================================
# Website analysis
# ============================================================

def explain_url_features(url: str) -> dict:
    """Return optional SHAP feature contributions without changing prediction."""
    try:
        features = extract_url_features(url)
        X = pd.DataFrame(
            [[features[name] for name in FEATURE_NAMES]],
            columns=FEATURE_NAMES,
        )

        explainer = shap.TreeExplainer(url_model)
        shap_values = explainer.shap_values(X)
        values = shap_values[0]

        ranked = sorted(
            zip(FEATURE_NAMES, values),
            key=lambda item: abs(float(item[1])),
            reverse=True,
        )

        return {
            "available": True,
            "method": "SHAP TreeExplainer",
            "output_space": "raw model score (log-odds)",
            "base_value": float(explainer.expected_value),
            "top_features": [
                {
                    "feature": name,
                    "value": float(features[name]),
                    "contribution": float(contribution),
                    "direction": (
                        "increases_phishing_score"
                        if float(contribution) > 0
                        else "decreases_phishing_score"
                        if float(contribution) < 0
                        else "no_effect"
                    ),
                }
                for name, contribution in ranked[:10]
            ],
        }
    except Exception:
        # Explanations are optional; never fail a prediction because of SHAP.
        return {
            "available": False,
            "method": "SHAP TreeExplainer",
            "top_features": [],
        }

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    url = request.url.strip()

    if not url:
        raise HTTPException(
            status_code=400,
            detail="URL is required.",
        )

    # --------------------------------------------------------
    # Live page capture
    # --------------------------------------------------------

    
    try:
        captured = capture_url(url)

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # Detect a likely security challenge before model inference.
    captured_title = (captured.title or "").strip().lower()
    captured_url = (captured.final_url or "").lower()

    is_security_challenge = (
        captured.status_code in (403, 429, 503)
        and (
            "just a moment" in captured_title
            or "challenge" in captured_url
            or "__cf_chl" in captured_url
        )
    )

    if is_security_challenge:
        raise HTTPException(
            status_code=422,
            detail=(
                "Unable to analyze this page reliably: a security "
                "challenge or automated-access block was detected. "
                "This is not a phishing verdict. Try again later "
                "or inspect the website in a normal browser."
            ),
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # --------------------------------------------------------
    # PhishAlign inference
    # --------------------------------------------------------

    try:
        result = analyze_page(
            url=captured.requested_url,
            html_bytes=captured.html,
            screenshot_bytes=captured.screenshot,
            page_title=captured.title,
            final_url=captured.final_url,
        )

    except InferenceError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal inference error.",
        ) from exc

    # --------------------------------------------------------
    # API response
    # --------------------------------------------------------

    return {
        "requested_url": result["requested_url"],
        "html_metrics": extract_html_display_metrics(
    captured.html,
    captured.final_url or captured.requested_url,
),
        "final_url": result["final_url"],

        "page_title": captured.title,
        "http_status": captured.status_code,
                "screenshot_data_url": (
            "data:image/png;base64,"
            + base64.b64encode(captured.screenshot).decode("ascii")
        ),

        "prediction": result["prediction"],
        "threshold": result["threshold"],

        "phishalign_probability": result["phishalign_probability"],

        "url_probability": result["url_probability"],

        "url_explanation": explain_url_features(
            result["requested_url"]
        ),

        "html_probability": result["html_probability"],
        "visual_probability": result["visual_probability"],

        "equal_weight_probability": result["equal_weight_probability"],
        "probability_only_probability": result[
            "probability_only_probability"
        ],

        "ocr_status": result["ocr_status"],
        "ocr_character_count": len(result["ocr_text"]),
        "ocr_error": result["ocr_error"],

        "consistency_features": result["consistency_features"],

        "modality_predictions": result["modality_predictions"],
    }