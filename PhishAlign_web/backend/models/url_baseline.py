import ipaddress
import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

import joblib
import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

BASE_DIR = Path(r"D:\Phish360")
CSV_PATH = BASE_DIR / "metadata" / "phish360_metadata_split_clean.csv"
OUTPUT_DIR = BASE_DIR / "url_baseline_output"
OUTPUT_DIR.mkdir(exist_ok=True)


def entropy(text):
    """Calculate character-level Shannon entropy."""
    if not text:
        return 0.0

    counts = Counter(text)
    length = len(text)

    return -sum(
        (count / length) * math.log2(count / length)
        for count in counts.values()
    )


def extract_url_features(raw_url):
    """Extract numerical features from a URL without visiting it."""
    url = str(raw_url).strip()

    # Add a scheme only for parsing; preserve the original URL for features.
    parse_url = url if "://" in url else "http://" + url

    try:
        parsed = urlsplit(parse_url)
        host = parsed.hostname or ""
        path = parsed.path or ""
        query = parsed.query or ""
        fragment = parsed.fragment or ""
    except Exception:
        host, path, query, fragment = "", "", "", ""

    host_lower = host.lower()
    url_lower = url.lower()

    try:
        is_ip = int(bool(host) and ipaddress.ip_address(host).version in (4, 6))
    except ValueError:
        is_ip = 0

    try:
        port_present = int(parsed.port is not None)
    except (ValueError, AttributeError):
        port_present = 0

    subdomain_count = max(0, len(host_lower.split(".")) - 2) if host_lower else 0

    suspicious_tokens = [
        "login", "signin", "sign-in", "verify", "verification",
        "account", "secure", "security", "update", "password",
        "bank", "confirm", "billing", "wallet", "payment",
        "authenticate", "support", "recover", "webscr",
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
        "suspicious_token_count": sum(
            token in url_lower for token in suspicious_tokens
        ),
    }

    return features


def main():
    print("Loading metadata...")
    df = pd.read_csv(CSV_PATH)

    required_columns = {"url", "binary_label", "dataset_split"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required CSV columns: {sorted(missing)}")

    # Use only the intended development splits. Keep official test untouched.
    df = df[df["dataset_split"].isin(["train", "validation"])].copy()
    df = df.dropna(subset=["url", "binary_label"])

    label_map = {"legitimate": 0, "phishing": 1}
    df["target"] = df["binary_label"].astype(str).str.lower().map(label_map)
    df = df.dropna(subset=["target"])
    df["target"] = df["target"].astype(int)

    print(f"Development samples: {len(df)}")
    print(df.groupby(["dataset_split", "binary_label"]).size())

    print("\nExtracting URL features...")
    feature_rows = [extract_url_features(url) for url in df["url"]]
    X = pd.DataFrame(feature_rows)
    y = df["target"].reset_index(drop=True)
    splits = df["dataset_split"].reset_index(drop=True)

    train_mask = splits == "train"
    val_mask = splits == "validation"

    X_train, y_train = X.loc[train_mask], y.loc[train_mask]
    X_val, y_val = X.loc[val_mask], y.loc[val_mask]

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Features: {X.shape[1]}")

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

    print("\nTraining XGBoost URL-only baseline...")
    model.fit(X_train, y_train)

    print("\nEvaluating on validation set...")
    predictions = model.predict(X_val)
    probabilities = model.predict_proba(X_val)[:, 1]

    results = {
        "accuracy": accuracy_score(y_val, predictions),
        "precision": precision_score(y_val, predictions, zero_division=0),
        "recall": recall_score(y_val, predictions, zero_division=0),
        "f1": f1_score(y_val, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_val, probabilities),
        "confusion_matrix": confusion_matrix(y_val, predictions).tolist(),
    }

    print("\nVALIDATION RESULTS")
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

    # Save model, feature list, and validation results.
    joblib.dump(model, OUTPUT_DIR / "url_xgboost_model.joblib")

    with open(OUTPUT_DIR / "url_feature_names.json", "w") as f:
        json.dump(list(X.columns), f, indent=2)

    with open(OUTPUT_DIR / "validation_metrics.json", "w") as f:
        json.dump(results, f, indent=2)

    # Save validation predictions for later analysis.
    validation_output = df.iloc[val_mask.to_numpy()][["sample_id", "url", "binary_label"]].copy()
    validation_output["predicted_label"] = [
        "phishing" if p == 1 else "legitimate" for p in predictions
    ]
    validation_output["phishing_probability"] = probabilities
    validation_output.to_csv(
        OUTPUT_DIR / "validation_predictions.csv", index=False
    )

    print(f"\nSaved outputs to: {OUTPUT_DIR}")
    print("Official test set was not used.")


if __name__ == "__main__":
    main()
