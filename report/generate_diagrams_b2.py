import os
import sys

# Ensure working directory is set to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs('diagrams', exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# High-contrast professional palette
C_BLUE = '#0d47a1'
C_TEAL = '#00838f'
C_CORAL = '#d84315'
C_GREEN = '#1b5e20'
C_RED = '#b71c1c'
C_PURPLE = '#4a148c'
C_DARK = '#212121'

# 7. Figure 5.1: Use Case Diagram
def create_fig5_1():
    fig, ax = plt.subplots(figsize=(11, 6.0), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    # Actors
    actors = [
        ('End User\n(Browser Extension)', 1.5, 6.0, C_BLUE),
        ('Security / SOC\nThreat Analyst', 1.5, 2.2, C_PURPLE),
        ('System & API\nAdministrator', 10.5, 3.8, C_DARK),
    ]
    for label, x, y, col in actors:
        ax.add_patch(plt.Circle((x, y+0.45), 0.28, color=col, fill=False, lw=2.5))
        ax.plot([x, x], [y+0.17, y-0.35], color=col, lw=2.5)
        ax.plot([x-0.3, x+0.3], [y, y], color=col, lw=2.5)
        ax.plot([x, x-0.25], [y-0.35, y-0.7], color=col, lw=2.5)
        ax.plot([x, x+0.25], [y-0.35, y-0.7], color=col, lw=2.5)
        ax.text(x, y-1.0, label, ha='center', va='top', fontsize=10.5, fontweight='bold', color=col)

    # System Boundary Box
    ax.add_patch(patches.FancyBboxPatch((3.2, 0.4), 5.8, 7.4, boxstyle="round,pad=0.2", facecolor='#fafafa', edgecolor='#90a4ae', lw=2, ls='--'))
    ax.text(6.1, 7.4, 'PhishAlign System Boundary', ha='center', va='center', fontsize=13, fontweight='bold', color='#455a64')

    # Use cases (ellipses: cx=6.1, width=4.4, height=0.95 -> left edge 3.9, right edge 8.3)
    use_cases = [
        ('Browse Web with Real-Time Guard', 6.1, 6.4, C_BLUE, '#e3f2fd'),
        ('View Non-Intrusive Safety Badge', 6.1, 5.1, C_BLUE, '#e3f2fd'),
        ('Receive Full-Screen Interception Alert', 6.1, 3.8, C_BLUE, '#e3f2fd'),
        ('Submit URL for Deep Forensic Audit', 6.1, 2.5, C_PURPLE, '#ede7f6'),
        ('Inspect Cross-Modal Consistency & SHAP', 6.1, 1.2, C_PURPLE, '#ede7f6'),
    ]
    for text, cx, cy, border, bg in use_cases:
        ellipse = patches.Ellipse((cx, cy), 4.4, 0.95, facecolor=bg, edgecolor=border, lw=2.2)
        ax.add_patch(ellipse)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)

    # Actor lines (stop cleanly outside ellipses at x=3.85 and x=8.35)
    # End User connects to UC 1, 2, 3
    ax.plot([1.9, 3.85], [5.8, 6.4], color=C_BLUE, lw=2)
    ax.plot([1.9, 3.85], [5.6, 5.1], color=C_BLUE, lw=2)
    ax.plot([1.9, 3.85], [5.4, 3.8], color=C_BLUE, lw=2)

    # Analyst connects to UC 4, 5
    ax.plot([1.9, 3.85], [2.4, 2.5], color=C_PURPLE, lw=2)
    ax.plot([1.9, 3.85], [2.2, 1.2], color=C_PURPLE, lw=2)

    # Admin connects to UC 4, 5
    ax.plot([10.1, 8.35], [3.8, 2.5], color=C_DARK, lw=2)
    ax.plot([10.1, 8.35], [3.8, 1.2], color=C_DARK, lw=2)

    plt.tight_layout()
    plt.savefig('diagrams/fig5_1_use_case.png', dpi=300, bbox_inches='tight')
    plt.close()

