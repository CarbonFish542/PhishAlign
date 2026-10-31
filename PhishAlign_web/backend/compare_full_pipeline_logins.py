import sys
sys.path.insert(0, "backend")

from app.page_capture import capture_url
from app.inference import analyze_page

urls = [
    "https://accounts.google.com/",
    "https://login.microsoftonline.com/",
]

for url in urls:
    print("\n" + "=" * 70)
    print("Requested URL:", url)

    try:
        captured = capture_url(url)

        result = analyze_page(
            url=url,
            html_bytes=captured.html,
            screenshot_bytes=captured.screenshot,
            page_title=captured.title,
            final_url=captured.final_url,
        )

        print("Final URL:", result["final_url"])
        print("Page title:", captured.title)

        for key in [
            "url_probability",
            "html_probability",
            "visual_probability",
            "equal_weight_probability",
            "probability_only_probability",
            "phishalign_probability",
        ]:
            print(f"{key}: {result[key]:.4%}")

        print("Prediction:", result["prediction"])
        print("Threshold:", result["threshold"])

        print("\nConsistency features:")
        for key, value in result["consistency_features"].items():
            print(f"  {key}: {value}")

    except Exception as exc:
        print("ANALYSIS FAILED:", repr(exc))
