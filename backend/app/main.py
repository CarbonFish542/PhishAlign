from __future__ import annotations

import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.inference import InferenceError, analyze_page
from app.page_capture import capture_url


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
    allow_origin_regex=r"chrome-extension://.*",
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ============================================================
# Request models
# ============================================================

class AnalyzeRequest(BaseModel):
    url: str = Field(..., min_length=1)


class AnalyzeContentRequest(BaseModel):
    """Layer 1: extension sends pre-captured page data — no Playwright needed."""
    url: str = Field(..., min_length=1)
    final_url: str = Field(..., min_length=1)
    html: str = Field(..., min_length=1)           # full outerHTML string
    screenshot_b64: str = Field(..., min_length=1) # raw base64, no data-URL prefix
    page_title: str = Field(default="")


# ============================================================
# Health check
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
    }


# ============================================================
# Website analysis — Layer 2/3: Playwright capture (fallback)
# ============================================================

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    url = request.url.strip()

    if not url:
        raise HTTPException(
            status_code=400,
            detail="URL is required.",
        )

    try:
        captured = capture_url(url)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

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

    return {
        "requested_url": result["requested_url"],
        "final_url": result["final_url"],
        "page_title": captured.title,
        "http_status": captured.status_code,
        "screenshot_data_url": (
            "data:image/png;base64,"
            + base64.b64encode(captured.screenshot).decode("ascii")
        ),
        "prediction": result["prediction"],
        "risk_tier": result["risk_tier"],
        "threshold": result["threshold"],
        "suspicious_threshold": result["suspicious_threshold"],
        "raw_phishalign_probability": result["raw_phishalign_probability"],
        "phishalign_probability": result["phishalign_probability"],
        "url_probability": result["url_probability"],
        "html_probability": result["html_probability"],
        "visual_probability": result["visual_probability"],
        "equal_weight_probability": result["equal_weight_probability"],
        "probability_only_probability": result["probability_only_probability"],
        "intent_signals": result["intent_signals"],
        "ocr_status": result["ocr_status"],
        "ocr_character_count": len(result["ocr_text"]),
        "ocr_error": result["ocr_error"],
        "consistency_features": result["consistency_features"],
        "modality_predictions": result["modality_predictions"],
    }


# ============================================================
# Website analysis — Layer 1: extension direct capture (primary)
# ============================================================

@app.post("/analyze_content")
def analyze_content(request: AnalyzeContentRequest):
    url = request.url.strip()
    final_url = request.final_url.strip()

    if not url:
        raise HTTPException(status_code=400, detail="URL is required.")

    try:
        screenshot_bytes = base64.b64decode(request.screenshot_b64)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid screenshot_b64: {exc}",
        ) from exc

    html_bytes = request.html.encode("utf-8", errors="replace")

    try:
        result = analyze_page(
            url=url,
            html_bytes=html_bytes,
            screenshot_bytes=screenshot_bytes,
            page_title=request.page_title,
            final_url=final_url,
        )
    except InferenceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal inference error.") from exc

    return {
        "requested_url": result["requested_url"],
        "final_url": result["final_url"],
        "page_title": request.page_title,
        "http_status": None,
        "screenshot_data_url": (
            "data:image/png;base64,"
            + base64.b64encode(screenshot_bytes).decode("ascii")
        ),
        "prediction": result["prediction"],
        "risk_tier": result["risk_tier"],
        "threshold": result["threshold"],
        "suspicious_threshold": result["suspicious_threshold"],
        "raw_phishalign_probability": result["raw_phishalign_probability"],
        "phishalign_probability": result["phishalign_probability"],
        "url_probability": result["url_probability"],
        "html_probability": result["html_probability"],
        "visual_probability": result["visual_probability"],
        "equal_weight_probability": result["equal_weight_probability"],
        "probability_only_probability": result["probability_only_probability"],
        "intent_signals": result["intent_signals"],
        "ocr_status": result["ocr_status"],
        "ocr_character_count": len(result["ocr_text"]),
        "ocr_error": result["ocr_error"],
        "consistency_features": result["consistency_features"],
        "modality_predictions": result["modality_predictions"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)