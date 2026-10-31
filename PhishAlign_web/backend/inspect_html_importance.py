import json
from pathlib import Path
from app.html_model import model, FEATURE_NAMES

if not hasattr(model, "feature_importances_"):
    print("This model does not expose feature_importances_.")
else:
    importances = model.feature_importances_
    ranked = sorted(
        zip(FEATURE_NAMES, importances),
        key=lambda item: item[1],
        reverse=True,
    )

    print("Top 15 HTML model features:")
    for name, importance in ranked[:15]:
        print(f"{name}: {importance:.6f}")

    print("\nFeatures of interest:")
    for target in (
        "at_symbol_count",
        "base64_marker_count",
        "suspicious_term_count",
        "hidden_input_count",
        "password_input_count",
        "meta_refresh_count",
        "inline_script_count",
    ):
        for name, importance in ranked:
            if name == target:
                print(f"{name}: {importance:.6f}")
                break
