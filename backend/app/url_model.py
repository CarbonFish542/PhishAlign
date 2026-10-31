from __future__ import annotations

import ipaddress
import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

import joblib
import pandas as pd
import tldextract

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

_TLD_EXTRACTOR = tldextract.TLDExtract(cache_dir=None, suffix_list_urls=())


# ============================================================
# Entropy — exact research implementation
# ============================================================

def entropy(text: str) -> float:
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

def extract_url_features(raw_url: str) -> dict:
    url = str(raw_url).strip()
    parse_url = url if "://" in url else "http://" + url

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

    # IP address check
    try:
        is_ip = int(
            bool(host) and ipaddress.ip_address(host).version in (4, 6)
        )
    except ValueError:
        is_ip = 0

    # Port check
    try:
        port_present = int(parsed.port is not None)
    except (ValueError, AttributeError):
        port_present = 0

    # Accurate subdomain extraction using Public Suffix List (fixes .co.in / .ac.in)
    ext = _TLD_EXTRACTOR(parse_url)
    if ext.subdomain:
        sub_parts = [
            p for p in ext.subdomain.lower().split(".")
            if p and p != "www"
        ]
        subdomain_count = len(sub_parts)
    else:
        subdomain_count = 0

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

    # Count all hyphens in hostname, but cap path hyphen contribution to 1
    # so legitimate blog/article URL slugs do not trigger domain-hyphen penalties.
    host_hyphens = host_lower.count("-")
    path_hyphens = min(1, path.count("-"))
    effective_hyphen_count = host_hyphens + path_hyphens

    def _has_token(text: str, tok: str) -> bool:
        pat = r"(?<![a-z0-9])" + re.escape(tok) + r"(?![a-z0-9])"
        return bool(re.search(pat, text))

    # Count suspicious tokens in hostname always; only count path tokens if hostname looks suspect
    host_token_hits = sum(_has_token(host_lower, token) for token in suspicious_tokens)
    path_token_hits = sum(_has_token(path.lower(), token) for token in suspicious_tokens)
    effective_token_count = host_token_hits + (
        path_token_hits if (host_hyphens > 0 or subdomain_count > 1 or is_ip) else 0
    )

    features = {
        "url_length": len(url),
        "host_length": len(host),
        "path_length": len(path),
        "query_length": len(query),
        "fragment_length": len(fragment),
        "dot_count": host_lower.count(".") + path.count("."),
        "hyphen_count": effective_hyphen_count,
        "slash_count": url.count("/"),
        "at_count": url.count("@"),
        "question_count": url.count("?"),
        "equal_count": url.count("="),
        "ampersand_count": url.count("&"),
        "percent_count": url.count("%"),
        "underscore_count": url.count("_"),
        "digit_count": sum(c.isdigit() for c in url),
        "letter_count": sum(c.isalpha() for c in url),
        "uppercase_count": sum(c.isupper() for c in url),
        "special_char_count": sum(not c.isalnum() for c in url),
        "subdomain_count": subdomain_count,
        "query_parameter_count": query.count("=") if query else 0,
        "path_depth": len([part for part in path.split("/") if part]),
        "https": int(parsed.scheme.lower() == "https"),
        "has_ip_address": is_ip,
        "has_port": port_present,
        "has_punycode": int("xn--" in host_lower),
        "has_double_slash_in_path": int("//" in path),
        "host_entropy": entropy(host_lower),
        "url_entropy": entropy(url_lower),
        "host_digit_count": sum(c.isdigit() for c in host_lower),
        "path_digit_count": sum(c.isdigit() for c in path),
        "suspicious_token_count": effective_token_count,
    }

    return features


# ============================================================
# Model prediction
# ============================================================

def predict_url(url: str) -> dict:
    features = extract_url_features(url)

    X = pd.DataFrame(
        [[features[name] for name in FEATURE_NAMES]],
        columns=FEATURE_NAMES,
    )

    probability = float(model.predict_proba(X)[0, 1])

    # Dampen false-positive penalty on clean single-hyphen HTTPS domains
    # (e.g., webdesign-inspiration.com) when no suspicious tokens or digits exist.
    if (
        features["hyphen_count"] <= 1
        and features["suspicious_token_count"] == 0
        and features["subdomain_count"] == 0
        and features["https"] == 1
        and features["host_digit_count"] == 0
        and features["has_ip_address"] == 0
    ):
        probability = min(probability, 0.30)

    return {
        "phishing_probability": probability,
        "features": features,
    }