# 8. Figure 6.1: End-to-End System Architecture
def create_fig6_1():
    fig, ax = plt.subplots(figsize=(13.5, 6.8), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 15.2)
    ax.set_ylim(0, 10.4)
    ax.axis('off')

    # Column 1: Clients (outer x in [0.2, 3.3])
    ax.add_patch(patches.FancyBboxPatch((0.4, 5.4), 2.7, 4.2, boxstyle="round,pad=0.18", facecolor='#e0f7fa', edgecolor=C_TEAL, lw=2.5))
    ax.text(1.75, 8.9, 'Browser Extension\n(User Facing)', ha='center', va='center', fontsize=11.5, fontweight='bold', color='#006064')
    ax.text(1.75, 7.0, '• Manifest V3 Architecture\n• Background Worker\n• Fast Tab DOM Capture\n• Native Viewport Snaps\n• Threat Intercept Modal', ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_DARK)

    ax.add_patch(patches.FancyBboxPatch((0.4, 0.6), 2.7, 4.2, boxstyle="round,pad=0.18", facecolor='#fff3e0', edgecolor=C_CORAL, lw=2.5))
    ax.text(1.75, 4.1, 'Web Dashboard\n(SOC / Research)', ha='center', va='center', fontsize=11.5, fontweight='bold', color='#e65100')
    ax.text(1.75, 2.2, '• React 18 + Vite SPA\n• Modality Breakdown\n• Jaccard Heatmaps\n• Headless Playwright\n• SHAP Attribution Dossier', ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_DARK)

    # Column 2: Gateway & Ingestion (outer x in [3.8, 6.8])
    ax.add_patch(patches.FancyBboxPatch((4.0, 1.8), 2.6, 6.6, boxstyle="round,pad=0.18", facecolor='#f3e5f5', edgecolor=C_PURPLE, lw=2.5))
    ax.text(5.3, 7.8, 'FastAPI Gateway\n(/analyze, /content)', ha='center', va='center', fontsize=11.5, fontweight='bold', color='#4a148c')
    ax.text(5.3, 4.6, '• Pydantic Verification\n• Asynchronous I/O\n• Playwright Headless\n  Chromium Engine\n• Viewport Rendering\n• Tesseract OCR Engine\n  Token Extraction\n• CORS & Security SSL', ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_DARK)

    # Column 3: Tri-Modal Feature Extractors & Base Models (outer x in [7.3, 10.9])
    ax.add_patch(patches.FancyBboxPatch((7.5, 7.1), 3.2, 2.6, boxstyle="round,pad=0.18", facecolor='#e3f2fd', edgecolor=C_BLUE, lw=2.5))
    ax.text(9.1, 9.1, 'URL Engine (XGBoost)', ha='center', va='center', fontsize=11, fontweight='bold', color=C_BLUE)
    ax.text(9.1, 7.9, '31 lexical & structural features\n(entropy, dots, host tokens, length)\nOutput: P_url ∈ [0, 1]', ha='center', va='center', fontsize=9, fontweight='bold', color=C_DARK)

    ax.add_patch(patches.FancyBboxPatch((7.5, 3.8), 3.2, 2.6, boxstyle="round,pad=0.18", facecolor='#e0f2f1', edgecolor=C_TEAL, lw=2.5))
    ax.text(9.1, 5.8, 'HTML Engine (XGBoost)', ha='center', va='center', fontsize=11, fontweight='bold', color=C_TEAL)
    ax.text(9.1, 4.6, '64 DOM tree & heuristic features\n(forms, passwords, scripts, iframes)\nOutput: P_html ∈ [0, 1]', ha='center', va='center', fontsize=9, fontweight='bold', color=C_DARK)

    ax.add_patch(patches.FancyBboxPatch((7.5, 0.5), 3.2, 2.6, boxstyle="round,pad=0.18", facecolor='#fff3e0', edgecolor=C_CORAL, lw=2.5))
    ax.text(9.1, 2.5, 'Visual Engine (MobileNetV3)', ha='center', va='center', fontsize=11, fontweight='bold', color=C_CORAL)
    ax.text(9.1, 1.3, 'Deep CNN representation\nBrand cues & layout structure\nOutput: P_visual ∈ [0, 1]', ha='center', va='center', fontsize=9, fontweight='bold', color=C_DARK)

    # Column 4: Consistency Engine & Meta-Fusion (outer x in [11.5, 14.9])
    ax.add_patch(patches.FancyBboxPatch((11.7, 5.1), 3.0, 4.6, boxstyle="round,pad=0.18", facecolor='#e8f5e9', edgecolor=C_GREEN, lw=3))
    ax.text(13.2, 9.1, 'Cross-Modal Engine', ha='center', va='center', fontsize=11.5, fontweight='bold', color='#1b5e20')
    ax.text(13.2, 7.0, '25 Consistency Dims:\n• 5 Availability flags\n• 10 Pairwise text overlap\n  (Jaccard & Containment)\n• 10 Domain identity match\n  (v3 exact token overlap)\nCross-Modal Conflict Check', ha='center', va='center', fontsize=9, fontweight='bold', color=C_DARK)

    ax.add_patch(patches.FancyBboxPatch((11.7, 0.5), 3.0, 3.8, boxstyle="round,pad=0.18", facecolor='#ede7f6', edgecolor=C_PURPLE, lw=3))
    ax.text(13.2, 3.7, 'Stacking Meta-Model\n& Alignment Gate', ha='center', va='center', fontsize=11.5, fontweight='bold', color='#4a148c')
    ax.text(13.2, 1.9, 'Logistic Regression (28-D)\n+ URL Asymmetry Gate\n\nPolicy: Safe / Caution / Phish\nJSON Response with Signals', ha='center', va='center', fontsize=9, fontweight='bold', color=C_DARK)

    # Connecting Arrows in clear corridors (ZERO border penetrations)
    # Gap 1 (Col 1 to Col 2): [3.3, 3.8]
    ax.annotate('', xy=(3.75, 6.8), xytext=(3.32, 7.4), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=2.2))
    ax.annotate('', xy=(3.75, 3.5), xytext=(3.32, 2.7), arrowprops=dict(arrowstyle="->", color=C_CORAL, lw=2.2))

    # Gap 2 (Col 2 to Col 3): [6.8, 7.3]
    ax.annotate('', xy=(7.25, 8.4), xytext=(6.82, 5.8), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.2))
    ax.annotate('', xy=(7.25, 5.1), xytext=(6.82, 5.1), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=2.2))
    ax.annotate('', xy=(7.25, 1.8), xytext=(6.82, 4.4), arrowprops=dict(arrowstyle="->", color=C_CORAL, lw=2.2))

    # Gap 3 (Col 3 to Col 4): [10.9, 11.5]
    ax.annotate('', xy=(11.45, 7.6), xytext=(10.92, 8.4), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.2))
    ax.annotate('', xy=(11.45, 6.4), xytext=(10.92, 5.1), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=2.2))
    ax.annotate('', xy=(11.45, 5.4), xytext=(10.92, 1.8), arrowprops=dict(arrowstyle="->", color=C_CORAL, lw=2.2))

    # Vertical corridor Col 4: [4.5, 4.9]
    ax.annotate('', xy=(13.2, 4.52), xytext=(13.2, 4.9), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.8))

    plt.tight_layout()
    plt.savefig('diagrams/fig6_1_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()

# 9. Figure 6.2: Dual-Interface Topology
def create_fig6_2():
    fig, ax = plt.subplots(figsize=(12, 5.6), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 6.4)
    ax.axis('off')

    # Top flow: Extension (outer x in [0.35, 3.65], [4.35, 7.65], [8.35, 11.65])
    ax.add_patch(patches.FancyBboxPatch((0.5, 3.6), 3.0, 2.2, boxstyle="round,pad=0.15", facecolor='#e0f7fa', edgecolor=C_TEAL, lw=2.5))
    ax.text(2.0, 5.1, 'Browser Extension\n(User Environment)', ha='center', va='center', fontsize=11, fontweight='bold', color='#006064')
    ax.text(2.0, 4.1, '• Zero client overhead\n• Captures active DOM & tab\n• Submits to /analyze-content', ha='center', va='center', fontsize=9.2, fontweight='bold', color=C_DARK)

    ax.add_patch(patches.FancyBboxPatch((4.5, 3.6), 3.0, 2.2, boxstyle="round,pad=0.15", facecolor='#e8f5e9', edgecolor=C_GREEN, lw=2.5))
    ax.text(6.0, 5.1, 'Layer 1: Fast Path\n(Sub-160ms Execution)', ha='center', va='center', fontsize=11, fontweight='bold', color='#1b5e20')
    ax.text(6.0, 4.1, '• Bypasses server browser\n• Evaluates models directly\n• Real-time classification', ha='center', va='center', fontsize=9.2, fontweight='bold', color=C_DARK)

    ax.add_patch(patches.FancyBboxPatch((8.5, 3.6), 3.0, 2.2, boxstyle="round,pad=0.15", facecolor='#ffebee', edgecolor=C_RED, lw=2.5))
    ax.text(10.0, 5.1, 'Active Defense\n(Immediate Protection)', ha='center', va='center', fontsize=11, fontweight='bold', color=C_RED)
    ax.text(10.0, 4.1, '• Red badge or full-page block\n• Prevents credential theft\n• Clean "Go Back to Safety"', ha='center', va='center', fontsize=9.2, fontweight='bold', color=C_DARK)

    # Bottom flow: Webpage
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.5), 3.0, 2.2, boxstyle="round,pad=0.15", facecolor='#fff3e0', edgecolor=C_CORAL, lw=2.5))
    ax.text(2.0, 2.0, 'Web Dashboard\n(SOC / Researcher)', ha='center', va='center', fontsize=11, fontweight='bold', color='#e65100')
    ax.text(2.0, 1.0, '• External URL audit\n• Submits URL to /analyze\n• Multi-tab interactive UI', ha='center', va='center', fontsize=9.2, fontweight='bold', color=C_DARK)

    ax.add_patch(patches.FancyBboxPatch((4.5, 0.5), 3.0, 2.2, boxstyle="round,pad=0.15", facecolor='#f3e5f5', edgecolor=C_PURPLE, lw=2.5))
    ax.text(6.0, 2.0, 'Layer 2/3: Deep Audit\n(Headless Playwright)', ha='center', va='center', fontsize=11, fontweight='bold', color='#4a148c')
    ax.text(6.0, 1.0, '• Playwright sandbox render\n• Complete OCR extraction\n• Compute 25 consistency dims', ha='center', va='center', fontsize=9.2, fontweight='bold', color=C_DARK)

    ax.add_patch(patches.FancyBboxPatch((8.5, 0.5), 3.0, 2.2, boxstyle="round,pad=0.15", facecolor='#e3f2fd', edgecolor=C_BLUE, lw=2.5))
    ax.text(10.0, 2.0, 'Forensic Transparency\n(Explainable AI Security)', ha='center', va='center', fontsize=11, fontweight='bold', color=C_BLUE)
    ax.text(10.0, 1.0, '• Jaccard matrix heatmaps\n• Modality probabilities\n• Research benchmark mode', ha='center', va='center', fontsize=9.2, fontweight='bold', color=C_DARK)

    # Connectors cleanly in gaps [3.65, 4.35] and [7.65, 8.35]
    ax.annotate('', xy=(4.3, 4.7), xytext=(3.7, 4.7), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=2.5))
    ax.annotate('', xy=(8.3, 4.7), xytext=(7.7, 4.7), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.5))

    ax.annotate('', xy=(4.3, 1.6), xytext=(3.7, 1.6), arrowprops=dict(arrowstyle="->", color=C_CORAL, lw=2.5))
    ax.annotate('', xy=(8.3, 1.6), xytext=(7.7, 1.6), arrowprops=dict(arrowstyle="->", color=C_PURPLE, lw=2.5))

    plt.tight_layout()
    plt.savefig('diagrams/fig6_2_dual_topology.png', dpi=300, bbox_inches='tight')
    plt.close()

