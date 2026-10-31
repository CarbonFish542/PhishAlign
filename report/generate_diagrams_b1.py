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
C_BORDER = '#9e9e9e'

# 1. Figure 1.1: Conventional Phishing Detection vs PhishAlign Cross-Modal Fusion
def create_fig1_1():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    
    # Left: Conventional
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('Conventional Multimodal Approaches\n(Isolated Modality Silos)', fontsize=13, fontweight='bold', color=C_DARK, pad=12)
    
    boxes1 = [
        ('URL Features\n(Lexical & Hostname)', 1.9, 7.5, '#e3f2fd', C_BLUE),
        ('HTML Features\n(DOM Structure & Tags)', 1.9, 5.0, '#e0f2f1', C_TEAL),
        ('Visual Features\n(Screenshot & Logos)', 1.9, 2.5, '#fff3e0', C_CORAL),
    ]
    for text, x, y, bg, border in boxes1:
        # width 3.2, pad 0.15 -> right edge is 1.9 + 1.6 + 0.15 = 3.65
        ax1.add_patch(patches.FancyBboxPatch((x-1.6, y-0.85), 3.2, 1.7, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, lw=2.2))
        ax1.text(x, y, text, ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_DARK)
        # target box left edge is 6.1 - 0.2 = 5.9
        ax1.annotate('', xy=(5.8, 5.0), xytext=(3.75, y), arrowprops=dict(arrowstyle="->", color=border, lw=2.2))
        
    ax1.add_patch(patches.FancyBboxPatch((6.1, 3.6), 3.6, 2.8, boxstyle="round,pad=0.2", facecolor='#f5f5f5', edgecolor='#757575', lw=2.2))
    ax1.text(7.9, 5.0, 'Late Concatenation /\nSimple Averaging\n\n(No Cross-Modality Links;\nFails on Brand Spoofing)', ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_DARK)
    
    # Right: PhishAlign
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('PhishAlign Proposed Methodology\n(Explicit Cross-Modal Consistency)', fontsize=13, fontweight='bold', color=C_BLUE, pad=12)
    
    boxes2 = [
        ('URL Modality\n(XGBoost)', 1.7, 7.8, '#e3f2fd', C_BLUE),
        ('HTML Modality\n(XGBoost)', 1.7, 5.0, '#e0f2f1', C_TEAL),
        ('Visual Modality\n(MobileNetV3 + OCR)', 1.7, 2.2, '#fff3e0', C_CORAL),
    ]
    for text, x, y, bg, border in boxes2:
        # width 2.8, pad 0.15 -> right edge is 1.7 + 1.4 + 0.15 = 3.25
        ax2.add_patch(patches.FancyBboxPatch((x-1.4, y-0.9), 2.8, 1.8, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, lw=2.2))
        ax2.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)

    # Consistency Engine in the middle: left edge 4.4 - 0.2 = 4.2, right edge 4.4 + 2.8 + 0.2 = 7.4
    ax2.add_patch(patches.FancyBboxPatch((4.4, 2.6), 2.8, 4.8, boxstyle="round,pad=0.2", facecolor='#e8f5e9', edgecolor=C_GREEN, lw=2.8))
    ax2.text(5.8, 5.0, '25 Explicit\nCross-Modal\nConsistency\nFeatures\n\n(Jaccard Overlap,\nContainment,\nIdentity Checks)', ha='center', va='center', fontsize=10, fontweight='bold', color='#1b5e20')
    
    # Arrows to consistency engine
    ax2.annotate('', xy=(4.1, 6.2), xytext=(3.35, 7.8), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2, ls='--'))
    ax2.annotate('', xy=(4.1, 5.0), xytext=(3.35, 5.0), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=2, ls='--'))
    ax2.annotate('', xy=(4.1, 3.8), xytext=(3.35, 2.2), arrowprops=dict(arrowstyle="->", color=C_CORAL, lw=2, ls='--'))

    # Final Stacking Model: left edge 8.1 - 0.15 = 7.95
    ax2.add_patch(patches.FancyBboxPatch((8.1, 3.5), 1.7, 3.0, boxstyle="round,pad=0.15", facecolor='#ede7f6', edgecolor=C_PURPLE, lw=2.8))
    ax2.text(8.95, 5.0, 'Stacking\nClassifier\n(28-D Vector)\n\nVerdict &\nSHAP Proof', ha='center', va='center', fontsize=10, fontweight='bold', color='#4a148c')

    ax2.annotate('', xy=(7.85, 5.0), xytext=(7.5, 5.0), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.5))
    
    plt.tight_layout()
    plt.savefig('diagrams/fig1_1_concept.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. Figure 1.2: Dual Interface Ecosystem
def create_fig1_2():
    fig, ax = plt.subplots(figsize=(13.5, 5.8), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 15.0)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    
    # Client 1: Browser Extension (Left): outer bounds [0.35, 3.85]
    ax.add_patch(patches.FancyBboxPatch((0.5, 1.2), 3.2, 5.8, boxstyle="round,pad=0.15", facecolor='#e0f7fa', edgecolor=C_TEAL, lw=2.5))
    ax.text(2.1, 6.4, 'CLIENT TYPE A:\nBrowser Extension', ha='center', va='center', fontsize=12, fontweight='bold', color='#006064')
    ax.text(2.1, 3.8, 'Target Audience:\nEveryday Consumers & Staff\n\nKey Capabilities:\n• Real-Time Zero-Click Guard\n• Direct DOM & Tab Capture\n• Instant Safe / Caution Badges\n• Non-Bypassable Block Modal\n• Zero Latency Overhead', ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)

    # Core backend in center: outer bounds [5.85, 9.15]
    ax.add_patch(patches.FancyBboxPatch((6.0, 1.2), 3.0, 5.8, boxstyle="round,pad=0.15", facecolor='#f0f4f8', edgecolor=C_BLUE, lw=3))
    ax.text(7.5, 6.4, 'PhishAlign Core Engine', ha='center', va='center', fontsize=12.5, fontweight='bold', color=C_BLUE)
    ax.text(7.5, 3.8, '• Unified 3-Tier Policy\n• Tri-Modal XGBoost / CNN\n• 25 Consistency Metrics\n• Sub-160ms Fast Path\n• URL Asymmetry Gate', ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_DARK)

    # Client 2: Web Analytical Dashboard (Right): outer bounds [11.15, 14.65]
    ax.add_patch(patches.FancyBboxPatch((11.3, 1.2), 3.2, 5.8, boxstyle="round,pad=0.15", facecolor='#fff3e0', edgecolor=C_CORAL, lw=2.5))
    ax.text(12.9, 6.4, 'CLIENT TYPE B:\nWeb Dashboard', ha='center', va='center', fontsize=12, fontweight='bold', color='#e65100')
    ax.text(12.9, 3.8, 'Target Audience:\nSOC Analysts & Researchers\n\nKey Capabilities:\n• Deep Forensic Audit Dossier\n• Server Headless Playwright\n• Jaccard Overlap Heatmaps\n• Modality Breakdown Gauges\n• Benchmark Comparison Mode\n• Game-Theoretic SHAP Proofs', ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_DARK)

    # Bidirectional arrows in generous 2.0-unit gaps
    # Gap 1: [3.85, 5.85], center 4.85
    ax.annotate('', xy=(5.7, 4.0), xytext=(4.0, 4.0), arrowprops=dict(arrowstyle="<->", color=C_TEAL, lw=3.0))
    ax.text(4.85, 4.45, 'REST API\n(/analyze-content)', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_TEAL)
    
    # Gap 2: [9.15, 11.15], center 10.15
    ax.annotate('', xy=(11.0, 4.0), xytext=(9.3, 4.0), arrowprops=dict(arrowstyle="<->", color=C_CORAL, lw=3.0))
    ax.text(10.15, 4.45, 'REST API\n(/analyze)', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=C_CORAL)

    plt.tight_layout()
    plt.savefig('diagrams/fig1_2_dual_interface.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. Figure 2.1: Tri-Modality Feature Space & 25-D Consistency Vector
def create_fig2_1():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 9.0)
    ax.axis('off')

    # Modality Nodes: outer bounds x in [0.2, 3.6]
    nodes = [
        ('URL Modality (31 Dims)\nLexical, Hostname & Entropy\n(XGBoost Model 1)', 1.9, 7.3, C_BLUE, '#e3f2fd'),
        ('HTML Modality (64 Dims)\nDOM Tree, Forms, Scripts & Links\n(XGBoost Model 2)', 1.9, 4.5, C_TEAL, '#e0f2f1'),
        ('Visual Modality (CNN + OCR)\nMobileNetV3 + Tesseract OCR\n(MobileNetV3 Model 3)', 1.9, 1.7, C_CORAL, '#fff3e0'),
    ]
    for text, x, y, col, bg in nodes:
        ax.add_patch(patches.FancyBboxPatch((x-1.6, y-0.95), 3.2, 1.9, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=col, lw=2.5))
        ax.text(x, y, text, ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_DARK)

    # Cross-Modal Consistency Metrics Box: outer bounds x in [4.8, 13.2]
    ax.add_patch(patches.FancyBboxPatch((5.0, 0.5), 8.0, 8.0, boxstyle="round,pad=0.2", facecolor='#f9fbe7', edgecolor=C_GREEN, lw=3))
    ax.text(9.0, 8.05, '25 Cross-Modal Consistency Features', ha='center', va='center', fontsize=13, fontweight='bold', color='#33691e')

    categories = [
        ('1. Availability Indicators (5 Features)', 
         'html_available, ocr_available, title_available,\nboth_html_ocr_available, url_host_available', 6.6, 1.6),
        ('2. Pairwise Text Overlap (10 Features)', 
         'url_html_jaccard, url_html_containment, url_ocr_jaccard,\nurl_ocr_containment, url_title_jaccard, url_title_containment,\nhtml_ocr_jaccard, html_ocr_containment, title_ocr_jaccard, title_ocr_containment', 4.3, 2.1),
        ('3. Domain Identity Overlap (10 Features)', 
         'domain_identity_token_count_v3, domain_html_jaccard_v3,\ndomain_html_containment_v3, domain_html_comp_avail_v3,\ndomain_ocr_jaccard_v3, domain_ocr_containment_v3,\ndomain_ocr_comp_avail_v3, domain_title_jaccard_v3,\ndomain_title_containment_v3, domain_title_comp_avail_v3', 1.7, 2.5),
    ]

    for title, desc, y_pos, box_h in categories:
        ax.add_patch(patches.FancyBboxPatch((5.25, y_pos-box_h/2), 7.5, box_h, boxstyle="round,pad=0.12", facecolor='#ffffff', edgecolor='#c0ca33', lw=1.8))
        ax.text(5.5, y_pos + box_h/2 - 0.32, title, ha='left', va='center', fontsize=10.5, fontweight='bold', color='#558b2f')
        ax.text(5.5, y_pos - 0.25, desc, ha='left', va='center', fontsize=8.5, family='monospace', fontweight='bold', color=C_DARK)

    # Connections cleanly in the gap [3.65, 4.75]
    ax.annotate('', xy=(4.7, 6.6), xytext=(3.7, 7.3), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.2))
    ax.annotate('', xy=(4.7, 4.5), xytext=(3.7, 4.5), arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=2.2))
    ax.annotate('', xy=(4.7, 2.0), xytext=(3.7, 1.7), arrowprops=dict(arrowstyle="->", color=C_CORAL, lw=2.2))

    plt.tight_layout()
    plt.savefig('diagrams/fig2_1_trimodal_space.png', dpi=300, bbox_inches='tight')
    plt.close()

