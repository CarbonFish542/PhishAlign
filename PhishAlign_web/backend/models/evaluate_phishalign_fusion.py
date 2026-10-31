import json
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

ROOT = Path(r"D:\Phish360")
DATA_DIR = ROOT / "phishalign_training_data"
OUTPUT = ROOT / "phishalign_fusion_output"
OUTPUT.mkdir(parents=True, exist_ok=True)

TRAIN_PATH = DATA_DIR / "phishalign_oof_train.csv"
VAL_PATH = DATA_DIR / "phishalign_validation.csv"

train = pd.read_csv(TRAIN_PATH)
val = pd.read_csv(VAL_PATH)

probability_cols = [
    "url_probability",
    "html_probability",
    "visual_probability",
]

consistency_cols = [
    "html_available",
    "ocr_available",
    "title_available",
    "both_html_ocr_available",
    "url_host_available",
    "url_html_jaccard",
    "url_html_containment",
    "url_ocr_jaccard",
    "url_ocr_containment",
    "url_title_jaccard",
    "url_title_containment",
    "html_ocr_jaccard",
    "html_ocr_containment",
    "title_ocr_jaccard",
    "title_ocr_containment",
    "domain_identity_token_count_v3",
    "domain_html_jaccard_v3",
    "domain_html_containment_v3",
    "domain_html_comparison_available_v3",
    "domain_ocr_jaccard_v3",
    "domain_ocr_containment_v3",
    "domain_ocr_comparison_available_v3",
    "domain_title_jaccard_v3",
    "domain_title_containment_v3",
    "domain_title_comparison_available_v3",
]

TARGET = "y_true"
THRESHOLD = 0.5

# -------------------- Integrity checks --------------------

for name, df in [("train", train), ("validation", val)]:
    if df["sample_id"].duplicated().any():
        raise ValueError(f"Duplicate IDs in {name}.")
    if df[TARGET].isna().any() or not df[TARGET].isin([0, 1]).all():
        raise ValueError(f"Invalid labels in {name}.")

feature_cols = probability_cols + consistency_cols

for name, df in [("train", train), ("validation", val)]:
    missing_cols = [c for c in feature_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"{name} missing columns: {missing_cols}")
    if df[feature_cols].isna().any().any():
        raise ValueError(f"Missing feature values in {name}.")

# Confirm that the feature definitions match the saved train table.
print("Training rows:", len(train))
print("Validation rows:", len(val))
print("Training class counts:", train[TARGET].value_counts().sort_index().to_dict())
print("Validation class counts:", val[TARGET].value_counts().sort_index().to_dict())

y_train = train[TARGET].astype(int).to_numpy()
y_val = val[TARGET].astype(int).to_numpy()

# -------------------- Model definitions --------------------

# Conventional late fusion: equal-weight average.
equal_prob = train[probability_cols].mean(axis=1).to_numpy()
equal_val_prob = val[probability_cols].mean(axis=1).to_numpy()

# Probability-only stacking.
prob_model = Pipeline([
    ("scale", StandardScaler()),
    ("logistic", LogisticRegression(
        C=1.0,
        max_iter=2000,
        random_state=42,
    )),
])
prob_model.fit(train[probability_cols], y_train)
stack_prob = prob_model.predict_proba(val[probability_cols])[:, 1]

# PhishAlign: base probabilities + explicit consistency features.
phishalign_cols = probability_cols + consistency_cols
phishalign_model = Pipeline([
    ("scale", StandardScaler()),
    ("logistic", LogisticRegression(
        C=1.0,
        max_iter=3000,
        random_state=42,
    )),
])
phishalign_model.fit(train[phishalign_cols], y_train)
phishalign_prob = phishalign_model.predict_proba(val[phishalign_cols])[:, 1]

# -------------------- Evaluation --------------------

def evaluate(name, probabilities):
    predictions = (probabilities >= THRESHOLD).astype(int)
    cm = confusion_matrix(y_val, predictions, labels=[0, 1])

    result = {
        "model": name,
        "threshold": THRESHOLD,
        "accuracy": accuracy_score(y_val, predictions),
        "phishing_precision": precision_score(
            y_val, predictions, zero_division=0
        ),
        "phishing_recall": recall_score(
            y_val, predictions, zero_division=0
        ),
        "phishing_f1": f1_score(
            y_val, predictions, zero_division=0
        ),
        "roc_auc": roc_auc_score(y_val, probabilities),
        "tn": int(cm[0, 0]),
        "fp": int(cm[0, 1]),
        "fn": int(cm[1, 0]),
        "tp": int(cm[1, 1]),
    }
    return result, predictions

results = []
prediction_rows = val[["sample_id", TARGET]].copy()

for name, probabilities in [
    ("Equal-weight fusion", equal_val_prob),
    ("Probability-only stacking", stack_prob),
    ("PhishAlign: probabilities + consistency", phishalign_prob),
]:
    result, predictions = evaluate(name, probabilities)
    results.append(result)
    safe_name = (
        name.lower()
        .replace(" ", "_")
        .replace(":", "")
        .replace("+", "plus")
        .replace("-", "_")
    )
    prediction_rows[f"{safe_name}_probability"] = probabilities
    prediction_rows[f"{safe_name}_prediction"] = predictions

results_df = pd.DataFrame(results)

print("\nVALIDATION RESULTS (threshold = 0.5)")
print(results_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

results_path = OUTPUT / "validation_fusion_metrics.csv"
predictions_path = OUTPUT / "validation_fusion_predictions.csv"

results_df.to_csv(results_path, index=False)
prediction_rows.to_csv(predictions_path, index=False)

# Save fitted stacking models for reproducibility.
import joblib
joblib.dump(prob_model, OUTPUT / "probability_only_stacking.joblib")
joblib.dump(phishalign_model, OUTPUT / "phishalign_stacking.joblib")

manifest = {
    "training_table": str(TRAIN_PATH),
    "validation_table": str(VAL_PATH),
    "training_rows": int(len(train)),
    "validation_rows": int(len(val)),
    "threshold": THRESHOLD,
    "probability_features": probability_cols,
    "consistency_features": consistency_cols,
    "models": [
        "Equal-weight probability average",
        "StandardScaler + LogisticRegression on probabilities",
        "StandardScaler + LogisticRegression on probabilities and consistency features",
    ],
    "official_test_used": False,
    "note": "Validation-only comparison. OOF predictions used for stacking-model training.",
}
(OUTPUT / "run_manifest.json").write_text(json.dumps(manifest, indent=2))

print("\nSaved metrics:", results_path)
print("Saved predictions:", predictions_path)
print("Saved models in:", OUTPUT)