# 10. Figure 6.3: DFD Level 0 (Context Diagram)
def create_fig6_3():
    fig, ax = plt.subplots(figsize=(13.2, 6.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 6.8)
    ax.axis('off')

    # Entities on left (outer x in [0.5, 2.9])
    ax.add_patch(patches.Rectangle((0.5, 3.8), 2.4, 2.2, facecolor='#e3f2fd', edgecolor=C_BLUE, lw=2.5))
    ax.text(1.7, 4.9, 'End User /\nBrowser Extension', ha='center', va='center', fontsize=11, fontweight='bold', color=C_DARK)

    ax.add_patch(patches.Rectangle((0.5, 0.8), 2.4, 2.2, facecolor='#fff3e0', edgecolor=C_CORAL, lw=2.5))
    ax.text(1.7, 1.9, 'Security Analyst /\nWeb Dashboard', ha='center', va='center', fontsize=11, fontweight='bold', color=C_DARK)

    # Core Process (Circle in Center: cx=6.6, r=1.6 -> outer x in [5.0, 8.2])
    core = patches.Ellipse((6.6, 3.4), 3.2, 3.2, facecolor='#ede7f6', edgecolor=C_PURPLE, lw=3)
    ax.add_patch(core)
    ax.text(6.6, 3.8, '0.0', ha='center', va='center', fontsize=13, fontweight='bold', color=C_PURPLE)
    ax.text(6.6, 3.1, 'PhishAlign\nCore System', ha='center', va='center', fontsize=12, fontweight='bold', color=C_DARK)

    # Target Web Server Entity on Right (outer x in [10.3, 12.7])
    ax.add_patch(patches.Rectangle((10.3, 2.3), 2.4, 2.2, facecolor='#e8f5e9', edgecolor=C_GREEN, lw=2.5))
    ax.text(11.5, 3.4, 'Target Web Server\n(Investigated Site)', ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_DARK)

    # Left gap is [2.9, 5.0] (width 2.1 units), mid_x = 3.95
    ax.annotate('', xy=(4.9, 4.7), xytext=(2.95, 4.7), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.2))
    ax.text(3.95, 4.95, 'Target URL, DOM,\n& Screenshot', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_BLUE)

    ax.annotate('', xy=(2.95, 3.9), xytext=(4.9, 3.9), arrowprops=dict(arrowstyle="->", color=C_RED, lw=2.2))
    ax.text(3.95, 3.65, 'Risk Badge /\nBlock Overlay', ha='center', va='top', fontsize=8.5, fontweight='bold', color=C_RED)

    ax.annotate('', xy=(4.9, 2.1), xytext=(2.95, 2.1), arrowprops=dict(arrowstyle="->", color=C_CORAL, lw=2.2))
    ax.text(3.95, 2.35, 'URL Audit\nSubmission', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_CORAL)

    ax.annotate('', xy=(2.95, 1.3), xytext=(4.9, 1.3), arrowprops=dict(arrowstyle="->", color=C_PURPLE, lw=2.2))
    ax.text(3.95, 1.05, 'Forensic Dossier\n& SHAP Proof', ha='center', va='top', fontsize=8.5, fontweight='bold', color=C_PURPLE)

    # Right gap is [8.2, 10.3] (width 2.1 units), mid_x = 9.25
    ax.annotate('', xy=(10.25, 3.9), xytext=(8.3, 3.9), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.2))
    ax.text(9.25, 4.15, 'HTTP GET /\nPlaywright', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_GREEN)

    ax.annotate('', xy=(8.3, 2.9), xytext=(10.25, 2.9), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.2))
    ax.text(9.25, 2.65, 'HTML, CSS &\nImage Assets', ha='center', va='top', fontsize=8.5, fontweight='bold', color=C_GREEN)

    plt.tight_layout()
    plt.savefig('diagrams/fig6_3_dfd0.png', dpi=300, bbox_inches='tight')
    plt.close()

