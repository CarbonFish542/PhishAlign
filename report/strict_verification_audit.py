import os
import sys

# Ensure working directory is set to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import docx
import zipfile
import re
import xml.etree.ElementTree as ET

def run_strict_audit():
    print("=================================================================")
    print("       PHISHALIGN FINAL PROJECT REPORT STRICT AUDIT SUITE        ")
    print("=================================================================")

    doc = docx.Document('final_project_report.docx')
    issues = []
    warnings = []
    passes = []

    # 1. Structural Sections Check
    print("\n[Audit 1: Section Structure & Page Setup]")
    if len(doc.sections) == 3:
        passes.append("Document has exactly 3 sections (Title, Preliminary, Main Body).")
    else:
        issues.append(f"Expected 3 sections, found {len(doc.sections)}.")

    for i, sec in enumerate(doc.sections):
        top = sec.top_margin.inches
        bottom = sec.bottom_margin.inches
        left = sec.left_margin.inches
        right = sec.right_margin.inches
        print(f" Section {i}: Margins (T={top:.2f}\", B={bottom:.2f}\", L={left:.2f}\", R={right:.2f}\"), Orient={sec.orientation}")

    # 2. Paragraph and Table counts
    print("\n[Audit 2: Paragraph & Table Metrics]")
    print(f" Total Paragraphs: {len(doc.paragraphs)}")
    print(f" Total Tables: {len(doc.tables)}")

    # 3. Comprehensive Text Corpus Audit for Prohibited / Placeholder Terms
    print("\n[Audit 3: Placeholder, Outdated Terminology & Anomaly Scan]")
    full_text = []
    for p in doc.paragraphs:
        full_text.append(p.text)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                full_text.append(cell.text)
    corpus = "\n".join(full_text)

    prohibited_patterns = [
        (r'\[Insert\b', 'Placeholder [Insert...]'),
        (r'\bTODO\b', 'Unresolved TODO'),
        (r'\bFIXME\b', 'Unresolved FIXME'),
        (r'\bTBD\b', 'Unresolved TBD'),
        (r'\bXXX\b', 'Unresolved XXX'),
        (r'Lorem ipsum', 'Lorem ipsum dummy text'),
        (r'\bLightGBM\b', 'Outdated LightGBM reference (should be XGBoost)'),
        (r'\b32 features\b', 'Outdated feature count (32 -> 31)'),
        (r'\b45 features\b', 'Outdated feature count (45 -> 64)'),
        (r'\b32 URL features\b', 'Outdated 32 URL features'),
        (r'\b45 HTML features\b', 'Outdated 45 HTML features'),
        (r'\bundefined\b', 'JavaScript undefined literal in text'),
        (r'\bNaN\b', 'NaN value in text'),
    ]

    for pattern, desc in prohibited_patterns:
        matches = re.findall(pattern, corpus, flags=re.IGNORECASE if 'lorem' in pattern else 0)
        if matches:
            issues.append(f"Found prohibited term: {desc} (count: {len(matches)})")
        else:
            passes.append(f"No occurrences of {desc}.")

    # Required Architecture Ground Truth Terms
    required_terms = [
        ('XGBoost', 10),
        ('MobileNetV3', 5),
        ('31 lexical', 1),
        ('64 structural', 1),
        ('25-dimensional', 1),
        ('28-dimensional', 1),
        ('URL Asymmetry Gate', 1),
        ('Playwright Stealth', 1),
        ('Bot-Protection Wall', 1),
        ('96.34%', 1),
        ('95.84%', 1),
        ('0.9961', 1),
        ('158 ms', 1),
    ]
    for term, min_count in required_terms:
        c = corpus.count(term)
        if c >= min_count:
            passes.append(f"Required term '{term}' present ({c} times >= {min_count}).")
        else:
            issues.append(f"Required term '{term}' insufficient: found {c}, expected >= {min_count}.")

    # 4. Figures Audit: Sequence, Duplicates & Image Association
    print("\n[Audit 4: Figure Captions, Sequential Numbering & Graphics Association]")
    fig_pattern = re.compile(r'^Figure\s+([0-9A-Za-z]+)\.(\d+):\s*(.*)$')
    
    body_figures = []
    # Identify in-body figures (skip List of Figures)
    in_list_of_figures = False
    for idx, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if 'LIST OF FIGURES' in text.upper():
            in_list_of_figures = True
            continue
        if in_list_of_figures and ('CHAPTER' in text.upper() or '1. INTRODUCTION' in text.upper()):
            in_list_of_figures = False

        if not in_list_of_figures and not '\t' in text:
            m = fig_pattern.match(text)
            if m:
                chap = int(m.group(1)) if m.group(1).isdigit() else m.group(1)
                num = int(m.group(2))
                title = m.group(3)
                # Check if preceding paragraph has a graphic
                has_preceding_graphic = False
                if idx > 0:
                    prev_p = doc.paragraphs[idx - 1]
                    if 'graphic' in prev_p._element.xml:
                        has_preceding_graphic = True
                body_figures.append({
                    'index': idx,
                    'chapter': chap,
                    'num': num,
                    'tag': f"Figure {chap}.{num}",
                    'title': title,
                    'has_image': has_preceding_graphic
                })

    print(f" Identified {len(body_figures)} distinct in-body figure captions.")
    
    # Check sequential numbering within each chapter
    chap_groups = {}
    for f in body_figures:
        chap_groups.setdefault(f['chapter'], []).append(f)

    for chap, figs in sorted(chap_groups.items(), key=lambda x: (0, x[0]) if isinstance(x[0], int) else (1, str(x[0]))):
        nums = [f['num'] for f in figs]
        expected_nums = list(range(1, len(nums) + 1))
        if nums == expected_nums:
            passes.append(f"Chapter/Annexure {chap} figures strictly sequential: 1 to {len(nums)}.")
        else:
            issues.append(f"Chapter/Annexure {chap} figure sequence anomaly: found {nums}, expected {expected_nums}")

        # Check image association
        missing_images = [f['tag'] for f in figs if not f['has_image']]
        if missing_images:
            warnings.append(f"Figure(s) without immediate preceding graphic: {missing_images}")
        else:
            passes.append(f"All Chapter/Annexure {chap} figures have immediate preceding graphic elements.")

    # 5. Tables Audit: Sequence and Duplicates
    print("\n[Audit 5: Table Captions & Sequential Numbering]")
    tbl_pattern = re.compile(r'^Table\s+([0-9A-Za-z]+)\.(\d+):\s*(.*)$')
    body_tables = []
    in_list_of_tables = False
    for idx, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if 'LIST OF TABLES' in text.upper():
            in_list_of_tables = True
            continue
        if in_list_of_tables and ('LIST OF FIGURES' in text.upper() or 'CHAPTER' in text.upper()):
            in_list_of_tables = False

        if not in_list_of_tables and not '\t' in text:
            m = tbl_pattern.match(text)
            if m:
                chap = int(m.group(1)) if m.group(1).isdigit() else m.group(1)
                num = int(m.group(2))
                title = m.group(3)
                body_tables.append({
                    'index': idx,
                    'chapter': chap,
                    'num': num,
                    'tag': f"Table {chap}.{num}",
                    'title': title
                })

    print(f" Identified {len(body_tables)} distinct in-body table captions.")
    tbl_chap_groups = {}
    for t in body_tables:
        tbl_chap_groups.setdefault(t['chapter'], []).append(t)

    for chap, tbls in sorted(tbl_chap_groups.items(), key=lambda x: (0, x[0]) if isinstance(x[0], int) else (1, str(x[0]))):
        nums = [t['num'] for t in tbls]
        expected_nums = list(range(1, len(nums) + 1))
        if nums == expected_nums:
            passes.append(f"Chapter/Annexure {chap} tables strictly sequential: 1 to {len(nums)}.")
        else:
            issues.append(f"Chapter/Annexure {chap} table sequence anomaly: found {nums}, expected {expected_nums}")

    # 6. Embedded Media File Integrity & Relationships
    print("\n[Audit 6: OpenXML Media & Relationships Integrity]")
    with zipfile.ZipFile('final_project_report.docx', 'r') as z:
        rels_xml = z.read('word/_rels/document.xml.rels')
        root = ET.fromstring(rels_xml)
        doc_xml = z.read('word/document.xml')
        doc_root = ET.fromstring(doc_xml)

        # Get all r:embed IDs in document.xml
        embed_ids = set()
        for elem in doc_root.iter():
            for k, v in elem.attrib.items():
                if k.endswith('embed'):
                    embed_ids.add(v)

        rel_map = {}
        for elem in root:
            r_id = elem.attrib.get('Id')
            target = elem.attrib.get('Target')
            rel_type = elem.attrib.get('Type')
            if 'image' in rel_type:
                rel_map[r_id] = target

        media_names = set(z.namelist())
        broken_refs = []
        for r_id in embed_ids:
            if r_id in rel_map:
                target_path = 'word/' + rel_map[r_id] if not rel_map[r_id].startswith('word/') else rel_map[r_id]
                # normalize path
                target_path = os.path.normpath(target_path).replace('\\', '/')
                if target_path not in media_names:
                    broken_refs.append((r_id, target_path))
            else:
                broken_refs.append((r_id, "MISSING_IN_RELS"))

        if not broken_refs:
            passes.append(f"All {len(embed_ids)} embedded graphic r:embed references resolve to valid zip media files.")
        else:
            issues.append(f"Broken graphic references found: {broken_refs}")

    # 7. Summary
    print("\n=================================================================")
    print("                      AUDIT VERDICT SUMMARY                      ")
    print("=================================================================")
    print(f"Total Tests Passed: {len(passes)}")
    print(f"Total Warnings:     {len(warnings)}")
    print(f"Total Issues:       {len(issues)}")

    if warnings:
        print("\n--- WARNINGS ---")
        for w in warnings:
            print(f" [!] {w}")

    if issues:
        print("\n--- CRITICAL ISSUES ---")
        for iss in issues:
            print(f" [X] {iss}")
    else:
        print("\n>>> STRICT DOCUMENT VERIFICATION AUDIT PASSED WITH ZERO ISSUES! <<<")

if __name__ == '__main__':
    run_strict_audit()
