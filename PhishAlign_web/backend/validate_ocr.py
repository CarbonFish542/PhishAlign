import pandas as pd
from pathlib import Path

from app.ocr import ocr_from_path


CSV_PATH = Path(r"D:\Phish360\ocr_output\test_ocr.csv")

df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

tested = 0
mismatched = 0
failed = 0
max_length_difference = 0

for _, row in df.iterrows():
    if str(row["status"]).strip().lower() != "ok":
        continue

    screenshot_path = Path(row["screenshot_path"])

    if not screenshot_path.exists():
        print("Missing:", row["sample_id"])
        failed += 1
        continue

    result = ocr_from_path(screenshot_path)

    if result["status"] != "ok":
        print("OCR failed:", row["sample_id"], result["error"])
        failed += 1
        continue

    expected = str(row["ocr_text"]).strip()
    actual = result["text"].strip()

    tested += 1

    length_difference = abs(len(expected) - len(actual))
    max_length_difference = max(max_length_difference, length_difference)

    if expected != actual:
        mismatched += 1
        if mismatched <= 5:
            print("\nMISMATCH:", row["sample_id"])
            print("Expected length:", len(expected))
            print("Actual length:  ", len(actual))
            print("Expected:", repr(expected[:300]))
            print("Actual:  ", repr(actual[:300]))


print("\n" + "=" * 60)
print("OCR VALIDATION")
print("=" * 60)
print("Reference rows:", len(df))
print("Samples tested:", tested)
print("Mismatched:", mismatched)
print("Failed:", failed)
print("Maximum length difference:", max_length_difference)

if mismatched == 0 and failed == 0:
    print("SUCCESS")
    print("Runtime OCR reproduces the frozen research OCR exactly.")
else:
    print("VALIDATION DIFFERENCES DETECTED")