# 11. Figure 6.4: DFD Level 1 (Decomposed Architecture)
def create_fig6_4():
    fig, ax = plt.subplots(figsize=(13.0, 6.4), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Processes (Ellipses)
    # P1: center (2.0, 6.6), rx=1.3, ry=0.9 -> [0.7, 3.3]
    p1 = patches.Ellipse((2.0, 6.6), 2.6, 1.8, facecolor='#ffffff', edgecolor=C_TEAL, lw=2.5)
    ax.add_patch(p1)
    ax.text(2.0, 6.6, '1.0\nPage Ingestion\n& Capture', ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)

    # P2: center (6.5, 6.6), rx=1.3, ry=0.9 -> [5.2, 7.8]
    p2 = patches.Ellipse((6.5, 6.6), 2.6, 1.8, facecolor='#ffffff', edgecolor=C_BLUE, lw=2.5)
    ax.add_patch(p2)
    ax.text(6.5, 6.6, '2.0\nTri-Modal Feature\nExtraction', ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)

    # P3: center (6.5, 3.6), rx=1.3, ry=0.9 -> [5.2, 7.8]
    p3 = patches.Ellipse((6.5, 3.6), 2.6, 1.8, facecolor='#ffffff', edgecolor=C_GREEN, lw=2.5)
    ax.add_patch(p3)
    ax.text(6.5, 3.6, '3.0\nConsistency Matrix\nCalculation', ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)

    # P4: center (11.0, 5.1), rx=1.4, ry=1.0 -> [9.6, 12.4]
    p4 = patches.Ellipse((11.0, 5.1), 2.8, 2.0, facecolor='#ffffff', edgecolor=C_PURPLE, lw=2.5)
    ax.add_patch(p4)
    ax.text(11.0, 5.1, '4.0\nStacking Fusion &\nAlignment Gate', ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)

    # Data Stores
    stores = [
        ('D1: Trained Model Weights (.joblib, .pth)', 2.0, 3.6),
        ('D2: Public Suffix & Identity Cache', 2.0, 1.4),
        ('D3: Telemetry & Evaluation Logs', 11.0, 1.4),
    ]
    for name, x, y in stores:
        ax.plot([x-1.7, x+1.7], [y+0.4, y+0.4], color='#616161', lw=2)
        ax.plot([x-1.7, x+1.7], [y-0.4, y-0.4], color='#616161', lw=2)
        ax.plot([x-1.7, x-1.7], [y-0.4, y+0.4], color='#616161', lw=2)
        ax.text(x, y, name, ha='center', va='center', fontsize=9, fontweight='bold', color=C_DARK)

    # Connecting Arrows cleanly in gaps
    # P1 to P2: gap [3.3, 5.2] (width 1.9 units)
    ax.annotate('', xy=(5.15, 6.6), xytext=(3.35, 6.6), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2.2))
    ax.text(4.25, 6.9, 'URL / DOM /\nScreenshot', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_DARK)

    # P2 to P3: gap [5.7, 4.5] (height 1.2 units)
    ax.annotate('', xy=(6.5, 4.55), xytext=(6.5, 5.65), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2.2))
    ax.text(6.65, 5.1, 'Raw Tokens', ha='left', va='center', fontsize=8.5, fontweight='bold', color=C_DARK)

    # P2 to P4: from (7.7, 6.2) to (9.7, 5.5) - gap is 2.0 units
    ax.annotate('', xy=(9.65, 5.55), xytext=(7.75, 6.2), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.2))
    ax.text(8.7, 6.15, 'Modality Probs', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_BLUE)

    # P3 to P4: from (7.7, 4.0) to (9.7, 4.65) - gap is 2.0 units
    ax.annotate('', xy=(9.65, 4.65), xytext=(7.75, 4.0), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.2))
    ax.text(8.35, 4.40, '25 Consistency Dims', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_GREEN)

    # Dashed store connectors
    ax.annotate('', xy=(5.3, 6.0), xytext=(3.7, 4.0), arrowprops=dict(arrowstyle="->", color='#616161', lw=1.8, ls='--'))
    ax.annotate('', xy=(5.2, 3.6), xytext=(3.7, 3.6), arrowprops=dict(arrowstyle="->", color='#616161', lw=1.8, ls='--'))
    ax.annotate('', xy=(5.3, 3.1), xytext=(3.7, 1.6), arrowprops=dict(arrowstyle="->", color='#616161', lw=1.8, ls='--'))
    ax.annotate('', xy=(11.0, 1.9), xytext=(11.0, 4.05), arrowprops=dict(arrowstyle="->", color='#616161', lw=1.8, ls='--'))

    plt.tight_layout()
    plt.savefig('diagrams/fig6_4_dfd1.png', dpi=300, bbox_inches='tight')
    plt.close()