# 4. Figure 2.2: Stacking Architecture
def create_fig2_2():
    fig, ax = plt.subplots(figsize=(12, 6.0), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # Base models
    models = [
        ('URL Features\n(31 tabular dims)', 'XGBoost\nURL Classifier', 1.3, 5.8, C_BLUE, '#e3f2fd', 'P(URL)'),
        ('HTML Features\n(64 tabular dims)', 'XGBoost\nHTML Classifier', 1.3, 3.7, C_TEAL, '#e0f2f1', 'P(HTML)'),
        ('Screenshot\n(224x224x3 RGB)', 'MobileNetV3-Small\nVisual Classifier', 1.3, 1.6, C_CORAL, '#fff3e0', 'P(Visual)'),
    ]
    for inp, mdl, x, y, col, bg, prob_lbl in models:
        # Input box: outer right edge is 0.3 + 1.5 + 0.1 = 1.9
        ax.add_patch(patches.FancyBboxPatch((x-1.0, y-0.75), 1.5, 1.5, boxstyle="round,pad=0.1", facecolor='#ffffff', edgecolor='#757575', lw=1.5))
        ax.text(x-0.25, y, inp, ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_DARK)
        
        # Arrow to base classifier: gap [1.9, 2.25]
        ax.annotate('', xy=(2.2, y), xytext=(1.95, y), arrowprops=dict(arrowstyle="->", color='#616161', lw=2))
        
        # Base classifier box: outer x in [2.25, 4.45]
        ax.add_patch(patches.FancyBboxPatch((2.4, y-0.75), 1.9, 1.5, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=col, lw=2.2))
        ax.text(3.35, y, mdl, ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)
        
        # Probability label and arrow: gap [4.45, 5.4]
        ax.text(4.9, y+0.28, prob_lbl, ha='center', va='bottom', fontsize=10, fontweight='bold', color=col)
        ax.annotate('', xy=(5.35, y), xytext=(4.55, y), arrowprops=dict(arrowstyle="->", color=col, lw=2.2))

    # Vector Box: outer x in [5.4, 8.0]
    ax.add_patch(patches.FancyBboxPatch((5.6, 0.8), 2.2, 5.8, boxstyle="round,pad=0.2", facecolor='#f5f5f5', edgecolor=C_DARK, lw=2.5))
    ax.text(6.7, 6.1, '28-D Feature Vector', ha='center', va='center', fontsize=11.5, fontweight='bold', color=C_DARK)
    ax.text(6.7, 3.8, '• P_url (1)\n• P_html (1)\n• P_visual (1)\n\n+ 25 Explicit\nCross-Modal\nConsistency\nFeatures', ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_DARK)

    # Arrow to Meta Learner: gap [8.0, 8.6]
    ax.annotate('', xy=(8.55, 3.7), xytext=(8.05, 3.7), arrowprops=dict(arrowstyle="->", color=C_PURPLE, lw=3))

    # Meta Learner: outer x in [8.6, 11.8]
    ax.add_patch(patches.FancyBboxPatch((8.8, 1.6), 2.8, 4.2, boxstyle="round,pad=0.2", facecolor='#ede7f6', edgecolor=C_PURPLE, lw=3))
    ax.text(10.2, 5.0, 'Stacking Meta-Learner\n(Logistic Regression L2)', ha='center', va='center', fontsize=11, fontweight='bold', color='#4a148c')
    ax.text(10.2, 3.0, 'Calibrated Decision Policy:\n• Safe: < 50%\n• Caution: 50% - 77%\n• Phishing: ≥ 78%\n\nFull-Screen Block Overlay', ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_DARK)

    plt.tight_layout()
    plt.savefig('diagrams/fig2_2_stacking_arch.png', dpi=300, bbox_inches='tight')
    plt.close()

# 5. Figure 4.1: Development Methodology
def create_fig4_1():
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 5.6)
    ax.axis('off')

    stages = [
        ('Phase 1:\nProblem & Dataset\nPhish360 Curation\nLeak-Free Group Split', 1.3, C_BLUE, '#e3f2fd'),
        ('Phase 2:\nFeature Engineering\n& Base Models\n31 URL & 64 HTML', 3.6, C_TEAL, '#e0f2f1'),
        ('Phase 3:\nConsistency Engine\n25 Jaccard & Identity\nFeatures Designed', 5.9, C_GREEN, '#e8f5e9'),
        ('Phase 4:\nStacking Fusion\n& Evaluation\nAblation & Bootstrap', 8.2, C_PURPLE, '#ede7f6'),
        ('Phase 5:\nDual App Delivery\nFastAPI, React Web,\nChrome Extension', 10.5, C_CORAL, '#fff3e0'),
    ]
    w = 1.7
    h = 2.4
    pad = 0.15
    for text, x, col, bg in stages:
        ax.add_patch(patches.FancyBboxPatch((x-w/2, 2.0), w, h, boxstyle=f"round,pad={pad}", facecolor=bg, edgecolor=col, lw=2.2))
        ax.text(x, 3.2, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_DARK)

    # Forward arrows in the gaps [x + w/2 + pad, next_x - w/2 - pad]
    for i in range(len(stages)-1):
        x1 = stages[i][1] + w/2 + pad + 0.04
        x2 = stages[i+1][1] - w/2 - pad - 0.04
        ax.annotate('', xy=(x2, 3.2), xytext=(x1, 3.2), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2.2))

    # Iterative Feedback Loop below boxes with no collision (rad=-0.35 curves DOWNWARDS)
    ax.annotate('', xy=(3.6, 1.8), xytext=(8.2, 1.8), 
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=2.2, connectionstyle="arc3,rad=-0.32", ls='--'))
    ax.text(5.9, 0.45, 'Iterative Metric Validation & Hyperparameter Tuning Loop', ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_RED)

    plt.tight_layout()
    plt.savefig('diagrams/fig4_1_dev_model.png', dpi=300, bbox_inches='tight')
    plt.close()

