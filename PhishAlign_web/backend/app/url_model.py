import ipaddress
import json
import math
import re
from collections import Counter
from pathlib import Path

import joblib
import pandas as pd
from urllib.parse import urlsplit


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "url_xgboost_model.joblib"
FEATURE_NAMES_PATH = MODEL_DIR / "url_feature_names.json"


# ============================================================
# Load frozen model
# ============================================================

model = joblib.load(MODEL_PATH)

with open(FEATURE_NAMES_PATH, "r", encoding="utf-8") as f:
    FEATURE_NAMES = json.load(f)


# ============================================================
# Entropy — exact research implementation
# ============================================================

def entropy(text):
    if not text:
        return 0.0

    counts = Counter(text)
    length = len(text)

    return -sum(
        (count / length) * math.log2(count / length)
        for count in counts.values()
    )


# ============================================================
# URL feature extraction
# ============================================================

def extract_url_features(raw_url):
    """
    Exact runtime equivalent of the frozen
    url_baseline.py extractor.
    """

    url = str(raw_url).strip()

    # Add scheme only for parsing.
    parse_url = (
        url
        if "://" in url
        else "http://" + url
    )

    try:
        parsed = urlsplit(parse_url)

        host = parsed.hostname or ""
        path = parsed.path or ""
        query = parsed.query or ""
        fragment = parsed.fragment or ""

    except Exception:
        host = ""
        path = ""
        query = ""
        fragment = ""

    host_lower = host.lower()
    url_lower = url.lower()

    # IP address
    try:
        is_ip = int(
            bool(host)
            and ipaddress.ip_address(host).version in (4, 6)
        )
    except ValueError:
        is_ip = 0

    # Port
    try:
        port_present = int(
            parsed.port is not None
        )
    except (ValueError, AttributeError):
        port_present = 0

    # Subdomains
    subdomain_count = (
        max(0, len(host_lower.split(".")) - 2)
        if host_lower
        else 0
    )

    suspicious_tokens = [
        "login",
        "signin",
        "sign-in",
        "verify",
        "verification",
        "account",
        "secure",
        "security",
        "update",
        "password",
        "bank",
        "confirm",
        "billing",
        "wallet",
        "payment",
        "authenticate",
        "support",
        "recover",
        "webscr",
    ]

    features = {
        "url_length": len(url),
        "host_length": len(host),
        "path_length": len(path),
        "query_length": len(query),
        "fragment_length": len(fragment),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "slash_count": url.count("/"),
        "at_count": url.count("@"),
        "question_count": url.count("?"),
        "equal_count": url.count("="),
        "ampersand_count": url.count("&"),
        "percent_count": url.count("%"),
        "underscore_count": url.count("_"),
        "digit_count": sum(
            c.isdigit() for c in url
        ),
        "letter_count": sum(
            c.isalpha() for c in url
        ),
        "uppercase_count": sum(
            c.isupper() for c in url
        ),
        "special_char_count": sum(
            not c.isalnum() for c in url
        ),
        "subdomain_count": subdomain_count,
        "query_parameter_count": (
            query.count("=")
            if query
            else 0
        ),
        "path_depth": len(
            [
                part
                for part in path.split("/")
                if part
            ]
        ),
        "https": int(
            parsed.scheme.lower() == "https"
        ),
        "has_ip_address": is_ip,
        "has_port": port_present,
        "has_punycode": int(
            "xn--" in host_lower
        ),
        "has_double_slash_in_path": int(
            "//" in path
        ),
        "host_entropy": entropy(host_lower),
        "url_entropy": entropy(url_lower),
        "host_digit_count": sum(
            c.isdigit() for c in host_lower
        ),
        "path_digit_count": sum(
            c.isdigit() for c in path
        ),
        "suspicious_token_count": sum(
            token in url_lower
            for token in suspicious_tokens
        ),
    }

    return features


# ============================================================
# Model prediction
# ============================================================

def predict_url(url):
    """
    Return the frozen URL model's phishing probability.
    """

    features = extract_url_features(url)

    # Explicitly follow the frozen feature ordering.
    X = pd.DataFrame(
        [[features[name] for name in FEATURE_NAMES]],
        columns=FEATURE_NAMES,
    )

    probability = float(
        model.predict_proba(X)[0, 1]
    )

    return {
        "phishing_probability": probability,
        "features": features,
    }