# 12. Figure 6.5: Flowchart of Scoring & Decision Policy
def create_fig6_5():
    fig, ax = plt.subplots(figsize=(11, 9.4), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 11.5)
    ax.axis('off')

    # Start: outer y in [9.9, 11.1]
    ax.add_patch(patches.FancyBboxPatch((2.5, 10.1), 6.0, 0.85, boxstyle="round,pad=0.15", facecolor='#e0f2f1', edgecolor=C_TEAL, lw=2.5))
    ax.text(5.5, 10.52, 'Start: Webpage Visited / URL Entered', ha='center', va='center', fontsize=11.5, fontweight='bold', color=C_DARK)

    # Step 1: Ingestion: outer y in [8.35, 9.65]
    ax.add_patch(patches.Rectangle((1.8, 8.4), 7.4, 1.1, facecolor='#ffffff', edgecolor='#757575', lw=2))
    ax.text(5.5, 8.95, 'Extract URL String, Raw HTML DOM & Screenshot\n(Browser Extension Direct or Playwright Capture)', ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_DARK)

    # Step 2: Tri-Modal: outer y in [6.65, 8.0]
    ax.add_patch(patches.Rectangle((1.8, 6.7), 7.4, 1.2, facecolor='#e3f2fd', edgecolor=C_BLUE, lw=2.2))
    ax.text(5.5, 7.3, 'Execute Base Classifiers in Parallel\n• URL XGBoost (31 features) -> P_url\n• HTML XGBoost (64 features) -> P_html\n• MobileNetV3 + Tesseract OCR -> P_visual & Tokens', ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)

    # Step 3: Consistency: outer y in [4.95, 6.3]
    ax.add_patch(patches.Rectangle((1.8, 5.0), 7.4, 1.2, facecolor='#e8f5e9', edgecolor=C_GREEN, lw=2.2))
    ax.text(5.5, 5.6, 'Calculate 25 Cross-Modal Consistency Dimensions\n• Pairwise Jaccard & Containment Metrics\n• Domain Identity vs HTML / OCR / Title Token Overlaps', ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)

    # Step 4: Stacking Model: outer y in [3.25, 4.6]
    ax.add_patch(patches.Rectangle((1.8, 3.3), 7.4, 1.2, facecolor='#ede7f6', edgecolor=C_PURPLE, lw=2.2))
    ax.text(5.5, 3.9, 'Stacking Meta-Classifier & URL Asymmetry Gate\n• Evaluates 28-D Vector (3 Probs + 25 Consistency Dims)\n• Calibrates Probabilities (Resolves Login Portal Paradox)', ha='center', va='center', fontsize=10, fontweight='bold', color='#4a148c')

    # Step 5: Decision Diamond: center (5.5, 1.95), w=4.8, h=1.3
    diamond = patches.Polygon([[5.5, 2.6], [7.9, 1.95], [5.5, 1.3], [3.1, 1.95]], closed=True, facecolor='#fff9c4', edgecolor='#fbc02d', lw=2.5)
    ax.add_patch(diamond)
    ax.text(5.5, 1.95, 'Risk Verdict?\n(0.50 / 0.78)', ha='center', va='center', fontsize=11, fontweight='bold', color=C_DARK)

    # Outcomes: outer y in [0.08, 0.88]
    ax.add_patch(patches.FancyBboxPatch((0.4, 0.18), 2.8, 0.65, boxstyle="round,pad=0.1", facecolor='#e8f5e9', edgecolor=C_GREEN, lw=2.5))
    ax.text(1.8, 0.50, 'Safe (<50%)\nGreen Badge Pass', ha='center', va='center', fontsize=10, fontweight='bold', color=C_GREEN)

    ax.add_patch(patches.FancyBboxPatch((4.1, 0.18), 2.8, 0.65, boxstyle="round,pad=0.1", facecolor='#fff3e0', edgecolor=C_CORAL, lw=2.5))
    ax.text(5.5, 0.50, 'Suspicious (50-77%)\nCaution Warning Badge', ha='center', va='center', fontsize=10, fontweight='bold', color=C_CORAL)

    ax.add_patch(patches.FancyBboxPatch((7.8, 0.18), 2.8, 0.65, boxstyle="round,pad=0.1", facecolor='#ffebee', edgecolor=C_RED, lw=2.5))
    ax.text(9.2, 0.50, 'Phishing (≥78%)\nFull Block Overlay', ha='center', va='center', fontsize=10, fontweight='bold', color=C_RED)

    # Vertical connectors cleanly in gaps
    ax.annotate('', xy=(5.5, 9.55), xytext=(5.5, 10.05), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))
    ax.annotate('', xy=(5.5, 7.95), xytext=(5.5, 8.35), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))
    ax.annotate('', xy=(5.5, 6.25), xytext=(5.5, 6.65), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))
    ax.annotate('', xy=(5.5, 4.55), xytext=(5.5, 4.95), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))
    ax.annotate('', xy=(5.5, 2.65), xytext=(5.5, 3.25), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))

    # Branch connectors from diamond (cleanly stop ABOVE outcome box tops at 0.90)
    ax.annotate('', xy=(1.8, 0.92), xytext=(3.3, 1.8), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.2))
    ax.annotate('', xy=(5.5, 0.92), xytext=(5.5, 1.25), arrowprops=dict(arrowstyle="->", color=C_CORAL, lw=2.2))
    ax.annotate('', xy=(9.2, 0.92), xytext=(7.7, 1.8), arrowprops=dict(arrowstyle="->", color=C_RED, lw=2.2))

    plt.tight_layout()
    plt.savefig('diagrams/fig6_5_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()

# 13. Figure 6.13: Browser Extension Architecture Pipeline
def create_fig6_extension_pipeline():
    fig, ax = plt.subplots(figsize=(12, 13), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 13.0)
    ax.axis('off')

    # Main Title
    ax.text(5.5, 12.6, 'PhishAlign Real-Time Browser Extension Architecture Pipeline', ha='center', va='center', fontsize=14, fontweight='bold', color=C_DARK)
    ax.text(5.5, 12.25, 'Multi-Modal Feature Extraction, Stacking Meta-Learner & URL Asymmetry Gate', ha='center', va='center', fontsize=11, color='#546e7a')

    # Box 1: Live Webpage: outer y in [10.95, 12.05]
    ax.add_patch(patches.FancyBboxPatch((2.5, 11.1), 6.0, 0.8, boxstyle="round,pad=0.15", facecolor='#1a237e', edgecolor=C_DARK, lw=2))
    ax.text(5.5, 11.5, 'LIVE WEBPAGE (Active Tab Navigation)', ha='center', va='center', fontsize=12, fontweight='bold', color='#ffffff')

    # Ingestion Stream boxes (3 columns: outer y in [9.4, 10.3])
    inputs = [
        ('[URL STRING]', 2.0, 9.85, C_BLUE, '#e3f2fd'),
        ('[RAW HTML DOM]', 5.5, 9.85, C_TEAL, '#e0f2f1'),
        ('[SCREENSHOT PNG]', 9.0, 9.85, C_CORAL, '#fff3e0'),
    ]
    for label, x, y, col, bg in inputs:
        ax.add_patch(patches.FancyBboxPatch((x-1.3, y-0.35), 2.6, 0.7, boxstyle="round,pad=0.12", facecolor=bg, edgecolor=col, lw=2))
        ax.text(x, y, label, ha='center', va='center', fontsize=11, fontweight='bold', color=C_DARK)

    # Arrows from Live Webpage to 3 inputs: gap [10.35, 10.9]
    ax.annotate('', xy=(2.0, 10.35), xytext=(3.8, 10.95), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))
    ax.annotate('', xy=(5.5, 10.35), xytext=(5.5, 10.95), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))
    ax.annotate('', xy=(9.0, 10.35), xytext=(7.2, 10.95), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))

    # Base Models (3 columns: outer y in [7.35, 8.85])
    models = [
        ('MODEL 1: XGBoost\nLexical URL Model\n(31 tabular features)', 2.0, 8.1, C_BLUE, '#e3f2fd'),
        ('MODEL 2: XGBoost\nDOM Structure Model\n(64 syntactic features)', 5.5, 8.1, C_TEAL, '#e0f2f1'),
        ('MODEL 3: MobileNetV3\nComputer Vision CNN\n(224×224 RGB image)', 9.0, 8.1, C_CORAL, '#fff3e0'),
    ]
    for label, x, y, col, bg in models:
        ax.add_patch(patches.FancyBboxPatch((x-1.4, y-0.65), 2.8, 1.3, boxstyle="round,pad=0.12", facecolor=bg, edgecolor=col, lw=2.2))
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)

    # Arrows to models: gap [8.9, 9.35]
    for x, col in [(2.0, C_BLUE), (5.5, C_TEAL), (9.0, C_CORAL)]:
        ax.annotate('', xy=(x, 8.9), xytext=(x, 9.35), arrowprops=dict(arrowstyle="->", color=col, lw=2.2))

    # Combined Representation Box: outer y in [5.7, 6.9]
    ax.add_patch(patches.FancyBboxPatch((1.0, 5.85), 9.0, 1.05, boxstyle="round,pad=0.15", facecolor='#f5f5f5', edgecolor='#757575', lw=2.2))
    ax.text(5.5, 6.55, 'Three Modality Probabilities: [url_prob, html_prob, visual_prob]', ha='center', va='center', fontsize=11, fontweight='bold', color=C_DARK)
    ax.text(5.5, 6.1, '+ 25 Cross-Modal Consistency Features (Jaccard Overlap, Containment, Identity Tokens)', ha='center', va='center', fontsize=10, fontweight='bold', color='#0288d1')

    # Arrows from models to combined representation: gap [6.95, 7.3]
    ax.annotate('', xy=(3.0, 6.95), xytext=(2.0, 7.3), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2))
    ax.annotate('', xy=(5.5, 6.95), xytext=(5.5, 7.3), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=2))
    ax.annotate('', xy=(8.0, 6.95), xytext=(9.0, 7.3), arrowprops=dict(arrowstyle="->", color=C_CORAL, lw=2))

    # Box 4: Stacking Meta-Learner: outer y in [4.3, 5.35]
    ax.add_patch(patches.FancyBboxPatch((1.5, 4.45), 8.0, 0.9, boxstyle="round,pad=0.15", facecolor='#ede7f6', edgecolor=C_PURPLE, lw=2.5))
    ax.text(5.5, 5.0, 'MODEL 4: PhishAlign Stacking Meta-Learner', ha='center', va='center', fontsize=11.5, fontweight='bold', color='#4a148c')
    ax.text(5.5, 4.65, '(phishalign_stacking.joblib — Regularized Logistic Regression on 28-D Vector)', ha='center', va='center', fontsize=10, color='#6a1b9a')

    # Arrow to Meta-Learner: gap [5.4, 5.7]
    ax.annotate('', xy=(5.5, 5.4), xytext=(5.5, 5.7), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2.5))

    # Raw Fusion Score Pill: outer y in [3.15, 3.85]
    ax.add_patch(patches.FancyBboxPatch((3.0, 3.25), 5.0, 0.6, boxstyle="round,pad=0.12", facecolor='#fff9c4', edgecolor='#fbc02d', lw=2))
    ax.text(5.5, 3.55, 'Raw ML Fusion Threat Probability (e.g., 96.4%)', ha='center', va='center', fontsize=10.5, fontweight='bold', color='#f57f17')

    # Arrow from Meta to Pill: gap [3.9, 4.3]
    ax.annotate('', xy=(5.5, 3.9), xytext=(5.5, 4.3), arrowprops=dict(arrowstyle="->", color=C_PURPLE, lw=2.5))

    # Box 5: NLP Dynamic Identity Gate: outer y in [1.4, 2.75]
    ax.add_patch(patches.FancyBboxPatch((0.8, 1.55), 9.4, 1.2, boxstyle="round,pad=0.15", facecolor='#e0f2f1', edgecolor=C_TEAL, lw=2.5))
    ax.text(5.5, 2.45, 'NLP Dynamic Identity & URL Asymmetry Gate', ha='center', va='center', fontsize=11.5, fontweight='bold', color='#004d40')
    ax.text(5.5, 1.95, '• Identity Verification: Does claimed visual/HTML brand match registered domain? (telegr.am vs Telegram)\n• URL Asymmetry Gate: If genuine brand + P_url < 0.25, damp legitimate login forms below 0.35 (Safe)\n• Hostile Escalation: If webhook exfiltration or spoof on untrusted tunnel/free host, force P ≥ 0.95 (Block)', ha='center', va='center', fontsize=9.2, fontweight='bold', color=C_DARK)

    # Arrow from Pill to Gate: gap [2.8, 3.15]
    ax.annotate('', xy=(5.5, 2.8), xytext=(5.5, 3.15), arrowprops=dict(arrowstyle="->", color='#f57f17', lw=2.5))

    # Outcomes: outer y in [0.15, 0.95]
    outcomes = [
        ('SAFE TIER (P < 50%)\nNon-intrusive green badge', 2.0, 0.55, C_GREEN, '#e8f5e9'),
        ('CAUTION (50% - 77%)\nYellow warning advisory', 5.5, 0.55, C_CORAL, '#fff3e0'),
        ('PHISHING (P ≥ 78%)\nFull-screen blocking modal', 9.0, 0.55, C_RED, '#ffebee'),
    ]
    for label, x, y, col, bg in outcomes:
        ax.add_patch(patches.FancyBboxPatch((x-1.4, y-0.35), 2.8, 0.7, boxstyle="round,pad=0.12", facecolor=bg, edgecolor=col, lw=2.5))
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color=col)

    # Arrows to Outcomes: gap [1.0, 1.4]
    ax.annotate('', xy=(2.0, 0.98), xytext=(4.0, 1.38), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.5))
    ax.annotate('', xy=(5.5, 0.98), xytext=(5.5, 1.38), arrowprops=dict(arrowstyle="->", color=C_CORAL, lw=2.5))
    ax.annotate('', xy=(9.0, 0.98), xytext=(7.0, 1.38), arrowprops=dict(arrowstyle="->", color=C_RED, lw=2.5))

    plt.tight_layout()
    plt.savefig('diagrams/fig6_extension_pipeline.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_fig5_1()
    create_fig6_1()
    create_fig6_2()
    create_fig6_3()
    create_fig6_4()
    create_fig6_5()
    create_fig6_extension_pipeline()
    print("Batch 2 diagrams (including extension pipeline) generated successfully!")
