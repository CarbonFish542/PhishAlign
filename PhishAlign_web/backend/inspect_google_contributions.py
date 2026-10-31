import sys
sys.path.insert(0, "backend")

import numpy as np
from app.page_capture import capture_url
from app.html_model import model, FEATURE_NAMES, extract_html_features

url = "https://accounts.google.com/"
captured = capture_url(url)
features = extract_html_features(captured.html)

print("Final URL:", captured.final_url)
print("Page title:", captured.title)
print("HTML phishing probability:",
      round(float(model.predict_proba([features])[0][1]) * 100, 2), "%")

try:
    booster = model.get_booster()
    contributions = booster.predict(
        __import__("xgboost").DMatrix(
            np.asarray([features], dtype=float),
            feature_names=FEATURE_NAMES,
        ),
        pred_contribs=True,
    )[0]

    print("\nLargest feature contributions:")
    ranked = sorted(
        zip(FEATURE_NAMES + ["BIAS"], contributions),
        key=lambda item: abs(float(item[1])),
        reverse=True,
    )

    for name, value in ranked[:15]:
        print(f"{name}: {float(value):+.6f}")

except Exception as exc:
    print("Built-in contribution analysis failed:", repr(exc))
