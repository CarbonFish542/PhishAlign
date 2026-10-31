import os
import sys

# Ensure working directory is set to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import docx

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('template.docx')

shapes = list(doc.inline_shapes)
print(f"Total shapes: {len(shapes)}")
for i in range(min(5, len(shapes))):
    s = shapes[i]
    print(f"Shape {i}: width={s.width.inches:.2f} in, height={s.height.inches:.2f} in")

for idx, p in enumerate(doc.paragraphs):
    if any(k in p.text for k in ['Figure 1.1', 'Figure 1.2', 'Figure 6.1']):
        print(f"Caption P[{idx}]: '{p.text}' | style={p.style.name} | align={p.alignment}")
        if idx > 0:
            prev_p = doc.paragraphs[idx-1]
            drawings = prev_p._p.xpath('.//w:drawing')
            print(f"  Prev P[{idx-1}]: text='{prev_p.text}' | drawings={len(drawings)} | align={prev_p.alignment}")
            if drawings:
                extent = drawings[0].xpath('.//wp:extent')
                if extent:
                    cx = int(extent[0].get('cx')) / 914400.0
                    cy = int(extent[0].get('cy')) / 914400.0
                    print(f"  Drawing size: {cx:.2f} in x {cy:.2f} in")

print("\n=== TABLE CAPTIONS ===")
for idx, p in enumerate(doc.paragraphs):
    if any(k in p.text for k in ['Table 1.1', 'Table 2.1', 'Table 6.1']):
        print(f"Table Caption P[{idx}]: '{p.text}' | style={p.style.name} | align={p.alignment} | space_before={p.paragraph_format.space_before.pt if p.paragraph_format.space_before else None} | space_after={p.paragraph_format.space_after.pt if p.paragraph_format.space_after else None}")
