#!/usr/bin/env python3
"""
build_report.py - PhishAlign Comprehensive Project Report Generator
Replicates template.docx with 100% fidelity:
- Inherits exact margins, orientations, headers/footers, styles, and font families
- Exact table styling: single 0.5pt borders, cell padding, D9E2F3 header shading, center alignment
- Modern, vibrant project diagrams (300 DPI) and curated real-world system snapshots
- Full academic report content covering all 10 chapters, preliminaries, bibliography, and annexures
- Saves output as final_project_report.docx
"""

import os
import sys

# Ensure current working directory and sys.path are set to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

import table_data as td
import report_content as rc
import chapters_content as cc1
import chapters_content_p2 as cc2

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def set_cell_margins(cell, top=50, bottom=50, left=90, right=90):
    """Sets exact cell padding matching template.docx (in dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)
    vAlign = parse_xml(f'<w:vAlign {nsdecls("w")} w:val="center"/>')
    tcPr.append(vAlign)


def render_math_text_to_p(p, text, base_font_size=12, default_color=RGBColor(0, 0, 0)):
    """
    Renders text into paragraph runs, converting mathematical symbols and
    ASCII notation (P_url, R^28, w^T, L^(t), e^(-z), y_hat_i^(t-1)) into
    proper Word runs with italic bases, subscripts, and superscripts.
    """
    token_pattern = re.compile(
        r'(?<![A-Za-z0-9])(y_hat_i\^\(t-1\))|'
        r'(?<![A-Za-z0-9])([fw])_([A-Za-z0-9]+)\^([A-Za-z0-9]+)|'
        r'(?<![A-Za-z0-9])([fw])_([A-Za-z0-9]+)\^\(([^\)]+)\)|'
        r'(?<![A-Za-z0-9])([RLwe0-9\)])\^\(([^\)]+)\)|'
        r'(?<![A-Za-z0-9])([RLwe0-9\)])\^([A-Za-z0-9]+)|'
        r'(?<![A-Za-z0-9])([PTwCghxyfφ])_([A-Za-z0-9]+)'
    )

    pos = 0
    for m in token_pattern.finditer(text):
        start, end = m.span()
        if start > pos:
            r = p.add_run(text[pos:start])
            r.font.name = "Times New Roman"
            r.font.size = Pt(base_font_size)
            r.font.color.rgb = default_color

        g = m.groups()
        if g[0]:  # y_hat_i^(t-1)
            r_base = p.add_run("ŷ")
            r_base.font.name = "Times New Roman"
            r_base.font.size = Pt(base_font_size)
            r_base.font.italic = True
            r_base.font.color.rgb = default_color
            r_sub = p.add_run("i")
            r_sub.font.name = "Times New Roman"
            r_sub.font.size = Pt(base_font_size)
            r_sub.font.subscript = True
            r_sub.font.color.rgb = default_color
            r_sup = p.add_run("(t-1)")
            r_sup.font.name = "Times New Roman"
            r_sup.font.size = Pt(base_font_size)
            r_sup.font.superscript = True
            r_sup.font.color.rgb = default_color
        elif g[1]:  # var_sub^sup (e.g. f_t^2, w_j^2)
            var, sub, sup = g[1], g[2], g[3]
            r_base = p.add_run(var)
            r_base.font.name = "Times New Roman"
            r_base.font.size = Pt(base_font_size)
            r_base.font.italic = True
            r_base.font.color.rgb = default_color
            r_sub = p.add_run(sub)
            r_sub.font.name = "Times New Roman"
            r_sub.font.size = Pt(base_font_size)
            r_sub.font.subscript = True
            r_sub.font.color.rgb = default_color
            r_sup = p.add_run(sup)
            r_sup.font.name = "Times New Roman"
            r_sup.font.size = Pt(base_font_size)
            r_sup.font.superscript = True
            r_sup.font.color.rgb = default_color
        elif g[4]:  # var_sub^(sup)
            var, sub, sup = g[4], g[5], g[6]
            r_base = p.add_run(var)
            r_base.font.name = "Times New Roman"
            r_base.font.size = Pt(base_font_size)
            r_base.font.italic = True
            r_base.font.color.rgb = default_color
            r_sub = p.add_run(sub)
            r_sub.font.name = "Times New Roman"
            r_sub.font.size = Pt(base_font_size)
            r_sub.font.subscript = True
            r_sub.font.color.rgb = default_color
            r_sup = p.add_run(sup)
            r_sup.font.name = "Times New Roman"
            r_sup.font.size = Pt(base_font_size)
            r_sup.font.superscript = True
            r_sup.font.color.rgb = default_color
        elif g[7]:  # var^(sup) (e.g. L^(t), e^(-z))
            var, sup = g[7], g[8]
            r_base = p.add_run(var)
            r_base.font.name = "Times New Roman"
            r_base.font.size = Pt(base_font_size)
            if var.isalpha():
                r_base.font.italic = True
            r_base.font.color.rgb = default_color
            r_sup = p.add_run(sup)
            r_sup.font.name = "Times New Roman"
            r_sup.font.size = Pt(base_font_size)
            r_sup.font.superscript = True
            r_sup.font.color.rgb = default_color
        elif g[9]:  # var^sup (e.g. R^28, w^T)
            var, sup = g[9], g[10]
            var_text = "ℝ" if var == "R" else var
            r_base = p.add_run(var_text)
            r_base.font.name = "Times New Roman"
            r_base.font.size = Pt(base_font_size)
            if var.isalpha() and var != "R":
                r_base.font.italic = True
            r_base.font.color.rgb = default_color
            r_sup = p.add_run(sup)
            r_sup.font.name = "Times New Roman"
            r_sup.font.size = Pt(base_font_size)
            r_sup.font.superscript = True
            r_sup.font.color.rgb = default_color
        elif g[11]:  # var_sub (e.g. P_url, x_i)
            var, sub = g[11], g[12]
            r_base = p.add_run(var)
            r_base.font.name = "Times New Roman"
            r_base.font.size = Pt(base_font_size)
            if var.isalpha():
                r_base.font.italic = True
            r_base.font.color.rgb = default_color
            r_sub = p.add_run(sub)
            r_sub.font.name = "Times New Roman"
            r_sub.font.size = Pt(base_font_size)
            r_sub.font.subscript = True
            r_sub.font.color.rgb = default_color
        pos = end

    if pos < len(text):
        r = p.add_run(text[pos:])
        r.font.name = "Times New Roman"
        r.font.size = Pt(base_font_size)
        r.font.color.rgb = default_color


def create_styled_table(doc, headers, data, col_widths=None):
    """
    Creates a table replicating template.docx table properties:
    - Center aligned
    - Borders: single sz=4 (0.5pt) color=808080
    - Header fill: D9E2F3 (soft blue)
    - Times New Roman font (10.5pt bold header, 10.0pt body)
    """
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

    # Populate Header
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        tcPr = hdr_cells[i]._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9E2F3"/>')
        tcPr.append(shd)
        set_cell_margins(hdr_cells[i], top=60, bottom=60, left=100, right=100)

        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        if p.runs:
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10.5)
            p.runs[0].font.bold = True
            p.runs[0].font.color.rgb = RGBColor(0, 0, 0)

    # Populate Data
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_data):
            set_cell_margins(row_cells[c_idx], top=50, bottom=50, left=90, right=90)
            val_str = str(val)
            lines = val_str.split("\n")
            p0 = row_cells[c_idx].paragraphs[0]
            p0.text = ""
            for l_idx, line in enumerate(lines):
                p = p0 if l_idx == 0 else row_cells[c_idx].add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(2)
                render_math_text_to_p(p, line, base_font_size=10.0, default_color=RGBColor(0x22, 0x22, 0x22))

    if col_widths:
        for row in table.rows:
            for c_idx, w in enumerate(col_widths):
                if c_idx < len(row.cells):
                    row.cells[c_idx].width = Inches(w)

    return table


def add_chapter_heading(doc, chapter_num, title):
    """Creates formal Heading 1 with page break before, centered, Times New Roman 18pt bold."""
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 1"]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.page_break_before = True
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    run = p.add_run(f"CHAPTER {chapter_num}\n{title.upper()}")
    run.font.name = "Times New Roman"
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_prelim_heading(doc, title):
    """Creates formal unnumbered prelim heading (CONTENTS, etc.)."""
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 1"]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.page_break_before = True
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(18)
    run = p.add_run(title.upper())
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_h2(doc, number_str, title):
    """Creates formal Heading 2 (e.g. 1.1 Introduction), Times New Roman 13pt bold."""
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 2"]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(f"{number_str}  {title}")
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_h3(doc, number_str, title):
    """Creates formal Heading 3 (e.g. 5.2.1 Product Perspective), Times New Roman 12pt bold."""
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 3"]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(f"{number_str}  {title}")
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_body_p(doc, text):
    """Creates justified body paragraph (or centered equation), 1.15 line spacing, Times New Roman 12pt."""
    p = doc.add_paragraph()
    p.style = doc.styles["Normal"]
    cleaned = text.strip()
    is_eqn = (
        cleaned.startswith(("L^(t)", "z = w^T", "P_phish = σ(z)", "Ω(f_t)"))
        or cleaned == "P_phish = σ(z) = 1 / (1 + e^(-z))"
    )
    if is_eqn:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)

    render_math_text_to_p(p, text, base_font_size=12, default_color=RGBColor(0, 0, 0))
    return p


def add_bullet(doc, text, bold_prefix=""):
    """Creates indented bullet item matching template style."""
    p = doc.add_paragraph()
    p.style = doc.styles["List Paragraph"]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    r_bullet = p.add_run("•  ")
    r_bullet.font.name = "Times New Roman"
    r_bullet.font.size = Pt(11.5)
    r_bullet.font.bold = True
    if bold_prefix:
        r_bold = p.add_run(bold_prefix + " ")
        r_bold.font.name = "Times New Roman"
        r_bold.font.size = Pt(11.5)
        r_bold.font.bold = True
    render_math_text_to_p(p, text, base_font_size=11.5, default_color=RGBColor(0, 0, 0))
    return p


def add_smart_bullet(doc, line):
    """Intelligently parses bullet or numbered lines, extracting bold prefixes if present."""
    line = line.strip()
    if not line:
        return
    # Strip leading bullet symbol or numbering
    if line.startswith("•"):
        line = line[1:].strip()
    elif len(line) > 2 and line[0].isdigit() and line[1] in [".", ":"] and line[2] == " ":
        line = line[3:].strip()
    elif len(line) > 3 and line[0:2].isdigit() and line[2] in [".", ":"] and line[3] == " ":
        line = line[4:].strip()

    # Check for bold prefix delimiter
    if ":" in line:
        prefix, body = line.split(":", 1)
        if len(prefix) < 55:
            add_bullet(doc, body.strip(), bold_prefix=prefix.strip() + ":")
            return
    elif " - " in line:
        prefix, body = line.split(" - ", 1)
        if len(prefix) < 55:
            add_bullet(doc, body.strip(), bold_prefix=prefix.strip() + ":")
            return

    add_bullet(doc, line)


def add_content_block(doc, text_block):
    """Handles paragraphs and bullet lists seamlessly."""
    if not text_block:
        return
    for p in text_block.split("\n\n"):
        lines = p.split("\n")
        if len(lines) > 1 and any(l.strip().startswith(("•", "1.", "2.", "3.", "4.", "5.", "6.", "7.")) for l in lines):
            for l in lines:
                if l.strip().startswith(("•", "1.", "2.", "3.", "4.", "5.", "6.", "7.")):
                    add_smart_bullet(doc, l)
                elif l.strip():
                    add_body_p(doc, l.strip())
        else:
            cleaned = p.strip()
            if cleaned.startswith(("•", "1.", "2.", "3.", "4.", "5.", "6.", "7.")):
                add_smart_bullet(doc, cleaned)
            elif cleaned:
                add_body_p(doc, cleaned)


def add_figure(doc, img_path, caption_text, width_inches=6.2):
    """Inserts centered high-DPI image followed by formal bold caption."""
    if not os.path.isfile(img_path):
        print(f"Warning: Image file not found: {img_path}")
        return None

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(3)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(12)
    run_cap = p_cap.add_run(caption_text)
    run_cap.font.name = "Times New Roman"
    run_cap.font.size = Pt(11)
    run_cap.font.bold = True
    run_cap.font.color.rgb = RGBColor(0, 0, 0)
    return p_cap


def add_table_caption(doc, caption_text):
    """Inserts formal bold table caption above table."""
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(8)
    p_cap.paragraph_format.space_after = Pt(5)
    run_cap = p_cap.add_run(caption_text)
    run_cap.font.name = "Times New Roman"
    run_cap.font.size = Pt(11)
    run_cap.font.bold = True
    run_cap.font.color.rgb = RGBColor(0, 0, 0)
    return p_cap


def add_toc_line(doc, title, page_str, is_bold=False):
    """Inserts TOC line with exact right-aligned tab stop at 8666 dxa and dot leaders."""
    p = doc.add_paragraph()
    p.style = doc.styles["Normal"]
    pPr = p._p.get_or_add_pPr()
    tabs = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:leader="dot" w:pos="8666"/></w:tabs>')
    pPr.append(tabs)
    spacing = parse_xml(f'<w:spacing {nsdecls("w")} w:before="60" w:after="30" w:line="260" w:lineRule="auto"/>')
    pPr.append(spacing)
    ind = parse_xml(f'<w:ind {nsdecls("w")} w:right="400"/>')
    pPr.append(ind)

    r1 = p.add_run(title)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11.5 if is_bold else 11.0)
    r1.font.bold = is_bold

    p.add_run("\t")

    r2 = p.add_run(str(page_str))
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(11.5 if is_bold else 11.0)
    r2.font.bold = is_bold
    return p


def build_final_report():
    print("=" * 65)
    print("   PhishAlign Comprehensive Project Report Generation Engine")
    print("=" * 65)

    print("\n[Step 1] Loading template.docx...")
    doc = docx.Document("template.docx")
    body = doc._body._element

    print(f"Loaded template with {len(doc.sections)} sections and {len(body)} XML children.")

    # Preserve section XMLs
    p20 = body[20]
    p186 = body[186]
    sect1_xml = p186.xpath(".//w:sectPr")[0].xml

    # Update Section 0: Title Page (paragraphs 0 to 19)
    print("[Step 2] Updating Section 0 Title Page...")
    doc.paragraphs[0].text = "A PROJECT REPORT ON"
    doc.paragraphs[1].text = "PHISHALIGN"
    doc.paragraphs[2].text = "CROSS-MODAL CONSISTENCY-BASED PHISHING WEBSITE DETECTION"
    doc.paragraphs[9].text = ""
    doc.paragraphs[10].text = ""
    doc.paragraphs[12].text = ""
    # Paragraph 13 has the college logo drawing - preserved!
    # Paragraph 20 has the sectPr for Section 0 - preserved!

    # Clear old children between Section 0 and body end
    print("[Step 3] Clearing legacy body elements while preserving section definitions...")
    while len(body) > 22:
        body.remove(body[21])

    # ------------------------------------------------------------
    # SECTION 1: PRELIMINARY PAGES
    # ------------------------------------------------------------
    print("[Step 4] Populating Section 1 Preliminary Pages...")

    # Certificate
    add_prelim_heading(doc, rc.CERTIFICATE_TITLE)
    add_content_block(doc, rc.CERTIFICATE_BODY)
    add_body_p(doc, "Guide                                     Head of Department                        Principal")

    # Certificate (Company / Lab)
    add_prelim_heading(doc, "CERTIFICATE (FROM INDUSTRY / LAB, IF ANY)")
    add_body_p(doc, "This is to certify that the project entitled \"PhishAlign: Cross-Modal Consistency-Based Phishing Website Detection\" has been validated using the Phish360 open cybersecurity benchmark and the dedicated local phishing simulation testbed in the Department of Computer Engineering.")

    # Declaration
    add_prelim_heading(doc, rc.DECLARATION_TITLE)
    add_content_block(doc, rc.DECLARATION_BODY)
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(14)
    p_date.paragraph_format.space_after = Pt(2)
    r_date = p_date.add_run("Date: 19th October 2026\nPlace: Pune")
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(12)

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(24)
    p_sig.paragraph_format.space_after = Pt(6)
    r_sig = p_sig.add_run("Rohit Patil (PRN: 2114110321)                  Siddhant Deshmukh (PRN: 2114110345)")
    r_sig.font.name = "Times New Roman"
    r_sig.font.size = Pt(12)
    r_sig.font.bold = True

    # Examiner's Approval Certificate
    add_prelim_heading(doc, rc.EXAMINER_APPROVAL_TITLE)
    add_content_block(doc, rc.EXAMINER_APPROVAL_BODY)

    # Acknowledgement
    add_prelim_heading(doc, rc.ACKNOWLEDGEMENT_TITLE)
    add_content_block(doc, rc.ACKNOWLEDGEMENT_BODY)

    # Abstract
    add_prelim_heading(doc, rc.ABSTRACT_TITLE)
    add_content_block(doc, rc.ABSTRACT_BODY)

    # Contents (TOC)
    add_prelim_heading(doc, "CONTENTS")
    for title, page_str, is_bold in rc.TOC_ITEMS:
        add_toc_line(doc, title, page_str, is_bold)

    # List of Figures
    add_prelim_heading(doc, "LIST OF FIGURES")
    add_toc_line(doc, "Figure No.: Title of the figure", "Page No.", is_bold=True)
    for title, page_str in rc.FIGURES_TOC:
        add_toc_line(doc, title, page_str, is_bold=False)

    # List of Tables
    add_prelim_heading(doc, "LIST OF TABLES")
    add_toc_line(doc, "Table No.: Title of the table", "Page No.", is_bold=True)
    for title, page_str in rc.TABLES_TOC:
        add_toc_line(doc, title, page_str, is_bold=False)

    # Nomenclature and Abbreviations
    add_prelim_heading(doc, "NOMENCLATURE AND ABBREVIATIONS")
    add_h2(doc, "A.", "Symbols and Notations")
    create_styled_table(doc, ["Symbol", "Meaning and Mathematical Definition"], rc.NOMENCLATURE_SYMBOLS, col_widths=[1.5, 4.5])

    add_h2(doc, "B.", "Abbreviations")
    create_styled_table(doc, ["Abbreviation", "Expanded Technical Term"], rc.NOMENCLATURE_ABBREVIATIONS, col_widths=[1.5, 4.5])

    # Finalize Section 1 break paragraph holding Section 1 sectPr
    p_break_s1 = doc.add_paragraph()
    pPr_s1 = p_break_s1._p.get_or_add_pPr()
    pPr_s1.append(parse_xml(sect1_xml))

    # ------------------------------------------------------------
    # SECTION 2: MAIN CHAPTERS, TABLES & FIGURES
    # ------------------------------------------------------------
    print("[Step 5] Populating Section 2 Body Chapters, Tables & Figures...")

    # Chapter 1
    print(" - Populating Chapter 1: Introduction...")
    add_chapter_heading(doc, 1, cc1.CH1_TITLE)
    add_h2(doc, "1.1", "Introduction")
    add_body_p(doc, cc1.CH1_P1)
    add_body_p(doc, cc1.CH1_P2)
    add_body_p(doc, cc1.CH1_P3)
    add_figure(doc, "diagrams/fig1_1_concept.png", "Figure 1.1: Conventional isolated phishing detection compared with PhishAlign cross-modal fusion", width_inches=6.2)
    add_body_p(doc, cc1.CH1_P4)
    add_figure(doc, "diagrams/fig1_2_dual_interface.png", "Figure 1.2: PhishAlign dual-client ecosystem: Browser Extension for users and Web Dashboard for analysts", width_inches=6.2)
    add_body_p(doc, cc1.CH1_P5)

    add_h2(doc, "1.2", cc1.CH1_SEC2_TITLE)
    add_content_block(doc, cc1.CH1_SEC2_P1)
    add_content_block(doc, cc1.CH1_SEC2_P2)

    add_h2(doc, "1.3", cc1.CH1_SEC3_TITLE)
    add_body_p(doc, cc1.CH1_SEC3_P1)
    add_table_caption(doc, "Table 1.1: Existing approaches to transaction and website phishing detection and their drawbacks")
    create_styled_table(doc, td.T1_1_HEADERS, td.T1_1_DATA, col_widths=[1.3, 1.6, 1.6, 1.5])

    add_h2(doc, "1.4", cc1.CH1_SEC4_TITLE)
    add_content_block(doc, cc1.CH1_SEC4_P1)

    add_h2(doc, "1.5", cc1.CH1_SEC5_TITLE)
    add_content_block(doc, cc1.CH1_SEC5_P1)

    add_h2(doc, "1.6", cc1.CH1_SEC6_TITLE)
    add_content_block(doc, cc1.CH1_SEC6_P1)

    add_h2(doc, "1.7", cc1.CH1_SEC7_TITLE)
    add_content_block(doc, cc1.CH1_SEC7_P1)

    # Chapter 2
    print(" - Populating Chapter 2: Concepts and Methods...")
    add_chapter_heading(doc, 2, cc1.CH2_TITLE)
    add_body_p(doc, cc1.CH2_P1)

    add_h2(doc, "2.1", cc1.CH2_SEC1_TITLE)
    add_content_block(doc, cc1.CH2_SEC1_P1)

    add_h2(doc, "2.2", cc1.CH2_SEC2_TITLE)
    add_content_block(doc, cc1.CH2_SEC2_P1)

    add_h2(doc, "2.3", cc1.CH2_SEC3_TITLE)
    add_content_block(doc, cc1.CH2_SEC3_P1)

    add_h2(doc, "2.4", cc1.CH2_SEC4_TITLE)
    add_content_block(doc, cc1.CH2_SEC4_P1)

    add_h2(doc, "2.5", cc1.CH2_SEC5_TITLE)
    add_content_block(doc, cc1.CH2_SEC5_P1)
    add_figure(doc, "diagrams/fig2_1_trimodal_space.png", "Figure 2.1: Tri-modality feature space and 25-dimensional cross-modal consistency vector representation", width_inches=6.2)

    add_h2(doc, "2.6", "Stacking Meta-Learning Architecture")
    add_content_block(doc, cc1.CH2_SEC6_P1)
    add_figure(doc, "diagrams/fig2_2_stacking_arch.png", "Figure 2.2: Stacking classifier architecture combining base modality probabilities and consistency vector", width_inches=6.2)

    add_h2(doc, "2.7", cc1.CH2_SEC7_TITLE)
    add_content_block(doc, cc1.CH2_SEC7_P1)

    add_h2(doc, "2.8", cc1.CH2_SEC8_TITLE)
    add_body_p(doc, cc1.CH2_SEC8_P1)
    add_table_caption(doc, "Table 2.1: Technology stack and engineering libraries utilized in PhishAlign")
    create_styled_table(doc, td.T2_1_HEADERS, td.T2_1_DATA, col_widths=[1.5, 1.4, 0.9, 2.2])

    # Chapter 3
    print(" - Populating Chapter 3: Literature Survey...")
    add_chapter_heading(doc, 3, cc1.CH3_TITLE)
    add_body_p(doc, cc1.CH3_P1)

    add_h2(doc, "3.1", cc1.CH3_SEC1_TITLE)
    add_content_block(doc, cc1.CH3_SEC1_P1)

    add_h2(doc, "3.2", cc1.CH3_SEC2_TITLE)
    add_content_block(doc, cc1.CH3_SEC2_P1)

    add_h2(doc, "3.3", cc1.CH3_SEC3_TITLE)
    add_content_block(doc, cc1.CH3_SEC3_P1)

    add_h2(doc, "3.4", cc1.CH3_SEC4_TITLE)
    add_content_block(doc, cc1.CH3_SEC4_P1)

    add_h2(doc, "3.5", cc1.CH3_SEC5_TITLE)
    add_content_block(doc, cc1.CH3_SEC5_P1)

    add_h2(doc, "3.6", cc1.CH3_SEC6_TITLE)
    add_body_p(doc, cc1.CH3_SEC6_P1)
    add_table_caption(doc, "Table 3.1: Summary of the surveyed literature on multimodal and heuristic phishing detection")
    create_styled_table(doc, td.T3_1_HEADERS, td.T3_1_DATA, col_widths=[1.2, 1.5, 1.1, 1.2, 1.0])

    add_h2(doc, "3.7", cc1.CH3_SEC7_TITLE)
    add_content_block(doc, cc1.CH3_SEC7_P1)

    # Chapter 4
    print(" - Populating Chapter 4: Project Plan...")
    add_chapter_heading(doc, 4, cc1.CH4_TITLE)
    add_body_p(doc, cc1.CH4_P1)

    add_h2(doc, "4.1", cc1.CH4_SEC1_TITLE)
    add_content_block(doc, cc1.CH4_SEC1_P1)
    add_figure(doc, "diagrams/fig4_1_dev_model.png", "Figure 4.1: Iterative and incremental engineering research methodology used for PhishAlign", width_inches=6.2)

    add_h2(doc, "4.2", cc1.CH4_SEC2_TITLE)
    add_body_p(doc, cc1.CH4_SEC2_P1)
    add_table_caption(doc, "Table 4.1: Project phases, scheduled activities, and concrete deliverables")
    create_styled_table(doc, td.T4_1_HEADERS, td.T4_1_DATA, col_widths=[0.8, 1.5, 2.2, 1.5])

    add_h2(doc, "4.3", cc1.CH4_SEC3_TITLE)
    add_body_p(doc, cc1.CH4_SEC3_P1)
    add_figure(doc, "diagrams/fig4_2_schedule.png", "Figure 4.2: PhishAlign project milestone schedule and work breakdown Gantt chart", width_inches=6.2)

    add_h2(doc, "4.4", cc1.CH4_SEC4_TITLE)
    add_content_block(doc, cc1.CH4_SEC4_P1)

    add_h2(doc, "4.5", cc1.CH4_SEC5_TITLE)
    add_body_p(doc, cc1.CH4_SEC5_P1)
    add_table_caption(doc, "Table 4.2: Identified project risks, severity ratings, and engineered mitigation strategies")
    create_styled_table(doc, td.T4_2_HEADERS, td.T4_2_DATA, col_widths=[1.3, 1.8, 1.1, 1.8])

    # Chapter 5
    print(" - Populating Chapter 5: SRS...")
    add_chapter_heading(doc, 5, cc1.CH5_TITLE)
    add_body_p(doc, cc1.CH5_P1)

    add_h2(doc, "5.1", cc1.CH5_SEC1_TITLE)
    add_body_p(doc, cc1.CH5_SEC1_P1)

    add_h2(doc, "5.2", cc1.CH5_SEC2_TITLE)
    add_content_block(doc, cc1.CH5_SEC2_P1)

    add_h2(doc, "5.3", cc1.CH5_SEC3_TITLE)
    add_body_p(doc, cc1.CH5_SEC3_P1)
    add_table_caption(doc, "Table 5.1: User classes and operational characteristics of PhishAlign")
    create_styled_table(doc, td.T5_1_HEADERS, td.T5_1_DATA, col_widths=[1.4, 1.8, 1.1, 1.7])

    add_h2(doc, "5.4", cc1.CH5_SEC4_TITLE)
    add_body_p(doc, cc1.CH5_SEC4_P1)
    add_table_caption(doc, "Table 5.2: Functional requirements specification for ingestion, modeling, and client delivery")
    create_styled_table(doc, td.T5_2_HEADERS, td.T5_2_DATA, col_widths=[0.8, 3.2, 1.0, 1.0])

    add_h2(doc, "5.5", cc1.CH5_SEC5_TITLE)
    add_body_p(doc, cc1.CH5_SEC5_P1)
    add_figure(doc, "diagrams/fig5_1_use_case.png", "Figure 5.1: Use case diagram of PhishAlign illustrating End User, SOC Analyst, and System Admin interactions", width_inches=6.2)
    add_table_caption(doc, "Table 5.3: Detailed use case specification: Submit and analyze website via web dashboard / extension")
    create_styled_table(doc, td.T5_3_HEADERS, td.T5_3_DATA, col_widths=[1.8, 4.2])

    add_h2(doc, "5.6", cc1.CH5_SEC6_TITLE)
    add_content_block(doc, cc1.CH5_SEC6_P1)

    add_h2(doc, "5.7", cc1.CH5_SEC7_TITLE)
    add_body_p(doc, cc1.CH5_SEC7_P1)
    add_table_caption(doc, "Table 5.4: Non-functional requirements specification governing latency, accuracy, and security")
    create_styled_table(doc, td.T5_4_HEADERS, td.T5_4_DATA, col_widths=[1.5, 2.0, 2.5])

    add_h2(doc, "5.8", cc1.CH5_SEC8_TITLE)
    add_body_p(doc, cc1.CH5_SEC8_P1)
    add_table_caption(doc, "Table 5.5: Minimum and recommended hardware and software development specifications")
    create_styled_table(doc, td.T5_5_HEADERS, td.T5_5_DATA, col_widths=[1.6, 2.2, 2.2])

    # Chapter 6
    print(" - Populating Chapter 6: System Design...")
    add_chapter_heading(doc, 6, cc2.CH6_TITLE)
    add_body_p(doc, cc2.CH6_P1)

    add_h2(doc, "6.1", cc2.CH6_SEC1_TITLE)
    add_body_p(doc, cc2.CH6_SEC1_P1)
    add_figure(doc, "diagrams/fig6_1_architecture.png", "Figure 6.1: PhishAlign end-to-end system architecture across ingestion, modeling, and client interfaces", width_inches=6.2)

    add_h2(doc, "6.2", cc2.CH6_SEC2_TITLE)
    add_content_block(doc, cc2.CH6_SEC2_P1)
    add_figure(doc, "diagrams/fig6_2_dual_topology.png", "Figure 6.2: Dual-interface topology: Webpage detailed analytical dashboard vs. Extension real-time guard", width_inches=6.2)

    add_h2(doc, "6.3", cc2.CH6_SEC3_TITLE)
    add_body_p(doc, cc2.CH6_SEC3_P1.split("\n\n")[0])
    add_figure(doc, "diagrams/fig6_3_dfd0.png", "Figure 6.3: Data flow diagram, Level 0 (Context diagram)", width_inches=6.2)
    add_body_p(doc, cc2.CH6_SEC3_P1.split("\n\n")[1])
    add_figure(doc, "diagrams/fig6_4_dfd1.png", "Figure 6.4: Data flow diagram, Level 1 (Decomposed processing pipeline)", width_inches=6.2)

    add_h2(doc, "6.4", cc2.CH6_SEC4_TITLE)
    add_body_p(doc, cc2.CH6_SEC4_P1)
    add_figure(doc, "diagrams/fig6_5_flowchart.png", "Figure 6.5: End-to-end scoring, consistency evaluation, and decision policy flowchart", width_inches=6.2)

    add_h2(doc, "6.5", cc2.CH6_SEC5_TITLE)
    add_body_p(doc, cc2.CH6_SEC5_P1)
    add_figure(doc, "diagrams/fig6_7_sequence.png", "Figure 6.6: UML sequence diagram for real-time website scoring and interception", width_inches=6.2)

    add_h2(doc, "6.6", cc2.CH6_SEC6_TITLE)
    add_body_p(doc, cc2.CH6_SEC6_P1.split("\n\n")[0])
    add_figure(doc, "diagrams/fig6_8_class_diagram.png", "Figure 6.7: Conceptual class diagram and component hierarchy of the backend service", width_inches=6.2)
    add_body_p(doc, cc2.CH6_SEC6_P1.split("\n\n")[1])
    add_table_caption(doc, "Table 6.1: Backend REST API input payload specifications for `/analyze` and `/analyze-content`")
    create_styled_table(doc, td.T6_1_HEADERS, td.T6_1_DATA, col_widths=[1.4, 1.0, 1.2, 1.0, 1.4])
    add_table_caption(doc, "Table 6.2: Backend REST API response payload fields, forensic types, and audience mapping")
    create_styled_table(doc, td.T6_2_HEADERS, td.T6_2_DATA, col_widths=[1.5, 1.1, 2.4, 1.0])

    add_h2(doc, "6.7", cc2.CH6_SEC7_TITLE)
    add_content_block(doc, cc2.CH6_SEC7_P1)
    add_figure(doc, "diagrams/fig6_9_feature_vector.png", "Figure 6.8: Composition of the 28-dimensional PhishAlign input feature vector", width_inches=6.2)
    add_table_caption(doc, "Table 6.3: Comprehensive inventory of the 25 Cross-Modal Consistency Features and formulas")
    create_styled_table(doc, td.T6_3_HEADERS, td.T6_3_DATA, col_widths=[0.5, 1.8, 1.1, 1.6, 1.0])

    add_h2(doc, "6.8", cc2.CH6_SEC8_TITLE)
    add_content_block(doc, cc2.CH6_SEC8_P1)

    add_h2(doc, "6.9", cc2.CH6_SEC9_TITLE)
    add_content_block(doc, cc2.CH6_SEC9_P1)
    add_figure(doc, "diagrams/fig6_6_consistency_calc.png", "Figure 6.9: Cross-modal pairwise Jaccard matrix computation and domain identity overlap analysis", width_inches=6.2)

    add_h2(doc, "6.10", cc2.CH6_SEC10_TITLE)
    add_content_block(doc, cc2.CH6_SEC10_P1)
    add_table_caption(doc, "Table 6.4: Three-tier risk classification policy, decision thresholds, and user alert interventions")
    create_styled_table(doc, td.T6_4_HEADERS, td.T6_4_DATA, col_widths=[1.2, 1.2, 1.1, 1.3, 1.2])
    add_figure(doc, "diagrams/fig6_extension_pipeline.png", "Figure 6.10: PhishAlign Browser Extension real-time multi-modal detection pipeline and NLP dynamic identity gate", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/ext_01_installed_service_worker.png", "Figure 6.11: Chrome Extension management interface displaying PhishAlign 1.0.0 MV3 Service Worker enabled", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/ext_02_scanning_overlay.png", "Figure 6.12: Chrome Extension real-time active scanning overlay banner during background page inspection", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/ext_03_safe_geeksforgeeks.png", "Figure 6.13: Chrome Extension in action: non-intrusive popup verification on legitimate site (GeeksforGeeks, 0.9% risk)", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/ext_04_safe_adobe_photoshop.png", "Figure 6.14: Chrome Extension cross-modal calibration on Adobe Photoshop (10.4% risk, overriding visual false alarm)", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/ext_05_phish_blocked_intercept.png", "Figure 6.15: Chrome Extension active defense: full-screen blocking overlay on simulated phishing page (100.0% risk)", width_inches=6.2)

    add_h2(doc, "6.11", cc2.CH6_SEC11_TITLE)
    add_body_p(doc, cc2.CH6_SEC11_P1)

    add_h2(doc, "6.12", cc2.CH6_SEC12_TITLE)
    add_content_block(doc, cc2.CH6_SEC12_P1)

    # Chapter 7
    print(" - Populating Chapter 7: Implementation...")
    add_chapter_heading(doc, 7, cc2.CH7_TITLE)
    add_body_p(doc, cc2.CH7_P1)

    add_h2(doc, "7.1", cc2.CH7_SEC1_TITLE)
    add_body_p(doc, cc2.CH7_SEC1_P1)
    add_table_caption(doc, "Table 7.1: Software development tools, frameworks, and utility libraries used in implementation")
    create_styled_table(doc, td.T7_1_HEADERS, td.T7_1_DATA, col_widths=[1.5, 1.5, 1.5, 1.5])

    add_h2(doc, "7.2", cc2.CH7_SEC2_TITLE)
    add_content_block(doc, cc2.CH7_SEC2_P1)
    add_figure(doc, "diagrams/fig6_10_offline_training.png", "Figure 7.1: Offline model development, leak-free group partitioning, and serialization pipeline", width_inches=6.2)

    add_h2(doc, "7.3", cc2.CH7_SEC3_TITLE)
    add_body_p(doc, cc2.CH7_SEC3_P1)

    add_h2(doc, "7.4", cc2.CH7_SEC4_TITLE)
    add_body_p(doc, cc2.CH7_SEC4_P1)
    add_table_caption(doc, "Table 7.2: Machine learning model hyperparameters and optimization configurations")
    create_styled_table(doc, td.T7_2_HEADERS, td.T7_2_DATA, col_widths=[1.3, 1.4, 1.1, 1.2, 1.0])

    add_h2(doc, "7.5", cc2.CH7_SEC5_TITLE)
    add_content_block(doc, cc2.CH7_SEC5_P1)

    add_h2(doc, "7.6", cc2.CH7_SEC6_TITLE)
    add_content_block(doc, cc2.CH7_SEC6_P1)

    add_h2(doc, "7.7", cc2.CH7_SEC7_TITLE)
    add_body_p(doc, cc2.CH7_SEC7_P1)

    add_h2(doc, "7.8", cc2.CH7_SEC8_TITLE)
    add_content_block(doc, cc2.CH7_SEC8_P1)
    add_table_caption(doc, "Table 7.3: Interface feature comparison: Webpage Detailed View vs. Browser Extension User View")
    create_styled_table(doc, td.T7_3_HEADERS, td.T7_3_DATA, col_widths=[1.5, 1.5, 1.5, 1.5])

    add_h2(doc, "7.9", cc2.CH7_SEC9_TITLE)
    add_body_p(doc, cc2.CH7_SEC9_P1)
    add_table_caption(doc, "Table 7.4: Technical implementation challenges encountered and engineering solutions adopted")
    create_styled_table(doc, td.T7_4_HEADERS, td.T7_4_DATA, col_widths=[1.3, 1.7, 1.4, 1.6])

    # Chapter 8
    print(" - Populating Chapter 8: Results and Discussion...")
    add_chapter_heading(doc, 8, cc2.CH8_TITLE)
    add_body_p(doc, cc2.CH8_P1)

    add_h2(doc, "8.1", cc2.CH8_SEC1_TITLE)
    add_body_p(doc, cc2.CH8_SEC1_P1)

    add_h2(doc, "8.2", cc2.CH8_SEC2_TITLE)
    add_content_block(doc, cc2.CH8_SEC2_P1)
    add_figure(doc, "diagrams/fig7_1_performance_benchmark.png", "Figure 8.1: Model performance comparison across individual modalities and fusion strategies on Phish360", width_inches=6.2)
    add_table_caption(doc, "Table 8.1: Comprehensive model performance benchmark evaluation on Phish360 test set")
    create_styled_table(doc, td.T8_1_HEADERS, td.T8_1_DATA, col_widths=[1.8, 0.8, 0.8, 0.8, 0.9, 0.9])
    add_figure(doc, "diagrams/fig8_1_roc_curves.png", "Figure 8.2: Receiver Operating Characteristic (ROC) comparative curves on official test partition", width_inches=6.2)

    add_h2(doc, "8.3", cc2.CH8_SEC3_TITLE)
    add_body_p(doc, cc2.CH8_SEC3_P1)

    add_h2(doc, "8.4", cc2.CH8_SEC4_TITLE)
    add_body_p(doc, cc2.CH8_SEC4_P1)
    add_table_caption(doc, "Table 8.2: Per-transaction execution latency breakdown across pipeline processing stages")
    create_styled_table(doc, td.T8_2_HEADERS, td.T8_2_DATA, col_widths=[2.0, 1.0, 1.0, 1.0, 1.0])
    add_figure(doc, "diagrams/fig8_2_latency_budget.png", "Figure 8.3: Per-transaction pipeline latency breakdown compared against real-time 200ms interactive budget", width_inches=6.2)

    add_h2(doc, "8.5", cc2.CH8_SEC5_TITLE)
    add_body_p(doc, cc2.CH8_SEC5_P1)
    add_table_caption(doc, "Table 8.3: Evaluation results across seven benchmark phishing and legitimate test scenarios")
    create_styled_table(doc, td.T8_3_HEADERS, td.T8_3_DATA, col_widths=[1.2, 1.3, 0.8, 0.5, 0.5, 0.5, 0.8, 0.7, 0.4])

    add_h2(doc, "8.6", cc2.CH8_SEC6_TITLE)
    add_content_block(doc, cc2.CH8_SEC6_P1)
    add_figure(doc, "snapshots/report_ready/web_00_landing.png", "Figure 8.4: PhishAlign Web Application research prototype landing page", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_00_pipeline_progress.png", "Figure 8.5: PhishAlign Web Application real-time 8-stage pipeline analysis progress view", width_inches=6.2)

    # 10 Legitimate Verification Screenshots (Wikipedia)
    add_figure(doc, "snapshots/report_ready/web_legit_01_overview.png", "Figure 8.6: Web Application Overview tab: Wikipedia legitimate verification (1.1% risk, modality breakdown)", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_legit_02_url_analysis.png", "Figure 8.7: Web Application URL Analysis tab: Lexical attributes, HTTPS validation, and entropy for Wikipedia", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_legit_03_html_analysis.png", "Figure 8.8: Web Application HTML Analysis tab: Structural metrics, form count, and external links for Wikipedia", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_legit_04_visual_analysis.png", "Figure 8.9: Web Application Visual Model inspector: MobileNetV3 visual score (72.31%) and OCR metrics", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_legit_05_visual_inspector.png", "Figure 8.10: Web Application Captured Website Analysis: Static rendered page view of Wikipedia", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_legit_06_consistency_graph.png", "Figure 8.11: Web Application Cross-Modal Text Overlap: Tri-modal Jaccard network graph for Wikipedia", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_legit_07_jaccard_matrix.png", "Figure 8.12: Web Application Text-Overlap Matrix: Pairwise 3x3 Jaccard token overlap for Wikipedia", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_legit_08_identity_signals.png", "Figure 8.13: Web Application Website Identity Signals: 100.0% Domain-to-Title lexical match for Wikipedia", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_legit_09_shap_evidence.png", "Figure 8.14: Web Application SHAP Live Analysis Evidence: Individual feature contribution breakdown for Wikipedia", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_legit_10_shap_waterfall.png", "Figure 8.15: Web Application SHAP TreeExplainer feature importance bar chart pushing score towards legitimacy", width_inches=6.2)

    # 7 Phishing Detection Screenshots (telegr.am)
    add_figure(doc, "snapshots/report_ready/web_phish_01_overview.png", "Figure 8.16: Web Application Overview tab: High Phishing Risk alert (98.2% probability) on typosquatted telegr.am", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_phish_02_url_analysis.png", "Figure 8.17: Web Application URL Analysis tab: Typosquatted domain, entropy 3.95, and suspicious token detection", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_phish_03_html_analysis.png", "Figure 8.18: Web Application HTML Analysis tab: Credential harvesting form with 1 password field and 2 external links", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_phish_04_visual_inspector.png", "Figure 8.19: Web Application Captured Website Analysis: Visual inspection of fake Telegram login form (96.7% visual probability)", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_phish_05_consistency_graph.png", "Figure 8.20: Web Application Cross-Modal Text Overlap: Asymmetry detection (HTML-OCR 70% vs URL-HTML 0%)", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_phish_06_jaccard_matrix.png", "Figure 8.21: Web Application Text-Overlap Matrix and 0.0% Domain Identity Overlap on telegr.am", width_inches=6.2)
    add_figure(doc, "snapshots/report_ready/web_phish_07_shap_waterfall.png", "Figure 8.22: Web Application SHAP TreeExplainer feature importance bar chart displaying massive phishing attribution spikes", width_inches=6.2)

    add_table_caption(doc, "Table 8.4: Unified multi-modal and cross-modal feature attribution ranking for adversarial phishing case")
    create_styled_table(doc, td.T8_4_HEADERS, td.T8_4_DATA, col_widths=[0.4, 1.6, 0.7, 0.8, 1.1, 1.4])

    add_h2(doc, "8.7", cc2.CH8_SEC7_TITLE)
    add_body_p(doc, cc2.CH8_SEC7_P1)

    # Chapter 9
    print(" - Populating Chapter 9: Software Testing...")
    add_chapter_heading(doc, 9, cc2.CH9_TITLE)
    add_body_p(doc, cc2.CH9_P1)

    add_h2(doc, "9.1", cc2.CH9_SEC1_TITLE)
    add_content_block(doc, cc2.CH9_SEC1_P1)
    add_figure(doc, "diagrams/fig9_1_testing_strategy.png", "Figure 9.1: Multi-tiered software testing and verification strategy of PhishAlign", width_inches=6.2)

    add_h2(doc, "9.2", cc2.CH9_SEC2_TITLE)
    add_body_p(doc, cc2.CH9_SEC2_P1)
    add_table_caption(doc, "Table 9.1: Unit test cases and validation results for feature extraction and consistency math")
    create_styled_table(doc, td.T9_1_HEADERS, td.T9_1_DATA, col_widths=[0.6, 1.3, 1.4, 1.4, 1.0, 0.5])

    add_h2(doc, "9.3", cc2.CH9_SEC3_TITLE)
    add_body_p(doc, cc2.CH9_SEC3_P1)
    add_table_caption(doc, "Table 9.2: Decision threshold boundary test cases for risk classification engine")
    create_styled_table(doc, td.T9_2_HEADERS, td.T9_2_DATA, col_widths=[0.8, 1.0, 1.4, 1.2, 1.2, 0.5])

    add_h2(doc, "9.4", cc2.CH9_SEC4_TITLE)
    add_body_p(doc, cc2.CH9_SEC4_P1)
    add_table_caption(doc, "Table 9.3: API endpoint integration test suite and status code verification")
    create_styled_table(doc, td.T9_3_HEADERS, td.T9_3_DATA, col_widths=[0.7, 1.2, 1.6, 0.9, 1.2, 0.5])

    add_h2(doc, "9.5", cc2.CH9_SEC5_TITLE)
    add_body_p(doc, cc2.CH9_SEC5_P1)
    add_table_caption(doc, "Table 9.4: System test results across live simulated testbed environments")
    create_styled_table(doc, td.T9_4_HEADERS, td.T9_4_DATA, col_widths=[1.3, 1.3, 1.3, 1.2, 0.6, 0.4])

    add_h2(doc, "9.6", cc2.CH9_SEC6_TITLE)
    add_body_p(doc, cc2.CH9_SEC6_P1)

    add_h2(doc, "9.7", cc2.CH9_SEC7_TITLE)
    add_body_p(doc, cc2.CH9_SEC7_P1)

    add_h2(doc, "9.8", cc2.CH9_SEC8_TITLE)
    add_body_p(doc, cc2.CH9_SEC8_P1)

    # Chapter 10
    print(" - Populating Chapter 10: Conclusion and Future Work...")
    add_chapter_heading(doc, 10, cc2.CH10_TITLE)
    add_body_p(doc, cc2.CH10_P1)

    add_h2(doc, "10.1", cc2.CH10_SEC1_TITLE)
    add_content_block(doc, cc2.CH10_SEC1_P1)

    add_h2(doc, "10.2", cc2.CH10_SEC2_TITLE)
    add_content_block(doc, cc2.CH10_SEC2_P1)

    add_h2(doc, "10.3", cc2.CH10_SEC3_TITLE)
    add_content_block(doc, cc2.CH10_SEC3_P1)
    add_figure(doc, "diagrams/fig10_1_roadmap.png", "Figure 10.1: PhishAlign future architectural enhancement and research roadmap", width_inches=6.2)

    # Bibliography
    print(" - Populating Bibliography...")
    add_prelim_heading(doc, cc2.BIBLIOGRAPHY_TITLE)
    for ref in cc2.BIBLIOGRAPHY_ENTRIES:
        p = doc.add_paragraph()
        p.style = doc.styles["Normal"]
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(ref)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10.5)

    # Annexures
    print(" - Populating Annexures A, B, C, D...")
    add_prelim_heading(doc, cc2.ANNEXURE_A_TITLE)
    add_content_block(doc, cc2.ANNEXURE_A_TEXT)
    add_table_caption(doc, "Table A.1: Publication details and target peer-reviewed IEEE conference/journal mapping")
    create_styled_table(doc, td.TA_1_HEADERS, td.TA_1_DATA, col_widths=[2.0, 4.0])

    add_prelim_heading(doc, cc2.ANNEXURE_B_TITLE)
    add_content_block(doc, cc2.ANNEXURE_B_TEXT)
    add_table_caption(doc, "Table B.1: Plagiarism screening results across Turnitin and Urkund verification suites")
    create_styled_table(doc, td.TB_1_HEADERS, td.TB_1_DATA, col_widths=[2.2, 1.3, 1.1, 1.2, 1.2])

    add_prelim_heading(doc, cc2.ANNEXURE_C_TITLE)
    add_content_block(doc, cc2.ANNEXURE_C_TEXT)
    add_figure(doc, "diagrams/fig_c1_empathy_map.png", "Figure C.1: Multi-stakeholder empathy map and user-centered solution architecture", width_inches=6.2)
    add_table_caption(doc, "Table C.1: Multi-stakeholder empathy mapping matrix and engineered feature alignment")
    create_styled_table(doc, td.TC_1_HEADERS, td.TC_1_DATA, col_widths=[1.5, 1.7, 1.8, 1.0])

    add_prelim_heading(doc, cc2.ANNEXURE_D_TITLE)
    add_content_block(doc, cc2.ANNEXURE_D_TEXT)
    add_table_caption(doc, "Table D.1: PhishAlign engineering milestone tracker and weekly progress record")
    create_styled_table(doc, td.TD_1_HEADERS, td.TD_1_DATA, col_widths=[0.8, 1.8, 0.9, 1.5, 1.0, 0.8])

    # Save final report
    out_path = "final_project_report.docx"
    print(f"\n[Step 6] Saving generated report to {out_path}...")
    doc.save(out_path)
    print(f"SUCCESS! Output report written to: {os.path.abspath(out_path)}")
    print(f"File size: {os.path.getsize(out_path):,} bytes")

    # Final verification
    doc_verify = docx.Document(out_path)
    print(f"Verification: {len(doc_verify.sections)} sections, {len(doc_verify.paragraphs)} paragraphs, {len(doc_verify.tables)} tables.")


if __name__ == "__main__":
    build_final_report()
