import sys
sys.path.insert(0, "backend")

import numpy as np
import xgboost as xgb

from app.page_capture import capture_url
from app.html_model import model, FEATURE_NAMES, extract_html_features

captured = capture_url("https://accounts.google.com/")
features = extract_html_features(captured.html)
feature_map = dict(zip(FEATURE_NAMES, features))

print("Final URL:", captured.final_url)
print("Page title:", captured.title)
print("HTML phishing probability:",
      round(float(model.predict_proba([features])[0][1]) * 100, 2), "%")

print("\nFeature values:")
for name in [
    "external_script_reference_count",
    "meta_refresh_count",
    "password_input_count",
    "suspicious_term_count",
    "html_bytes_read",
]:
    print(f"{name}: {feature_map.get(name, 'NOT FOUND')}")

try:
    matrix = xgb.DMatrix(
        np.asarray([features], dtype=float),
        feature_names=FEATURE_NAMES,
    )
    contributions = model.get_booster().predict(
        matrix, pred_contribs=True
    )[0]

    print("\nContributions from this exact capture:")
    ranked = sorted(
        zip(FEATURE_NAMES + ["BIAS"], contributions),
        key=lambda item: abs(float(item[1])),
        reverse=True,
    )
    for name, value in ranked[:15]:
        print(f"{name}: {float(value):+.6f}")

except Exception as exc:
    print("Contribution analysis failed:", repr(exc))
