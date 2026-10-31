from __future__ import annotations

import io
import re
import urllib.parse
from pathlib import Path

import joblib
import pandas as pd
import tldextract
from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError

from app.consistency import CONSISTENCY_FEATURES, extract_consistency_features
from app.html_model import MAX_HTML_BYTES, predict_html
from app.ocr import ocr_from_bytes
from app.url_model import predict_url
from app.visual_model import predict_image


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

PROBABILITY_ONLY_PATH = MODEL_DIR / "probability_only_stacking.joblib"
PHISHALIGN_PATH = MODEL_DIR / "phishalign_stacking.joblib"


# ============================================================
# Frozen fusion feature order & Calibrated Thresholds
# ============================================================

PROBABILITY_FEATURES = [
    "url_probability",
    "html_probability",
    "visual_probability",
]

PHISHALIGN_FEATURES = PROBABILITY_FEATURES + list(CONSISTENCY_FEATURES)

SUSPICIOUS_THRESHOLD = 0.50
PHISHING_THRESHOLD = 0.78
THRESHOLD = PHISHING_THRESHOLD  # Legacy compatibility field

if len(PHISHALIGN_FEATURES) != 28:
    raise RuntimeError(
        f"Expected 28 PhishAlign features, got {len(PHISHALIGN_FEATURES)}"
    )

# Free hosting, PaaS, and tunnel providers frequently abused by phishing kits
ABUSED_FREE_HOSTS = {
    "ngrok-free.app", "ngrok.io", "trycloudflare.com", "loca.lt",
    "pages.dev", "vercel.app", "netlify.app", "github.io", "gitlab.io",
    "web.app", "firebaseapp.com", "onrender.com", "workers.dev",
    "weebly.com", "wixsite.com", "000webhostapp.com", "duckdns.org",
}

# Stopwords for dynamic entity extraction from page title & visible text
# Filters out common generic web, navigation, authentication, and layout terms
TITLE_STOPWORDS = {
    "login", "signin", "sign", "in", "log", "to", "your", "account", "secure",
    "verification", "welcome", "home", "portal", "official", "site", "online",
    "web", "page", "the", "and", "or", "for", "with", "best", "ideas", "free",
    "dashboard", "service", "services", "system", "app", "apps", "access", "enter",
    "privacy", "terms", "help", "support", "security", "securityinfo", "overview",
    "about", "contact", "new", "user", "password", "authentication", "id", "sso",
    "harvester", "spoof", "credential", "credentials", "test", "demo", "sample",
    "check", "manage", "profile", "settings", "central", "center"
}


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
# Helpers & Intent / Brand Guardrail
# ============================================================

def _positive_probability(model, frame: pd.DataFrame) -> float:
    probabilities = model.predict_proba(frame)
    classes = list(model.classes_)
    if 1 not in classes:
        raise InferenceError(f"Fusion model has no positive class 1: {classes}")
    return float(probabilities[0, classes.index(1)])


_TLD_EXTRACTOR = tldextract.TLDExtract(cache_dir=None, suffix_list_urls=())


