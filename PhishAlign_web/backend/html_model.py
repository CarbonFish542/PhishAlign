import json
import re
from pathlib import Path

import joblib
import pandas as pd
from bs4 import BeautifulSoup


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "html_xgboost_model.joblib"
FEATURE_NAMES_PATH = MODEL_DIR / "html_feature_names.json"

MAX_HTML_BYTES = 2 * 1024 * 1024


# ============================================================
# Frozen model
# ============================================================

model = joblib.load(MODEL_PATH)

with open(FEATURE_NAMES_PATH, "r", encoding="utf-8") as f:
    FEATURE_NAMES = json.load(f)


# ============================================================
# Exact frozen constants
# ============================================================

TAGS = [
    "a",
    "area",
    "base",
    "button",
    "form",
    "input",
    "textarea",
    "select",
    "option",
    "iframe",
    "frame",
    "img",
    "script",
    "link",
    "meta",
    "style",
    "div",
    "span",
    "p",
    "h1",
    "h2",
    "h3",
    "table",
    "tr",
    "td",
    "th",
    "svg",
    "object",
    "embed",
]


SUSPICIOUS_TERMS = [
    "login",
    "signin",
    "sign in",
    "log in",
    "verify",
    "verification",
    "password",
    "account",
    "bank",
    "secure",
    "security",
    "update",
    "confirm",
    "billing",
    "payment",
    "wallet",
    "suspended",
    "unusual activity",
    "authentication",
    "recover",
]


# ============================================================
# HTML feature extraction
# ============================================================

