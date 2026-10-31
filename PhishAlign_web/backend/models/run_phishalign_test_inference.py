from pathlib import Path
import json
import sys
import warnings

import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

# -------------------- Paths --------------------

ROOT = Path(r"D:\Phish360")
sys.path.insert(0, str(ROOT / "scripts"))

from url_baseline import extract_url_features
from html_baseline import extract_html_features

METADATA = ROOT / "metadata" / "phish360_metadata_split_clean.csv"
CONSISTENCY = ROOT / "consistency_output" / "test_consistency_features_v3.csv"

URL_MODEL_PATH = ROOT / "url_baseline_output" / "url_xgboost_model.joblib"
URL_FEATURES_PATH = ROOT / "url_baseline_output" / "url_feature_names.json"

HTML_MODEL_PATH = ROOT / "html_baseline_output" / "html_xgboost_model.joblib"
HTML_FEATURES_PATH = ROOT / "html_baseline_output" / "html_feature_names.json"

VISUAL_CHECKPOINT = (
    ROOT / "visual_oof_output" /
    "visual_validation_model_oofprotocol.pth"
)

FUSION_DIR = ROOT / "phishalign_fusion_output"
PROB_FUSION_PATH = FUSION_DIR / "probability_only_stacking.joblib"
PHISHALIGN_PATH = FUSION_DIR / "phishalign_stacking.joblib"

OUTPUT = ROOT / "official_test_inference"
OUTPUT.mkdir(parents=True, exist_ok=True)

# -------------------- Feature definitions --------------------

PROBABILITY_COLS = [
    "url_probability",
    "html_probability",
    "visual_probability",
]

CONSISTENCY_COLS = [
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

# -------------------- Helpers --------------------

def load_feature_names(path):
    obj = json.loads(path.read_text(encoding="utf-8-sig"))

    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for key in ("feature_names", "features", "columns"):
            if key in obj and isinstance(obj[key], list):
                return obj[key]

    raise ValueError(f"Unrecognized feature-name JSON format: {path}")


def require_columns(df, columns, name):
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"{name} is missing required columns: {missing}")


def positive_probability(model, frame):
    probabilities = model.predict_proba(frame)
    classes = list(model.classes_)
    if 1 not in classes:
        raise ValueError(f"Model has no positive class 1: {classes}")
    return probabilities[:, classes.index(1)]


# -------------------- Load test metadata --------------------

print("Loading official test metadata...")
metadata = pd.read_csv(METADATA, dtype={"sample_id": str})
metadata = metadata[metadata["dataset_split"].eq("test")].copy()
metadata["sample_id"] = metadata["sample_id"].astype(str)

if metadata["sample_id"].duplicated().any():
    raise ValueError("Duplicate sample IDs in test metadata.")

require_columns(
    metadata,
    ["sample_id", "url", "html_path", "screenshot_path"],
    "Test metadata",
)

print("Official test samples:", len(metadata))

# -------------------- Load saved models and schemas --------------------

url_model = joblib.load(URL_MODEL_PATH)
html_model = joblib.load(HTML_MODEL_PATH)
prob_fusion = joblib.load(PROB_FUSION_PATH)
phishalign = joblib.load(PHISHALIGN_PATH)

url_features = load_feature_names(URL_FEATURES_PATH)
html_features = load_feature_names(HTML_FEATURES_PATH)

if len(url_features) != 31 or url_model.n_features_in_ != len(url_features):
    raise ValueError("URL model/schema feature-count mismatch.")

if len(html_features) != 64 or html_model.n_features_in_ != len(html_features):
    raise ValueError("HTML model/schema feature-count mismatch.")

if prob_fusion.n_features_in_ != len(PROBABILITY_COLS):
    raise ValueError("Probability-fusion input count mismatch.")

if phishalign.n_features_in_ != (
    len(PROBABILITY_COLS) + len(CONSISTENCY_COLS)
):
    raise ValueError("PhishAlign input count mismatch.")

