from pathlib import Path
import sys

sys.path.insert(0, r"D:\Phish360\scripts")

from html_baseline import extract_html_features as frozen_extract
from app.html_model import (
    extract_html_features_from_path as runtime_extract,
    FEATURE_NAMES,
)


TEST_DIR = Path(r"D:\Phish360\test")
MAX_SAMPLES = 100


print("=" * 70)
print("HTML RUNTIME BATCH VALIDATION")
print("=" * 70)


# Find actual dataset HTML files, excluding anything outside
# the sample directories.
html_files = sorted(
    TEST_DIR.glob("*/RAW-HTML/index.html")
)

if not html_files:
    raise RuntimeError(
        f"No HTML files found under {TEST_DIR}"
    )

html_files = html_files[:MAX_SAMPLES]

print(f"HTML files found: {len(html_files)}")
print(f"Testing samples:  {len(html_files)}")
print(f"Features/sample:  {len(FEATURE_NAMES)}")


total_comparisons = 0
total_mismatches = 0
max_difference = 0.0
failed_samples = []


for index, html_path in enumerate(html_files, start=1):

    frozen = frozen_extract(html_path)
    runtime = runtime_extract(html_path)

    if frozen is None:
        failed_samples.append(
            (html_path.name, "Frozen extractor returned None")
        )
        continue

    if runtime is None:
        failed_samples.append(
            (html_path.name, "Runtime extractor returned None")
        )
        continue

    for feature_index, feature_name in enumerate(FEATURE_NAMES):

        frozen_value = frozen[feature_name]
        runtime_value = runtime[feature_index]

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

        total_comparisons += 1

        if difference > max_difference:
            max_difference = difference

        if difference > 1e-12:
            total_mismatches += 1

            if len(failed_samples) < 20:
                failed_samples.append(
                    (
                        str(html_path),
                        f"{feature_name}: "
                        f"frozen={frozen_value}, "
                        f"runtime={runtime_value}, "
                        f"difference={difference}"
                    )
                )

    if index % 10 == 0 or index == len(html_files):
        print(
            f"Processed {index}/{len(html_files)}"
        )


print()
print("=" * 70)
print("RESULT")
print("=" * 70)

print(f"Samples tested:       {len(html_files)}")
print(f"Features per sample:  {len(FEATURE_NAMES)}")
print(f"Total comparisons:    {total_comparisons}")
print(f"Maximum difference:   {max_difference}")
print(f"Mismatched values:    {total_mismatches}")
print(f"Failed samples:       {len(failed_samples)}")


if failed_samples:

    print()
    print("FAILURES / MISMATCHES")
    print("-" * 70)

    for sample, reason in failed_samples:
        print(f"{sample}: {reason}")


if total_mismatches == 0 and not failed_samples:

    print()
    print("SUCCESS")
    print(
        "Runtime HTML extractor reproduces the frozen "
        "research features exactly across the batch."
    )

else:

    raise SystemExit(
        "FAIL: HTML runtime validation detected differences."
    )