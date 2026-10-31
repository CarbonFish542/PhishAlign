import os
import sys
import glob
from PIL import Image

# Ensure working directory is set to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=== Extension Screenshots ===")
for p in glob.glob("snapshots/extension screenshots/*.*"):
    im = Image.open(p)
    print(p, im.size)

print("\n=== Web Page Screenshots (Root) ===")
for p in glob.glob("snapshots/web_page_screenshots/*.*"):
    im = Image.open(p)
    print(p, im.size)

print("\n=== Legitimate Web Page Screenshots ===")
for p in glob.glob("snapshots/web_page_screenshots/legitimate/*.*")[:5]:
    im = Image.open(p)
    print(p, im.size)

print("\n=== Phishing Web Page Screenshots ===")
for p in glob.glob("snapshots/web_page_screenshots/phishing/*.*")[:5]:
    im = Image.open(p)
    print(p, im.size)
