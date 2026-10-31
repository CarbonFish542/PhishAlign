import sys
import math
sys.path.insert(0, "backend")

import numpy as np
import xgboost as xgb

from app.page_capture import capture_url
from app.html_model import model, FEATURE_NAMES, extract_html_features

captured = capture_url("https://accounts.google.com/")
features = extract_html_features(captured.html)

matrix = xgb.DMatrix(
    np.asarray([features], dtype=float),
    feature_names=FEATURE_NAMES,
)

probability = float(model.predict_proba([features])[0][1])
booster = model.get_booster()

margin = float(booster.predict(matrix, output_margin=True)[0])
contributions = booster.predict(matrix, pred_contribs=True)[0]
contribution_sum = float(np.sum(contributions))
margin_probability = 1.0 / (1.0 + math.exp(-margin))

print("Final URL:", captured.final_url)
print("Page title:", captured.title)
print(f"predict_proba:             {probability:.8f}")
print(f"Sigmoid(raw margin):       {margin_probability:.8f}")
print(f"Raw margin:                {margin:.8f}")
print(f"Sum of contributions:      {contribution_sum:.8f}")
print(f"Margin minus contribution sum: {margin - contribution_sum:.10f}")

print("\nLargest contributions:")
ranked = sorted(
    zip(FEATURE_NAMES + ["BIAS"], contributions),
    key=lambda item: abs(float(item[1])),
    reverse=True,
)
for name, value in ranked[:10]:
    print(f"{name}: {float(value):+.6f}")
