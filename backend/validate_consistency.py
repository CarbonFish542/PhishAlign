import sys
from pathlib import Path

import numpy as np
import pandas as pd

from app.consistency import (
    CONSISTENCY_FEATURES,
    extract_consistency_features,
)


# ============================================================
# Frozen Phish360 research artifacts
# ============================================================

CONSISTENCY_FILE = Path(
    r"D:\Phish360\consistency_output\test_consistency_features_v3.csv"
)

HTML_FILE = Path(
    r"D:\Phish360\html_text_output\test_html_text.csv"
)

OCR_FILE = Path(
    r"D:\Phish360\ocr_output\test_ocr.csv"
)

METADATA_FILE = Path(
    r"D:\Phish360\metadata\phish360_metadata_split_clean.csv"
)


# ============================================================
# Check files
# ============================================================

for path in [
    CONSISTENCY_FILE,
    HTML_FILE,
    OCR_FILE,
    METADATA_FILE,
]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found:\n{path}"
        )


# ============================================================
# Load
# ============================================================

print("Loading frozen research artifacts...")

reference = pd.read_csv(
    CONSISTENCY_FILE,
    low_memory=False,
)

html = pd.read_csv(
    HTML_FILE,
    low_memory=False,
)

ocr = pd.read_csv(
    OCR_FILE,
    low_memory=False,
)

metadata = pd.read_csv(
    METADATA_FILE,
    low_memory=False,
)


# ============================================================
# Identify URL column
# ============================================================

url_candidates = [
    col
    for col in metadata.columns
    if str(col).strip().lower() in {"url"}
]

if not url_candidates:
    raise RuntimeError(
        "Could not find URL column in metadata."
    )

url_column = url_candidates[0]


# ============================================================
# Validate IDs
# ============================================================

print(f"Reference rows: {len(reference)}")
print(f"HTML rows:      {len(html)}")
print(f"OCR rows:       {len(ocr)}")
print(f"Metadata rows:  {len(metadata)}")

assert reference["sample_id"].is_unique
assert html["sample_id"].is_unique
assert ocr["sample_id"].is_unique
assert metadata["sample_id"].is_unique


# ============================================================
# Select only required columns
# ============================================================

html_small = html[
    [
        "sample_id",
        "status",
        "html_text",
        "title",
    ]
].copy()

html_small = html_small.rename(
    columns={
        "status": "html_status",
        "html_text": "html_text_runtime",
        "title": "html_title_runtime",
    }
)

ocr_small = ocr[
    [
        "sample_id",
        "status",
        "ocr_text",
    ]
].copy()

ocr_small = ocr_small.rename(
    columns={
        "status": "ocr_status",
        "ocr_text": "ocr_text_runtime",
    }
)

metadata_small = metadata[
    [
        "sample_id",
        url_column,
    ]
].copy()

metadata_small = metadata_small.rename(
    columns={
        url_column: "url",
    }
)


# ============================================================
# Merge
# ============================================================

data = reference[
    ["sample_id"] + CONSISTENCY_FEATURES
].copy()

data = data.merge(
    metadata_small,
    on="sample_id",
    how="left",
    validate="one_to_one",
)

data = data.merge(
    html_small,
    on="sample_id",
    how="left",
    validate="one_to_one",
)

data = data.merge(
    ocr_small,
    on="sample_id",
    how="left",
    validate="one_to_one",
)


if len(data) != len(reference):
    raise RuntimeError(
        "Row count changed during merge."
    )


# ============================================================
# Recompute runtime features
# ============================================================

print()
print("Recomputing runtime consistency features...")
print()

runtime_rows = []

for index, row in data.iterrows():

    html_status = str(
        row["html_status"]
    ).lower()

    ocr_status = str(
        row["ocr_status"]
    ).lower()

    html_text = (
        str(row["html_text_runtime"]).strip()
        if html_status == "ok"
        and pd.notna(row["html_text_runtime"])
        else ""
    )

    ocr_text = (
        str(row["ocr_text_runtime"]).strip()
        if ocr_status == "ok"
        and pd.notna(row["ocr_text_runtime"])
        else ""
    )

    html_title = (
        str(row["html_title_runtime"]).strip()
        if pd.notna(row["html_title_runtime"])
        else ""
    )

    features = extract_consistency_features(
        url=row["url"],
        html_text=html_text,
        html_title=html_title,
        ocr_text=ocr_text,
    )

    runtime_rows.append(features)

    if (index + 1) % 500 == 0:
        print(
            f"Processed {index + 1}/{len(data)}"
        )


runtime = pd.DataFrame(
    runtime_rows,
    columns=CONSISTENCY_FEATURES,
)


# ============================================================
# Compare
# ============================================================

reference_values = data[
    CONSISTENCY_FEATURES
].astype(float).to_numpy()

runtime_values = runtime[
    CONSISTENCY_FEATURES
].astype(float).to_numpy()


difference = np.abs(
    reference_values - runtime_values
)


max_difference = float(
    difference.max()
)

total_comparisons = difference.size

mismatch_mask = difference > 1e-12

mismatch_count = int(
    mismatch_mask.sum()
)


# ============================================================
# Report
# ============================================================

print()
print("=" * 70)
print("PhishAlign CONSISTENCY FEATURE VALIDATION")
print("=" * 70)

print(
    f"Samples tested:       {len(data)}"
)

print(
    f"Features per sample:  {len(CONSISTENCY_FEATURES)}"
)

print(
    f"Total comparisons:    {total_comparisons}"
)

print(
    f"Maximum difference:   {max_difference:.15g}"
)

print(
    f"Mismatched values:    {mismatch_count}"
)


# ============================================================
# Feature-level diagnostics
# ============================================================

if mismatch_count > 0:

    print()
    print("FEATURE-LEVEL MISMATCH SUMMARY")
    print("-" * 70)

    for i, feature in enumerate(
        CONSISTENCY_FEATURES
    ):

        feature_diff = difference[:, i]

        count = int(
            (feature_diff > 1e-12).sum()
        )

        if count > 0:

            max_diff = float(
                feature_diff.max()
            )

            print(
                f"{feature:45s}"
                f" mismatches={count:5d}"
                f" max_diff={max_diff:.15g}"
            )

else:

    print()
    print("SUCCESS")
    print("-" * 70)
    print(
        "Runtime consistency.py reproduces "
        "the frozen research features exactly."
    )


print()
print("=" * 70)


if mismatch_count != 0:
    sys.exit(1)