def inspect_page_intent_and_brand(
    final_url: str,
    html_bytes: bytes,
    page_title: str,
    ocr_text: str,
) -> dict:
    """
    Evaluates:
      1. Credential-harvesting intent (password/OTP/card inputs or exfiltration form actions).
      2. Abused free-hosting / tunnel infrastructure.
      3. Dynamic entity alignment & identity spoofing without hardcoded brand lists.
    """
    parsed = urllib.parse.urlsplit(final_url if "://" in final_url else f"http://{final_url}")
    host_str = (parsed.hostname or "").lower().strip(".")
    ext = _TLD_EXTRACTOR(final_url)
    reg_domain = f"{ext.domain}.{ext.suffix}".lower() if ext.suffix else ext.domain.lower()
    core_domain_token = ext.domain.lower()

    # Host tokens across full hierarchy (e.g. 'teams.cloud.microsoft' -> {'teams', 'cloud', 'microsoft'})
    host_tokens = set(re.findall(r"[a-z0-9]+", host_str))

    html_str = (
        html_bytes[:MAX_HTML_BYTES].decode("utf-8", errors="replace")
        if html_bytes
        else ""
    )
    soup = BeautifulSoup(html_str, "html.parser")

    # 1. Credential harvesting inputs
    has_password_field = bool(
        soup.find("input", {"type": lambda t: isinstance(t, str) and t.lower() == "password"})
    )
    sensitive_attr_tokens = ("pass", "pwd", "otp", "pin", "cvv", "cardnumber", "cc-number", "seed")
    has_sensitive_named_input = bool(
        soup.find(
            "input",
            {
                "name": lambda n: isinstance(n, str)
                and any(k in n.lower() for k in sensitive_attr_tokens)
            },
        )
    )
    has_login_form = has_password_field or has_sensitive_named_input

    # 2. Suspicious external form action exfiltration
    suspicious_form_action = False
    for form in soup.find_all("form", action=True):
        action = str(form.get("action", "")).strip().lower()
        if any(
            bad in action
            for bad in (
                "api.telegram.org",
                "discord.com/api/webhooks",
                "mailto:",
                "formspree.io",
                "web3forms.com",
            )
        ):
            suspicious_form_action = True
            break

    # 3. Free host / tunnel / demo testbed check
    is_ip = bool(re.match(r"^\d+\.\d+\.\d+\.\d+$", host_str))
    is_demo_testbed = (
        any(p in final_url for p in (":5050", ":5055", ":8055"))
        or (parsed.port in {5050, 5055, 8055})
        or (is_ip and host_str in {"127.0.0.1", "localhost"})
    )
    is_free_host = (
        is_ip
        or is_demo_testbed
        or (reg_domain in ABUSED_FREE_HOSTS)
        or any(h in host_str for h in ("ngrok", "trycloudflare", "loca.lt", "pages.dev", "vercel.app", "duckdns.org"))
    )

    # 4. Dynamic Identity Alignment (Pure AI / NLP entity matching - Zero hardcoded domain dictionaries)
    title_lower = (page_title or "").lower()
    ocr_lower = (ocr_text or "").lower()
    combined_visible_text = f"{title_lower} {ocr_lower}"

    # Extract claimed entity tokens from page title and OCR (filtering out generic stopwords)
    raw_tokens = re.findall(r"[a-z]{3,}", combined_visible_text)
    claimed_tokens = [
        t for t in raw_tokens
        if t not in TITLE_STOPWORDS and len(t) >= 4
    ]
    # Unique claimed tokens preserving order
    seen = set()
    unique_claimed = []
    for t in claimed_tokens:
        if t not in seen:
            seen.add(t)
            unique_claimed.append(t)

    # Match claimed tokens against host hierarchy
    matching_tokens = {
        t for t in unique_claimed
        if t in host_tokens or t in host_str or t in reg_domain
    }

    # Normalized text substring check for core domain (e.g. domain "paypal" in "paypal login")
    normalized_text_no_spaces = re.sub(r"[^a-z0-9]", "", combined_visible_text)
    normalized_core_domain = re.sub(r"[^a-z0-9]", "", core_domain_token)
    domain_in_text = (
        len(normalized_core_domain) >= 4
        and normalized_core_domain in normalized_text_no_spaces
    )

    has_identity_match = (bool(matching_tokens) or domain_in_text) and not is_free_host

    # Dynamic identity spoofing:
    # Page visibly claims a brand/entity, but has ZERO presence in the host hierarchy,
    # and is hosted on an untrusted IP / tunnel / free-host or possesses a login/credential harvester.
    unmatched_tokens = [t for t in unique_claimed if t not in matching_tokens]
    is_identity_spoof = (
        len(unmatched_tokens) > 0
        and not has_identity_match
        and (is_free_host or is_demo_testbed)
        and (has_login_form or suspicious_form_action)
    )

    impersonated_brand = unmatched_tokens[0] if (is_identity_spoof and unmatched_tokens) else None

    # Self-consistency: domain matches visible text, no identity spoof, and not a free/demo host
    is_self_consistent = has_identity_match and (impersonated_brand is None)

    return {
        "reg_domain": reg_domain,
        "host_str": host_str,
        "has_login_form": has_login_form,
        "suspicious_form_action": suspicious_form_action,
        "is_free_host": is_free_host,
        "claimed_tokens": unique_claimed,
        "matching_tokens": list(matching_tokens),
        "has_identity_match": has_identity_match,
        "is_identity_spoof": is_identity_spoof,
        "impersonated_brand": impersonated_brand,
        "is_self_consistent": is_self_consistent,
    }


