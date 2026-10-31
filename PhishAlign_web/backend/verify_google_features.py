import sys
sys.path.insert(0, "backend")

from app.page_capture import capture_url
from app.html_model import extract_html_features, FEATURE_NAMES

captured = capture_url("https://accounts.google.com/")
features = extract_html_features(captured.html)
feature_map = dict(zip(FEATURE_NAMES, features))

print("Final URL:", captured.final_url)
print("Page title:", captured.title)

for name in [
    "external_script_reference_count",
    "meta_refresh_count",
    "password_input_count",
    "suspicious_term_count",
    "html_bytes_read",
]:
    print(f"{name}: {feature_map.get(name, 'NOT FOUND')}")
