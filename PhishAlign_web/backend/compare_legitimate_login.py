import sys
sys.path.insert(0, "backend")

from app.page_capture import capture_url
from app.html_model import model, FEATURE_NAMES, extract_html_features

urls = [
    "https://login.microsoftonline.com/",
]

for url in urls:
    print("\n" + "=" * 60)
    print("Input URL:", url)

    try:
        captured = capture_url(url)
        features = extract_html_features(captured.html)
        feature_map = dict(zip(FEATURE_NAMES, features))
        probability = float(model.predict_proba([features])[0][1])

        print("Final URL:", captured.final_url)
        print("Page title:", captured.title)
        print(f"HTML phishing probability: {probability:.2%}")

        for name in [
            "external_script_reference_count",
            "meta_refresh_count",
            "password_input_count",
            "suspicious_term_count",
            "form_count",
            "html_bytes_read",
        ]:
            print(f"{name}: {feature_map.get(name, 'NOT FOUND')}")

    except Exception as exc:
        print("Capture failed:", repr(exc))