# -------------------- URL inference --------------------

print("\nExtracting URL features...")
url_rows = []
for _, row in metadata.iterrows():
    features = extract_url_features(str(row["url"]))
    if features is None:
        raise ValueError(f"URL extraction failed: {row['sample_id']}")
    url_rows.append(features)

url_frame = pd.DataFrame(url_rows)
require_columns(url_frame, url_features, "Extracted URL features")
url_frame = url_frame[url_features].apply(pd.to_numeric, errors="raise")

metadata["url_probability"] = positive_probability(url_model, url_frame)

# -------------------- HTML inference --------------------

print("Extracting HTML features...")
html_records = []
html_failed_ids = []

for _, row in metadata.iterrows():
    sample_id = row["sample_id"]
    features = extract_html_features(row["html_path"])

    if features is None:
        html_failed_ids.append(sample_id)
        continue

    record = {"sample_id": sample_id}
    record.update(features)
    html_records.append(record)

html_frame = pd.DataFrame(html_records)

if len(html_frame):
    require_columns(html_frame, html_features, "Extracted HTML features")
    X_html = html_frame[html_features].apply(pd.to_numeric, errors="raise")
    html_frame["html_probability"] = positive_probability(html_model, X_html)
    html_predictions = html_frame[["sample_id", "html_probability"]]
else:
    html_predictions = pd.DataFrame(
        columns=["sample_id", "html_probability"]
    )

metadata = metadata.merge(
    html_predictions, on="sample_id", how="left", validate="one_to_one"
)

# -------------------- Visual model and inference --------------------

print("Loading visual checkpoint...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Inference device:", device)

visual_model = models.mobilenet_v3_small(weights=None)
visual_model.classifier[-1] = nn.Linear(
    visual_model.classifier[-1].in_features, 2
)

state = torch.load(
    VISUAL_CHECKPOINT,
    map_location="cpu",
    weights_only=True,
)
visual_model.load_state_dict(state, strict=True)
visual_model = visual_model.to(device)
visual_model.eval()

visual_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

visual_probabilities = {}
visual_failed_ids = []

print("Running visual inference...")
with torch.no_grad():
    for _, row in metadata.iterrows():
        sample_id = row["sample_id"]
        image_path = Path(str(row["screenshot_path"]))

        try:
            with Image.open(image_path) as image:
                image = image.convert("RGB")
                tensor = visual_transform(image).unsqueeze(0).to(device)

            logits = visual_model(tensor)
            probability = torch.softmax(logits, dim=1)[0, 1].item()
            visual_probabilities[sample_id] = float(probability)

        except Exception as exc:
            visual_failed_ids.append({
                "sample_id": sample_id,
                "error": str(exc),
            })

metadata["visual_probability"] = metadata["sample_id"].map(
    visual_probabilities
)

# -------------------- Join consistency features --------------------

print("Joining consistency features...")
consistency = pd.read_csv(CONSISTENCY, dtype={"sample_id": str})
consistency["sample_id"] = consistency["sample_id"].astype(str)

if consistency["sample_id"].duplicated().any():
    raise ValueError("Duplicate sample IDs in test consistency table.")

require_columns(
    consistency,
    ["sample_id"] + CONSISTENCY_COLS,
    "Test consistency table",
)

# The metadata may already contain some consistency columns.
# Drop those copies so the values from the dedicated consistency
# feature table retain their original names and are used by PhishAlign.
overlapping_cols = [
    col for col in CONSISTENCY_COLS
    if col in metadata.columns
]

if overlapping_cols:
    print("Replacing overlapping metadata columns:", overlapping_cols)
    metadata = metadata.drop(columns=overlapping_cols)

metadata = metadata.merge(
    consistency[["sample_id"] + CONSISTENCY_COLS],
    on="sample_id",
    how="left",
    validate="one_to_one",
)

