import os
import sys

# Ensure working directory is set to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import docx
import zipfile

doc = docx.Document('final_project_report.docx')

full_text = []
for p in doc.paragraphs:
    full_text.append(p.text)
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            full_text.append(cell.text)

corpus = '\n'.join(full_text)

print('=== COMPREHENSIVE DOCUMENT VERIFICATION AUDIT ===')
print(f'Total paragraphs: {len(doc.paragraphs)}')
print(f'Total tables: {len(doc.tables)}')

checks = [
    ('LightGBM', 0),
    ('32 features', 0),
    ('45 features', 0),
    ('32 URL features', 0),
    ('45 HTML features', 0),
    ('31 Features', '>0'),
    ('64 Features', '>0'),
    ('31 lexical', '>0'),
    ('64 structural', '>0'),
    ('78%', '>0'),
    ('50%', '>0'),
    ('URL Asymmetry Gate', '>0'),
    ('Bot-Protection Wall', '>0'),
    ('Playwright Stealth', '>0'),
    ('T. Chen and C. Guestrin', '>0'),
    ('XGBoost', '>0'),
    ('Figure 6.11:', '>0'),
    ('Figure 6.12:', '>0'),
    ('Figure 6.13:', '>0'),
    ('Figure 6.14:', '>0'),
    ('Figure 6.15:', '>0'),
    ('Figure 7.1:', '>0'),
    ('Figure 8.1:', '>0'),
    ('Figure 8.4:', '>0'),
    ('Figure 8.5:', '>0'),
    ('Figure 8.6:', '>0'),
    ('Figure 8.15:', '>0'),
    ('Figure 8.16:', '>0'),
    ('Figure 8.22:', '>0'),
    ('Figure 9.1:', '>0'),
    ('Figure 10.1:', '>0'),
]

all_passed = True
for term, expected in checks:
    count = corpus.count(term)
    passed = (count == 0) if expected == 0 else (count > 0)
    status = "PASS" if passed else "FAIL"
    if not passed:
        all_passed = False
    print(f'[{status}] Term "{term}": found {count} times (Expected: {expected})')

with zipfile.ZipFile('final_project_report.docx', 'r') as z:
    media_files = [f for f in z.namelist() if f.startswith('word/media/')]
    print(f'\nTotal embedded media files: {len(media_files)}')

# Count figure caption paragraphs and graphics
figure_captions = [p.text for p in doc.paragraphs if p.text.startswith('Figure ') and ':' in p.text and not p.text.endswith('\tPage No.') and not '\t' in p.text]
graphic_paragraphs = [p for p in doc.paragraphs if 'graphic' in p._element.xml]
print(f'Total in-body figure captions: {len(figure_captions)}')
print(f'Total embedded graphic paragraphs: {len(graphic_paragraphs)}')

if all_passed and len(media_files) >= 45 and len(graphic_paragraphs) >= 47:
    print('\nALL VERIFICATION CHECKS PASSED PERFECTLY!')
else:
    print('\nSOME CHECKS FAILED!')