# 6. Figure 4.2: Gantt Chart Schedule
def create_fig4_2():
    fig, ax = plt.subplots(figsize=(11, 5.0), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    tasks = [
        "1. Literature Review & Problem Formulation",
        "2. Phish360 Dataset Curation & Leak Audit",
        "3. Base URL & HTML Feature Engineering (31/64)",
        "4. Visual MobileNetV3 Training & OCR",
        "5. Cross-Modal Consistency Feature Design",
        "6. Fusion Meta-Classifier & Ablation Study",
        "7. FastAPI Backend & Playwright Pipeline",
        "8. React Web Forensic Dashboard UI",
        "9. Chrome Extension Development (MV3)",
        "10. End-to-End Evaluation & Final Documentation"
    ]
    starts = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    durations = [3, 3, 3, 4, 3, 3, 4, 4, 4, 5]
    colors = [C_BLUE, C_BLUE, C_TEAL, C_TEAL, C_GREEN, C_GREEN, C_PURPLE, C_CORAL, C_CORAL, C_DARK]

    y_pos = np.arange(len(tasks))
    ax.barh(y_pos, durations, left=starts, align='center', color=colors, height=0.62, edgecolor='none', alpha=0.92)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tasks, fontsize=10.5, fontweight='bold', color=C_DARK)
    ax.invert_yaxis()
    ax.set_xlabel('Project Timeline (Weeks)', fontsize=12, fontweight='bold', color=C_DARK)
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25, 2))
    ax.tick_params(axis='x', labelsize=10.5)
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig('diagrams/fig4_2_schedule.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_fig1_1()
    create_fig1_2()
    create_fig2_1()
    create_fig2_2()
    create_fig4_1()
    create_fig4_2()
    print("Batch 1 diagrams generated successfully!")
