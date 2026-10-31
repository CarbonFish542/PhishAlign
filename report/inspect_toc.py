import os
import sys

# Ensure working directory is set to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import docx

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('template.docx')

recording = False
for i, p in enumerate(doc.paragraphs):
    if 'CONTENTS' in p.text:
        recording = True
    if 'NOMENCLATURE AND ABBREVIATIONS' in p.text and recording:
        print(f"[{i}] {p.text}")
        recording = False
        break
    if recording:
        print(f"[{i}] {p.text}")