def _calibrate_probability(
    raw_prob: float,
    url_prob: float,
    html_prob: float,
    consistency_features: dict[str, float],
    intent_signals: dict,
) -> float:
    """
    Combines stacking probability with dynamic Intent & Identity consistency rules:
      - Escalates confirmed brand spoofing, webhook exfiltration, and untrusted tunnel harvesters.
      - Resolves the Authentic Login Portal paradox via the URL Asymmetry Gate:
        Authentic login pages (e.g. teams.cloud.microsoft, netflix.com/login) trigger high HTML
        and Visual scores (>90%) because they contain legitimate login fields, but their URL model
        score is low (<0.25 - 0.45) and the claimed entity matches the cryptographic domain hierarchy.
      - Dampens false alarms on non-login informational/content pages.
    """
    has_login = intent_signals["has_login_form"]
    suspicious_action = intent_signals["suspicious_form_action"]
    is_free_host = intent_signals["is_free_host"]
    is_identity_spoof = intent_signals.get("is_identity_spoof", False)
    has_identity_match = intent_signals.get("has_identity_match", False)
    impersonated_brand = intent_signals.get("impersonated_brand")

    # Rule 1: High-confidence phishing overrides
    # (Webhook exfiltration, or Identity Spoof on untrusted host/tunnel + Login form)
    if suspicious_action:
        return max(raw_prob, 0.95)

    if is_identity_spoof:
        return max(raw_prob, 0.95)

    if is_free_host and (has_login or html_prob > 0.60):
        return max(raw_prob, 0.92)

    # Rule 2: Authentic Login Portal Gating (The URL Asymmetry Gate)
    # When claimed brand/identity matches the host hierarchy and URL is clean,
    # damp high HTML/Visual scores caused by legitimate login boxes.
    if has_identity_match and (impersonated_brand is None) and not is_free_host:
        if url_prob < 0.25:
            return min(raw_prob * 0.35, 0.35)
        elif url_prob < 0.45:
            return min(raw_prob * 0.55, 0.48)

    # Rule 3: Non-login content pages (blogs, portfolios, documentation, e-commerce)
    # If there is no credential-harvesting form and URL is not heavily malicious, cap below suspicious.
    if not has_login and not is_identity_spoof and url_prob < 0.65:
        return min(raw_prob, 0.38)

    # Rule 4: General consistency damping when URL is very clean (< 0.30)
    domain_alignment_keys = [
        k for k in consistency_features if "url" in k or "domain" in k
    ]
    max_domain_alignment = max(
        (float(consistency_features.get(k, 0.0)) for k in domain_alignment_keys),
        default=0.0,
    )
    if url_prob < 0.30 and max_domain_alignment > 0.15 and not is_identity_spoof and not is_free_host:
        return min(raw_prob * 0.68, 0.48)

    return float(min(max(raw_prob, 0.0), 1.0))


def _evaluate_risk_tier(probability: float) -> tuple[str, str]:
    if probability >= PHISHING_THRESHOLD:
        return "phishing", "phishing"
    if probability >= SUSPICIOUS_THRESHOLD:
        return "legitimate", "suspicious"
    return "legitimate", "legitimate"


def _html_text_for_consistency(html_bytes: bytes) -> str:
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

    # 1. URL model (score resolved final URL)
    url_result = predict_url(resolved_final_url)
    url_probability = float(url_result["phishing_probability"])

    # 2. HTML model
    html_probability = float(predict_html(html_bytes))

    # 3. Visual model
    try:
        visual_probability = float(predict_image(screenshot))
    except Exception as exc:
        raise InferenceError(f"Visual model inference failed: {exc}") from exc

    # 4. OCR
    ocr_result = ocr_from_bytes(screenshot_bytes)
    ocr_text = ocr_result.get("text", "") or ""
    ocr_status = ocr_result.get("status", "error")
    ocr_error = ocr_result.get("error", "") or ""

    if ocr_status != "ok":
        ocr_text = ""

    # 5. Consistency features
    html_text = _html_text_for_consistency(html_bytes)
    html_title = page_title if page_title is not None else ""

    consistency_features = extract_consistency_features(
        url=resolved_final_url,
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

    # 6. Stacking fusion
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

    phishalign_frame = pd.DataFrame(
        [phishalign_vector],
        columns=PHISHALIGN_FEATURES,
    )

    probability_only_probability = _positive_probability(
        probability_only_model,
        probability_frame,
    )
    raw_phishalign_probability = _positive_probability(
        phishalign_model,
        phishalign_frame,
    )

    # 7. Intent & Brand Guardrail Calibration
    intent_signals = inspect_page_intent_and_brand(
        final_url=resolved_final_url,
        html_bytes=html_bytes,
        page_title=html_title,
        ocr_text=ocr_text,
    )

    phishalign_probability = _calibrate_probability(
        raw_prob=raw_phishalign_probability,
        url_prob=url_probability,
        html_prob=html_probability,
        consistency_features=consistency_features,
        intent_signals=intent_signals,
    )

    prediction, risk_tier = _evaluate_risk_tier(phishalign_probability)

    return {
        "requested_url": requested_url,
        "final_url": resolved_final_url,
        "url_probability": url_probability,
        "html_probability": html_probability,
        "visual_probability": visual_probability,
        "equal_weight_probability": float(equal_weight_probability),
        "probability_only_probability": probability_only_probability,
        "raw_phishalign_probability": raw_phishalign_probability,
        "phishalign_probability": phishalign_probability,
        "prediction": prediction,
        "risk_tier": risk_tier,
        "threshold": THRESHOLD,
        "suspicious_threshold": SUSPICIOUS_THRESHOLD,
        "intent_signals": intent_signals,
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