# Confirm the expected feature names survived the merge.
missing_consistency_cols = [
    col for col in CONSISTENCY_COLS
    if col not in metadata.columns
]
if missing_consistency_cols:
    raise ValueError(
        f"Consistency columns missing after merge: {missing_consistency_cols}"
    )

# Check consistency values exist for every official test ID.
if metadata[CONSISTENCY_COLS].isna().any().any():
    missing_count = int(metadata[CONSISTENCY_COLS].isna().any(axis=1).sum())
    raise ValueError(
        f"{missing_count} rows have missing consistency features. "
        "Inspect the consistency table before inference."
    )

# -------------------- Fusion inference on complete cases --------------------

complete_mask = metadata[
    PROBABILITY_COLS
].notna().all(axis=1)

complete = metadata.loc[complete_mask].copy()

if complete.empty:
    raise ValueError("No complete-case test rows available.")

print("\nComplete-case test samples:", len(complete))
print("Excluded due to missing HTML probability:", int(metadata["html_probability"].isna().sum()))
print("Excluded due to missing visual probability:", int(metadata["visual_probability"].isna().sum()))

# Fixed feature order from the training script.
X_prob = complete[PROBABILITY_COLS].astype(float)
X_phishalign = complete[PROBABILITY_COLS + CONSISTENCY_COLS].astype(float)

complete["probability_only_probability"] = positive_probability(
    prob_fusion, X_prob
)
complete["phishalign_probability"] = positive_probability(
    phishalign, X_phishalign
)

# Equal-weight late fusion, matching the validation definition.
complete["equal_weight_probability"] = complete[
    PROBABILITY_COLS
].mean(axis=1)

# -------------------- Save predictions and audit --------------------

prediction_cols = [
    "sample_id",
    "url_probability",
    "html_probability",
    "visual_probability",
    "equal_weight_probability",
    "probability_only_probability",
    "phishalign_probability",
]

complete[prediction_cols].to_csv(
    OUTPUT / "official_test_predictions_complete_cases.csv",
    index=False,
)

# Keep all official test IDs in the audit, including excluded cases.
audit = metadata[[
    "sample_id",
    "url_probability",
    "html_probability",
    "visual_probability",
]].copy()

audit["complete_case"] = complete_mask.to_numpy()
audit["exclusion_reason"] = ""

audit.loc[
    audit["html_probability"].isna(),
    "exclusion_reason"
] += "html_probability_unavailable;"

audit.loc[
    audit["visual_probability"].isna(),
    "exclusion_reason"
] += "visual_probability_unavailable;"

audit.to_csv(
    OUTPUT / "official_test_inference_audit.csv",
    index=False,
)

pd.DataFrame({"sample_id": html_failed_ids}).to_csv(
    OUTPUT / "html_inference_failures.csv",
    index=False,
)

pd.DataFrame(visual_failed_ids).to_csv(
    OUTPUT / "visual_inference_failures.csv",
    index=False,
)

manifest = {
    "official_test_rows": int(len(metadata)),
    "complete_case_rows": int(len(complete)),
    "html_probability_missing": int(metadata["html_probability"].isna().sum()),
    "visual_probability_missing": int(metadata["visual_probability"].isna().sum()),
    "fusion_threshold": 0.5,
    "test_labels_used_for_inference": False,
    "fusion_feature_order": PROBABILITY_COLS + CONSISTENCY_COLS,
    "prediction_file": "official_test_predictions_complete_cases.csv",
    "audit_file": "official_test_inference_audit.csv",
}

(OUTPUT / "inference_manifest.json").write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8",
)

print("\nINFERENCE COMPLETE")
print("Output folder:", OUTPUT)
print("Prediction rows:", len(complete))
print("All official test IDs audited:", len(audit))
print("HTML extraction failures:", len(html_failed_ids))
print("Visual inference failures:", len(visual_failed_ids))
print("No test labels were loaded or used.")