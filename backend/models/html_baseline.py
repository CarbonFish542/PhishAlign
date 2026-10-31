import json
import re
from collections import Counter
from pathlib import Path

import joblib
import pandas as pd
from bs4 import BeautifulSoup
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

BASE_DIR = Path(r"D:\Phish360")
CSV_PATH = BASE_DIR / "metadata" / "phish360_metadata_split_clean.csv"
OUTPUT_DIR = BASE_DIR / "html_baseline_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Safety/resource limit: read at most 2 MB from each HTML file.
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


def extract_html_features(html_path):
    """Read HTML as inert text and extract static features only."""
    features = {}

    try:
        path = Path(str(html_path))

        if not path.is_file():
            return None

        with path.open("rb") as file:
            raw = file.read(MAX_HTML_BYTES)

        html = raw.decode("utf-8", errors="replace")

        # Built-in html.parser: no browser, JavaScript, or network requests.
        soup = BeautifulSoup(html, "html.parser")

        # Basic document and text characteristics.
        text = soup.get_text(" ", strip=True)
        text_lower = text.lower()

        features["html_bytes_read"] = len(raw)
        features["html_truncated"] = int(path.stat().st_size > MAX_HTML_BYTES)
        features["text_length"] = len(text)
        features["word_count"] = len(text.split())
        features["unique_word_count"] = len(set(text_lower.split()))
        features["average_word_length"] = (
            sum(len(word) for word in text.split()) / max(1, len(text.split()))
        )

        # Tag counts.
        for tag in TAGS:
            features[f"tag_{tag}_count"] = len(soup.find_all(tag))

        # Forms and input characteristics.
        inputs = soup.find_all("input")
        input_types = [
            str(element.get("type", "")).lower()
            for element in inputs
        ]

        features["input_count"] = len(inputs)
        features["password_input_count"] = input_types.count("password")
        features["hidden_input_count"] = input_types.count("hidden")
        features["email_input_count"] = input_types.count("email")
        features["submit_input_count"] = input_types.count("submit")
        features["form_count"] = len(soup.find_all("form"))
        features["form_with_action_count"] = sum(
            bool(form.get("action")) for form in soup.find_all("form")
        )

        # Link and resource characteristics.
        links = soup.find_all("a")
        hrefs = [str(a.get("href", "")) for a in links]

        features["anchor_count"] = len(links)
        features["empty_href_count"] = sum(not href.strip() for href in hrefs)
        features["javascript_href_count"] = sum(
            href.strip().lower().startswith("javascript:") for href in hrefs
        )
        features["data_href_count"] = sum(
            href.strip().lower().startswith("data:") for href in hrefs
        )

        features["image_count"] = len(soup.find_all("img"))
        features["image_missing_src_count"] = sum(
            not str(img.get("src", "")).strip()
            for img in soup.find_all("img")
        )

        # Embedded code and event-handler attributes.
        features["script_count"] = len(soup.find_all("script"))
        features["external_script_reference_count"] = sum(
            bool(script.get("src")) for script in soup.find_all("script")
        )
        features["inline_script_count"] = sum(
            not script.get("src") for script in soup.find_all("script")
        )

        all_tags = soup.find_all(True)
        event_attributes = [
            attr
            for tag in all_tags
            for attr in tag.attrs
            if str(attr).lower().startswith("on")
        ]

        features["event_handler_attribute_count"] = len(event_attributes)
        features["style_attribute_count"] = sum(
            "style" in tag.attrs for tag in all_tags
        )
        features["iframe_count"] = len(soup.find_all("iframe"))
        features["meta_refresh_count"] = sum(
            str(meta.get("http-equiv", "")).lower() == "refresh"
            for meta in soup.find_all("meta")
        )

        # Text-based indicators.
        features["title_length"] = len(
            soup.title.get_text(" ", strip=True) if soup.title else ""
        )
        features["suspicious_term_count"] = sum(
            text_lower.count(term) for term in SUSPICIOUS_TERMS
        )
        features["https_text_count"] = text_lower.count("https://")
        features["http_text_count"] = text_lower.count("http://")

        # HTML attribute patterns.
        features["external_style_reference_count"] = sum(
            bool(link.get("href"))
            for link in soup.find_all("link")
            if "stylesheet" in str(link.get("rel", "")).lower()
        )
        features["target_blank_count"] = sum(
            str(a.get("target", "")).lower() == "_blank"
            for a in links
        )

        # Character-level indicators from the raw HTML.
        html_lower = html.lower()
        features["at_symbol_count"] = html.count("@")
        features["encoded_entity_count"] = len(
            re.findall(r"&#(?:x[0-9a-f]+|\d+);", html_lower)
        )
        features["base64_marker_count"] = html_lower.count("base64")

        return features

    except (OSError, ValueError, UnicodeError):
        return None


