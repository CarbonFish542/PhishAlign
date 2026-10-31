import os
import sys

# Ensure working directory is set to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import docx

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('template.docx')

print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")

for i, p in enumerate(doc.paragraphs):
    has_page_brk = '<w:br w:type="page"/>' in p._p.xml or '<w:pageBreakBefore/>' in p._p.xml
    is_heading1 = p.style.name == 'Heading 1'
    if has_page_brk or is_heading1 or i in [21, 121, 153, 181]:
        print(f"P[{i}]: style={p.style.name}, page_brk={has_page_brk}, text={repr(p.text[:60])}")