def extract_html_features_from_bytes(raw_html):
    """
    Runtime version of the frozen HTML feature extractor.

    raw_html should be bytes obtained from the webpage.
    """

    if raw_html is None:
        return None

    try:
        # Preserve the research 2 MB limit.
        raw = bytes(raw_html[:MAX_HTML_BYTES])

        html = raw.decode(
            "utf-8",
            errors="replace",
        )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        # ----------------------------------------------------
        # Basic document/text characteristics
        # ----------------------------------------------------

        text = soup.get_text(
            " ",
            strip=True,
        )

        text_lower = text.lower()

        features = {}

        features["html_bytes_read"] = len(raw)

        # Runtime input is already limited to MAX_HTML_BYTES.
        features["html_truncated"] = int(
            len(raw_html) > MAX_HTML_BYTES
        )

        features["text_length"] = len(text)

        features["word_count"] = len(
            text.split()
        )

        features["unique_word_count"] = len(
            set(text_lower.split())
        )

        features["average_word_length"] = (
            sum(
                len(word)
                for word in text.split()
            )
            / max(
                1,
                len(text.split()),
            )
        )

        # ----------------------------------------------------
        # Tag counts
        # ----------------------------------------------------

        for tag in TAGS:
            features[
                f"tag_{tag}_count"
            ] = len(
                soup.find_all(tag)
            )

        # ----------------------------------------------------
        # Forms and input characteristics
        # ----------------------------------------------------

        inputs = soup.find_all("input")

        input_types = [
            str(
                element.get(
                    "type",
                    "",
                )
            ).lower()
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

        forms = soup.find_all("form")

        features["form_count"] = len(forms)

        features["form_with_action_count"] = sum(
            bool(form.get("action"))
            for form in forms
        )

        # ----------------------------------------------------
        # Links
        # ----------------------------------------------------

        links = soup.find_all("a")

        hrefs = [
            str(
                a.get(
                    "href",
                    "",
                )
            )
            for a in links
        ]

        features["anchor_count"] = len(links)

        features["empty_href_count"] = sum(
            not href.strip()
            for href in hrefs
        )

        features["javascript_href_count"] = sum(
            href.strip()
            .lower()
            .startswith("javascript:")
            for href in hrefs
        )

        features["data_href_count"] = sum(
            href.strip()
            .lower()
            .startswith("data:")
            for href in hrefs
        )

        # ----------------------------------------------------
        # Images
        # ----------------------------------------------------

        images = soup.find_all("img")

        features["image_count"] = len(images)

        features["image_missing_src_count"] = sum(
            not str(
                img.get(
                    "src",
                    "",
                )
            ).strip()
            for img in images
        )

        # ----------------------------------------------------
        # Scripts
        # ----------------------------------------------------

        scripts = soup.find_all("script")

        features["script_count"] = len(scripts)

        features[
            "external_script_reference_count"
        ] = sum(
            bool(script.get("src"))
            for script in scripts
        )

        features["inline_script_count"] = sum(
            not script.get("src")
            for script in scripts
        )

        # ----------------------------------------------------
        # Event handlers / attributes
        # ----------------------------------------------------

        all_tags = soup.find_all(True)

        event_attributes = [
            attr
            for tag in all_tags
            for attr in tag.attrs
            if str(attr)
            .lower()
            .startswith("on")
        ]

        features[
            "event_handler_attribute_count"
        ] = len(event_attributes)

        features["style_attribute_count"] = sum(
            "style" in tag.attrs
            for tag in all_tags
        )

        features["iframe_count"] = len(
            soup.find_all("iframe")
        )

        features["meta_refresh_count"] = sum(
            str(
                meta.get(
                    "http-equiv",
                    "",
                )
            ).lower()
            == "refresh"
            for meta in soup.find_all("meta")
        )

        # ----------------------------------------------------
        # Text indicators
        # ----------------------------------------------------

        title_text = (
            soup.title.get_text(
                " ",
                strip=True,
            )
            if soup.title
            else ""
        )

        features["title_length"] = len(
            title_text
        )

        features[
            "suspicious_term_count"
        ] = sum(
            text_lower.count(term)
            for term in SUSPICIOUS_TERMS
        )

        features["https_text_count"] = (
            text_lower.count("https://")
        )

        features["http_text_count"] = (
            text_lower.count("http://")
        )

        # ----------------------------------------------------
        # HTML attributes
        # ----------------------------------------------------

        features[
            "external_style_reference_count"
        ] = sum(
            bool(link.get("href"))
            for link in soup.find_all("link")
            if "stylesheet"
            in str(
                link.get(
                    "rel",
                    "",
                )
            ).lower()
        )

        features["target_blank_count"] = sum(
            str(
                a.get(
                    "target",
                    "",
                )
            ).lower()
            == "_blank"
            for a in links
        )

        # ----------------------------------------------------
        # Raw HTML character indicators
        # ----------------------------------------------------

        html_lower = html.lower()

        features["at_symbol_count"] = (
            html.count("@")
        )

        features["encoded_entity_count"] = len(
            re.findall(
                r"&#(?:x[0-9a-f]+|\d+);",
                html_lower,
            )
        )

        features["base64_marker_count"] = (
            html_lower.count("base64")
        )

        return features

    except (
        ValueError,
        UnicodeError,
        TypeError,
    ):
        return None


# ============================================================
# Text/title helper
# ============================================================

def extract_html_content(raw_html):
    """
    Extract the two pieces of content required by
    PhishAlign consistency.py:

        html_text
        title
    """

    if raw_html is None:
        return "", ""

    raw = bytes(raw_html[:MAX_HTML_BYTES])

    html = raw.decode(
        "utf-8",
        errors="replace",
    )

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    title = (
        soup.title.get_text(
            " ",
            strip=True,
        )
        if soup.title
        else ""
    )

    html_text = soup.get_text(
        " ",
        strip=True,
    )

    return html_text, title


# ============================================================
# Prediction
# ============================================================

def predict_html(raw_html):
    """
    Run the frozen HTML XGBoost model.
    """

    features = extract_html_features_from_bytes(
        raw_html
    )

    if features is None:
        raise ValueError(
            "Unable to extract HTML features."
        )

    X = pd.DataFrame(
        [[
            features[name]
            for name in FEATURE_NAMES
        ]],
        columns=FEATURE_NAMES,
    )

    probability = float(
        model.predict_proba(X)[0, 1]
    )

    html_text, title = extract_html_content(
        raw_html
    )

    return {
        "phishing_probability": probability,
        "features": features,
        "html_text": html_text,
        "title": title,
    }