# PhishAlign Final Project Report

This folder contains all files, scripts, assets, and verification suites used to generate the academic project report for **PhishAlign: Cross-Modal Consistency-Based Phishing Website Detection**.

Keeping these files isolated in this directory prevents any overlap or confusion with the core project codebase (`backend/`, `extension/`, `src/`, `public/`, and `demo-phish/`).

---

## 📁 Directory Structure

```text
report/
├── build_report.py              # Main report generation engine (replicates template styles with 100% fidelity)
├── chapters_content.py          # Full academic chapters: Chapters 1 to 6
├── chapters_content_p2.py       # Full academic chapters: Chapters 7 to 10, Bibliography, Annexures A-D
├── report_content.py            # Preliminaries: Certificate, Declaration, Acknowledgments, Abstract, TOCs
├── table_data.py                # All 32 academic data tables formatted for Word
├── strict_verification_audit.py # Strict 61-test verification audit suite (0 warnings, 0 issues)
├── verify_report.py             # Terminology and media integrity validator
├── generate_diagrams_b1.py      # Architecture, DFD, and concept diagrams generator (300 DPI)
├── generate_diagrams_b2.py      # Flowcharts, offline pipeline, and latency breakdowns generator
├── generate_diagrams_b3.py      # ROC curves, confusion matrices, and SHAP plots generator
├── generate_diagram_c1.py       # Multi-stakeholder empathy map generator (Annexure C)
├── template.docx                # Departmental reference template (.docx)
├── final_project_report.docx    # Complete generated project report (~13 MB)
├── PhishAlign.docx              # Baseline reference draft document
├── diagrams/                    # 24 rendered 300-DPI high-contrast diagram PNGs
└── snapshots/                   # 24 uncropped real-world testbed & extension UI screenshots
    ├── extension screenshots/   # Chrome Extension interface & badge states
    └── web_page_screenshots/   # Legitimate and adversarial phishing testbed captures
```

---

## 🚀 Usage & Commands

All scripts are path-independent and can be executed either from the project root or from inside the `report/` folder:

### 1. Rebuild the Project Report
To regenerate `final_project_report.docx`:
```powershell
python report/build_report.py
```
*(Or `cd report; python build_report.py`)*

### 2. Run the Strict Verification Audit
To verify formatting, figure/table captions, math formulas, terminology, and media references:
```powershell
python report/strict_verification_audit.py
```
Expected output:
```text
Total Tests Passed: 61
Total Warnings:     0
Total Issues:       0
>>> STRICT DOCUMENT VERIFICATION AUDIT PASSED WITH ZERO ISSUES! <<<
```

### 3. Regenerate Architecture Diagrams (Optional)
If any diagram styling needs updating:
```powershell
python report/generate_diagrams_b1.py
python report/generate_diagrams_b2.py
python report/generate_diagrams_b3.py
python report/generate_diagram_c1.py
```
*(All generated PNGs will be saved into `report/diagrams/`)*
