from app.consistency import (
    CONSISTENCY_FEATURES,
    extract_consistency_features,
    consistency_vector,
)


features = extract_consistency_features(
    url="https://www.microsoft.com/login",
    html_text="""
        Microsoft Account
        Sign in to your Microsoft account
        Enter your password
    """,
    html_title="Microsoft Account Sign In",
    ocr_text="""
        Microsoft
        Sign in
        Enter your password
    """,
)

print("Feature count:", len(features))
print()

for name, value in features.items():
    print(f"{name:45s} {value}")

print()
print("Vector length:", len(consistency_vector(
    "https://www.microsoft.com/login",
    "Microsoft Account Sign in to your Microsoft account",
    "Microsoft Account Sign In",
    "Microsoft Sign in",
)))