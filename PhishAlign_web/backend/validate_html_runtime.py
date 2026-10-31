from pathlib import Path
import sys

# Allow importing the frozen research script
sys.path.insert(0, r"D:\Phish360\scripts")

from html_baseline import extract_html_features as frozen_extract
from app.html_model import (
    extract_html_features_from_path as runtime_extract,
    FEATURE_NAMES,
)


HTML_PATH = Path(
    r"D:\Phish360\test\L00001_legitimate\RAW-HTML\index.html"
)


print("=" * 70)
print("HTML RUNTIME FEATURE VALIDATION")
print("=" * 70)

print(f"HTML file: {HTML_PATH}")
print(f"Exists:    {HTML_PATH.is_file()}")

if not HTML_PATH.is_file():
    raise FileNotFoundError(HTML_PATH)


# ------------------------------------------------------------
# Frozen research extractor
# ------------------------------------------------------------

frozen = frozen_extract(HTML_PATH)

if frozen is None:
    raise RuntimeError(
        "Frozen research extractor returned None."
    )


# ------------------------------------------------------------
# Application extractor
# ------------------------------------------------------------

runtime = runtime_extract(HTML_PATH)

if runtime is None:
    raise RuntimeError(
        "Runtime extractor returned None."
    )


# ------------------------------------------------------------
# Basic checks
# ------------------------------------------------------------

print()
print(f"Frozen feature count:  {len(frozen)}")
print(f"Runtime feature count: {len(runtime)}")
print(f"Expected feature count: {len(FEATURE_NAMES)}")


if len(frozen) != len(FEATURE_NAMES):
    raise RuntimeError(
        f"Frozen extractor returned {len(frozen)} features."
    )

if len(runtime) != len(FEATURE_NAMES):
    raise RuntimeError(
        f"Runtime extractor returned {len(runtime)} features."
    )


# ------------------------------------------------------------
# Feature-by-feature comparison
# ------------------------------------------------------------

mismatches = []
max_difference = 0.0

for i, name in enumerate(FEATURE_NAMES):

    # Frozen research extractor returns a dictionary.
    frozen_value = frozen[name]

    # Runtime extractor returns values in FEATURE_NAMES order.
    runtime_value = runtime[i]

    try:
        difference = abs(
            float(frozen_value) -
            float(runtime_value)
        )
    except (TypeError, ValueError):
        difference = (
            0.0
            if frozen_value == runtime_value
            else float("inf")
        )

    max_difference = max(
        max_difference,
        difference
    )

    if difference > 1e-12:
        mismatches.append(
            {
                "index": i,
                "feature": name,
                "frozen": frozen_value,
                "runtime": runtime_value,
                "difference": difference,
            }
        )
# ------------------------------------------------------------
# Results
# ------------------------------------------------------------

print()
print("=" * 70)
print("RESULT")
print("=" * 70)

print(f"Features compared: {len(FEATURE_NAMES)}")
print(f"Maximum difference: {max_difference}")
print(f"Mismatched features: {len(mismatches)}")


if mismatches:

    print()
    print("MISMATCH DETAILS")
    print("-" * 70)

    for item in mismatches:
        print(
            f"[{item['index']:02d}] "
            f"{item['feature']}: "
            f"frozen={item['frozen']} "
            f"runtime={item['runtime']} "
            f"diff={item['difference']}"
        )

    raise SystemExit(
        "FAIL: Runtime HTML extractor does not exactly "
        "match the frozen research extractor."
    )


print()
print("SUCCESS")
print(
    "Runtime HTML extractor reproduces the frozen "
    "research features exactly."
)