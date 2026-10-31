import json
from app.page_capture import capture_url
from app.html_model import extract_html_features, FEATURE_NAMES, model

url = "https://accounts.google.com/"
captured = capture_url(url)
html_bytes = captured.html

features = extract_html_features(html_bytes)
probability = float(model.predict_proba([features])[0][1])

print("Requested URL:", url)
print("Final URL:", captured.final_url)
print("Page title:", captured.title)
print("HTML bytes:", len(html_bytes))
print("HTML phishing probability:", round(probability * 100, 2), "%")
print("\nExtracted HTML features:")

for name, value in zip(FEATURE_NAMES, features):
    print(f"{name}: {value}")