def main():
    print("Loading metadata...")
    df = pd.read_csv(CSV_PATH)

    required = {
        "sample_id", "html_path", "html_available",
        "binary_label", "dataset_split",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # Exclude test and test_connected from development.
    df = df[
        df["dataset_split"].isin(["train", "validation"])
        & (df["html_available"] == 1)
    ].copy()

    label_map = {"legitimate": 0, "phishing": 1}
    df["target"] = (
        df["binary_label"].astype(str).str.lower().map(label_map)
    )
    df = df.dropna(subset=["target", "html_path"]).reset_index(drop=True)
    df["target"] = df["target"].astype(int)

    print(f"HTML samples to process: {len(df)}")

    rows = []
    kept_indices = []

    print("\nExtracting static HTML features...")
    for index, row in df.iterrows():
        features = extract_html_features(row["html_path"])

        if features is not None:
            rows.append(features)
            kept_indices.append(index)

        if (index + 1) % 500 == 0:
            print(f"Processed {index + 1}/{len(df)}")

    if not rows:
        raise RuntimeError("No HTML files could be processed.")

    X = pd.DataFrame(rows).fillna(0)
    used_df = df.iloc[kept_indices].reset_index(drop=True)
    y = used_df["target"]
    splits = used_df["dataset_split"]

    train_mask = splits == "train"
    val_mask = splits == "validation"

    X_train = X.loc[train_mask].reset_index(drop=True)
    y_train = y.loc[train_mask].reset_index(drop=True)
    X_val = X.loc[val_mask].reset_index(drop=True)
    y_val = y.loc[val_mask].reset_index(drop=True)

    print("\nDataset summary")
    print(f"Processed samples: {len(used_df)}")
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Features: {X.shape[1]}")
    print("\nClass distribution:")
    print(used_df.groupby(["dataset_split", "binary_label"]).size())

    model = XGBClassifier(
        n_estimators=500,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
        tree_method="hist",
    )

    print("\nTraining HTML-only XGBoost baseline...")
    model.fit(X_train, y_train)

    print("\nEvaluating on validation set...")
    predictions = model.predict(X_val)
    probabilities = model.predict_proba(X_val)[:, 1]

    results = {
        "accuracy": float(accuracy_score(y_val, predictions)),
        "precision": float(precision_score(y_val, predictions, zero_division=0)),
        "recall": float(recall_score(y_val, predictions, zero_division=0)),
        "f1": float(f1_score(y_val, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_val, probabilities)),
        "confusion_matrix": confusion_matrix(y_val, predictions).tolist(),
        "training_samples": int(len(X_train)),
        "validation_samples": int(len(X_val)),
        "feature_count": int(X.shape[1]),
    }

    print("\nHTML VALIDATION RESULTS")
    for name, value in results.items():
        print(f"{name}: {value}")

    print("\nClassification report:")
    print(
        classification_report(
            y_val,
            predictions,
            target_names=["legitimate", "phishing"],
            zero_division=0,
        )
    )

    # Save model and supporting artifacts.
    joblib.dump(model, OUTPUT_DIR / "html_xgboost_model.joblib")

    with open(OUTPUT_DIR / "html_feature_names.json", "w") as file:
        json.dump(list(X.columns), file, indent=2)

    with open(OUTPUT_DIR / "validation_metrics.json", "w") as file:
        json.dump(results, file, indent=2)

    validation_output = used_df.loc[
        val_mask.to_numpy(),
        ["sample_id", "binary_label", "html_path"],
    ].copy()

    validation_output["predicted_label"] = [
        "phishing" if value == 1 else "legitimate"
        for value in predictions
    ]
    validation_output["phishing_probability"] = probabilities

    validation_output.to_csv(
        OUTPUT_DIR / "validation_predictions.csv",
        index=False,
    )

    print(f"\nSaved outputs to: {OUTPUT_DIR}")
    print("Official test set was not used.")


if __name__ == "__main__":
    main()