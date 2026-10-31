import sys
sys.path.insert(0, "backend")

from app.page_capture import capture_url
from app.inference import (
    analyze_page,
    phishalign_model,
    PHISHALIGN_FEATURES,
)

scaler = phishalign_model.named_steps["scale"]
logistic = phishalign_model.named_steps["logistic"]

urls = [
    "https://accounts.google.com/",
    "https://login.microsoftonline.com/",
]

for url in urls:
    print("\n" + "=" * 65)
    print("URL:", url)

    captured = capture_url(url)
    result = analyze_page(
        url=url,
        html_bytes=captured.html,
        screenshot_bytes=captured.screenshot,
        page_title=captured.title,
        final_url=captured.final_url,
    )

    raw = result["phishalign_feature_vector"]
    scaled = scaler.transform([raw])[0]
    contributions = scaled * logistic.coef_[0]

    print("Prediction:", result["prediction"])
    print(f"PhishAlign probability: {result['phishalign_probability']:.4%}")
    print(f"Logistic intercept: {logistic.intercept_[0]:+.6f}")

    print("\nLargest per-page contributions:")
    ranked = sorted(
        zip(PHISHALIGN_FEATURES, contributions),
        key=lambda item: abs(float(item[1])),
        reverse=True,
    )

    for name, value in ranked[:12]:
        print(f"{name}: {float(value):+.6f}")

    print(f"\nSum of contributions: {sum(contributions):+.6f}")
    print(
        "Reconstructed logit:",
        f"{float(logistic.intercept_[0] + sum(contributions)):+.6f}",
    )
