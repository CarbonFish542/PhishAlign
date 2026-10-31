import os
import sys
import glob
from PIL import Image

# Ensure working directory is set to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def analyze_folder(folder):
    files = glob.glob(os.path.join(folder, "*.png"))
    print(f"\n--- {folder} ({len(files)} files) ---")
    for f in sorted(files):
        im = Image.open(f)
        print(f"{os.path.basename(f)}: size={im.size}")

analyze_folder("snapshots/web_page_screenshots")
analyze_folder("snapshots/web_page_screenshots/legitimate")
analyze_folder("snapshots/web_page_screenshots/phishing")
analyze_folder("snapshots/extension screenshots")
