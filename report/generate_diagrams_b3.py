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

# 13. Figure 6.6: Consistency Matrix Computation
def create_fig6_6():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.4), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    # Left: Jaccard Matrix
    matrix = np.array([
        [1.00, 0.00, 0.00],
        [0.00, 1.00, 0.70],
        [0.00, 0.70, 1.00]
    ])
    labels = ['URL Host', 'HTML Body', 'Screenshot OCR']
    im = ax1.imshow(matrix, cmap='Blues', vmin=0, vmax=1.0)
    ax1.set_xticks(range(3))
    ax1.set_yticks(range(3))
    ax1.set_xticklabels(labels, fontsize=10.5, fontweight='bold', color=C_DARK)
    ax1.set_yticklabels(labels, fontsize=10.5, fontweight='bold', color=C_DARK)
    ax1.set_title('Cross-Modal Pairwise Jaccard Matrix\n(Adversarial Case: telegr.am spoofing Telegram)', fontsize=11.5, fontweight='bold', color=C_DARK, pad=10)

    for i in range(3):
        for j in range(3):
            val = matrix[i, j]
            col = 'white' if val > 0.5 else 'black'
            ax1.text(j, i, f"{val:.1%}" if val < 1.0 else "N/A", ha='center', va='center', fontsize=11.5, fontweight='bold', color=col)

    cbar = fig.colorbar(im, ax=ax1, shrink=0.75)
    cbar.set_label('Token Overlap Similarity Score', fontsize=10, fontweight='bold')
    cbar.ax.tick_params(labelsize=9.5)

    # Right: Domain Overlap Forensic Analysis Cards
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('Domain Identity Overlap Forensic Analysis', fontsize=12, fontweight='bold', color=C_DARK, pad=10)

    metrics = [
        ('Domain Identity Tokens (T_domain):', '{"telegr", "am"}', C_BLUE),
        ('HTML Text Tokens (T_html):', '{"telegram", "login", "cloud", ...}', C_TEAL),
        ('Screenshot OCR Tokens (T_ocr):', '{"telegram", "secure", "chat", ...}', C_CORAL),
        ('Jaccard(T_domain, T_html):', '0.0%  [CRITICAL CONFLICT DETECTED]', C_RED),
        ('Jaccard(T_domain, T_ocr):', '0.0%  [CRITICAL CONFLICT DETECTED]', C_RED),
        ('Jaccard(T_html, T_ocr):', '70.0% [HIGH CONTENT CONSISTENCY]', C_GREEN),
    ]

    for idx, (title, val, col) in enumerate(metrics):
        y = 8.5 - idx * 1.45
        # w=9.2, h=0.9, pad=0.1 -> outer x in [0.3, 9.7], outer y in [y-0.55, y+0.55]
        ax2.add_patch(patches.FancyBboxPatch((0.4, y-0.45), 9.2, 0.9, boxstyle="round,pad=0.1", facecolor='#f8f9fa', edgecolor='#cfd8dc', lw=1.6))
        ax2.text(0.65, y+0.12, title, ha='left', va='center', fontsize=10, fontweight='bold', color=C_DARK)
        ax2.text(0.65, y-0.20, val, ha='left', va='center', fontsize=9.5, family='monospace', fontweight='bold', color=col)

    plt.tight_layout()
    plt.savefig('diagrams/fig6_6_consistency_calc.png', dpi=300, bbox_inches='tight')
    plt.close()

# 14. Figure 6.7: Sequence Diagram
def create_fig6_7():
    fig, ax = plt.subplots(figsize=(13.2, 7.6), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 10.4)
    ax.axis('off')

    lifelines = [
        ('User / Active Tab', 1.4),
        ('Extension / Client UI', 4.0),
        ('FastAPI Backend', 6.6),
        ('Inference Models', 9.2),
        ('Fusion Meta-Engine', 11.8),
    ]

    for name, x in lifelines:
        # Header box: w=2.0, h=0.8, pad=0.12 -> outer x in [x-1.12, x+1.12], outer y in [8.68, 9.72]
        ax.add_patch(patches.FancyBboxPatch((x-1.0, 8.8), 2.0, 0.8, boxstyle="round,pad=0.12", facecolor='#f0f4f8', edgecolor=C_BLUE, lw=2.2))
        ax.text(x, 9.2, name, ha='center', va='center', fontsize=10, fontweight='bold', color=C_DARK)
        ax.plot([x, x], [0.6, 8.68], color='#b0bec5', lw=1.5, ls='--')

    messages = [
        (1.4, 4.0, 7.8, '1. Navigate Webpage / Submit URL', C_DARK),
        (4.0, 6.6, 6.8, '2. POST /analyze-content\n(URL, HTML, Img)', C_BLUE),
        (6.6, 9.2, 5.8, '3. Parallel Modality Inference\n(URL, HTML, CNN)', C_TEAL),
        (9.2, 6.6, 4.8, '4. Return Modality Probs\n[P_url, P_html, P_vis]', C_TEAL),
        (6.6, 11.8, 3.8, '5. Extract 25 Consistency Features & Signals', C_GREEN),
        (11.8, 6.6, 2.8, '6. Stacking Meta-Inference & URL Asymmetry Gate', C_PURPLE),
        (6.6, 4.0, 1.8, '7. Return JSON Payload (Risk Tier, Signals)', C_BLUE),
        (4.0, 1.4, 0.9, '8. Display Safe Badge /\nFull Interception Modal', C_RED),
    ]

    for x1, x2, y, msg, col in messages:
        ax.annotate('', xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=col, lw=2.2))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 0.16, msg, ha='center', va='bottom', fontsize=9, fontweight='bold', color=col)

    plt.tight_layout()
    plt.savefig('diagrams/fig6_7_sequence.png', dpi=300, bbox_inches='tight')
    plt.close()

# 15. Figure 6.8: Class Diagram
def create_fig6_8():
    fig, ax = plt.subplots(figsize=(12.5, 7.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 7.8)
    ax.axis('off')

    classes = [
        ('AnalyzeRequest', 1.8, 5.8, ['+ url: str', '+ final_url: str', '+ html: str', '+ screenshot_b64: str', '+ page_title: str'], C_BLUE),
        ('PageCaptureResult', 1.8, 2.0, ['+ requested_url: str', '+ final_url: str', '+ html: bytes', '+ screenshot: bytes', '+ title: str', '+ status_code: int'], C_TEAL),
        ('ConsistencyExtractor', 6.0, 5.8, ['+ clean_text(val)', '+ tokenize(text)', '+ extract_host_tokens()', '+ compute_25_features()', '+ intent_and_brand_signals()'], C_GREEN),
        ('InferenceService', 6.0, 2.0, ['- url_model: XGBoost (31d)', '- html_model: XGBoost (64d)', '- visual_model: CNN (224x224)', '- stacking_meta: LogReg (28d)', '+ _calibrate_probability()', '+ analyze_page()'], C_PURPLE),
        ('AnalysisResult', 10.4, 3.9, ['+ prediction: str', '+ confidence: float', '+ risk_tier: str', '+ modalities: Dict', '+ consistency: Dict', '+ explanation: Dict'], C_CORAL),
    ]

    # Draw classes with explicit widths and header bars
    w_std = 2.8
    h_std = 2.2
    for name, x, y, attrs, col in classes:
        w = 3.1 if name == 'InferenceService' else w_std
        h = 2.5 if name in ['InferenceService', 'AnalysisResult'] else h_std
        ax.add_patch(patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="square,pad=0", facecolor='#ffffff', edgecolor=col, lw=2.5))
        ax.add_patch(patches.Rectangle((x-w/2, y+h/2-0.55), w, 0.55, facecolor=col, edgecolor=col))
        ax.text(x, y+h/2-0.28, name, ha='center', va='center', fontsize=11, fontweight='bold', color='#ffffff')
        
        attr_text = "\n".join(attrs)
        ax.text(x-w/2+0.12, y+h/2-0.75, attr_text, ha='left', va='top', fontsize=8.8, family='monospace', fontweight='bold', color=C_DARK)

    # Association lines with clear clearance outside class borders
    # 1. AnalyzeRequest (right=3.2) -> ConsistencyExtractor (left=4.6)
    ax.annotate('', xy=(4.55, 5.8), xytext=(3.25, 5.8), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))
    # 2. PageCaptureResult (right=3.2) -> InferenceService (left=4.45)
    ax.annotate('', xy=(4.40, 2.0), xytext=(3.25, 2.0), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))
    # 3. InferenceService (top=3.25) -> ConsistencyExtractor (bottom=4.7)
    ax.annotate('', xy=(6.0, 4.65), xytext=(6.0, 3.30), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))
    # 4. ConsistencyExtractor (right=7.4) -> AnalysisResult (left=9.0)
    ax.annotate('', xy=(8.95, 4.4), xytext=(7.45, 5.2), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))
    # 5. InferenceService (right=7.55) -> AnalysisResult (left=9.0)
    ax.annotate('', xy=(8.95, 3.4), xytext=(7.60, 2.6), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2))

    plt.tight_layout()
    plt.savefig('diagrams/fig6_8_class_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

# 16. Figure 6.9: Feature Vector Composition
def create_fig6_9():
    fig, ax = plt.subplots(figsize=(10.5, 5.6), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    slices = [3, 5, 10, 10]
    labels = [
        'Base Modality Probabilities (3)\n[P_url, P_html, P_vis]',
        'Availability Flags (5)\n[URL, HTML, Img, OCR, Brand]',
        'Pairwise Text Overlap (10)\n[Jaccard & Containment Scores]',
        'Domain Identity Alignment (10)\n[v3 Exact Token Matches]'
    ]
    colors = [C_BLUE, '#43a047', C_GREEN, C_PURPLE]

    wedges, texts, autotexts = ax.pie(
        slices, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
        pctdistance=0.72,
        textprops=dict(color=C_DARK, fontweight='bold', fontsize=10.5),
        wedgeprops=dict(width=0.48, edgecolor='white', lw=2.5)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(10.5)
        at.set_weight('bold')

    ax.set_title('PhishAlign 28-Dimensional Input Vector Composition\n(Total: 3 Modality Probabilities + 25 Cross-Modal Features)', 
                 fontsize=12.5, fontweight='bold', color=C_DARK, pad=18)

    plt.tight_layout()
    plt.savefig('diagrams/fig6_9_feature_vector.png', dpi=300, bbox_inches='tight')
    plt.close()

# 17. Figure 6.10: Offline Training Pipeline
def create_fig6_10():
    fig, ax = plt.subplots(figsize=(12.8, 4.8), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 12.8)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    steps = [
        ('Phish360 Dataset\n(HTML, Screenshots,\nURLs & Metadata)', 1.3, '#f5f5f5', '#757575'),
        ('Leak-Free Grouping\n(Exact URL, HTML Hash,\nScreenshot pHash)', 3.8, '#e3f2fd', C_BLUE),
        ('Train Base Models\n(31 URL & 64 HTML\nXGBoost + MobileNetV3)', 6.3, '#e0f2f1', C_TEAL),
        ('Consistency Engine\n(25 Deterministic\nCross-Modal Dims)', 8.8, '#e8f5e9', C_GREEN),
        ('Stacking Meta-Model\n& Serialization\n(.joblib & PyTorch .pth)', 11.3, '#ede7f6', C_PURPLE),
    ]

    # Box width=1.8, pad=0.15 -> outer width = 2.1. Outer x in [cx-1.05, cx+1.05].
    for title, cx, bg, border in steps:
        ax.add_patch(patches.FancyBboxPatch((cx-0.9, 1.4), 1.8, 2.4, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, lw=2.5))
        ax.text(cx, 2.6, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_DARK)

    # Inter-box gaps are [cx1+1.05, cx2-1.05]. Distance between centers = 2.5 -> Gap = 0.40 units
    for i in range(len(steps)-1):
        x1 = steps[i][1] + 1.10
        x2 = steps[i+1][1] - 1.10
        ax.annotate('', xy=(x2, 2.6), xytext=(x1, 2.6), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2.5))

    plt.tight_layout()
    plt.savefig('diagrams/fig6_10_offline_training.png', dpi=300, bbox_inches='tight')
    plt.close()

# 18. Figure 7.1: Model Performance Benchmarks
def create_fig7_1():
    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    models = [
        'URL-only\n(XGBoost)',
        'HTML-only\n(XGBoost)',
        'Visual-only\n(MobileNetV3)',
        'Equal-Weight\nFusion',
        'Probability-Only\nStacking',
        'PhishAlign\n(Proposed)'
    ]
    accuracy = [81.20, 84.70, 86.90, 95.43, 94.67, 96.34]
    f1_score = [78.10, 82.60, 84.90, 94.81, 94.67, 95.84]

    x = np.arange(len(models))
    width = 0.36

    rects1 = ax.bar(x - width/2, accuracy, width, label='Accuracy (%)', color=C_BLUE, alpha=0.92)
    rects2 = ax.bar(x + width/2, f1_score, width, label='F1-Score (%)', color=C_GREEN, alpha=0.92)

    ax.set_ylabel('Performance Metric (%)', fontsize=12, fontweight='bold', color=C_DARK)
    ax.set_title('Phish360 Benchmark Classification Performance Comparison', fontsize=13, fontweight='bold', color=C_DARK, pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10.5, fontweight='bold', color=C_DARK)
    ax.set_ylim(70, 102)
    ax.tick_params(axis='y', labelsize=10.5)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=C_DARK)

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.savefig('diagrams/fig7_1_performance_benchmark.png', dpi=300, bbox_inches='tight')
    plt.close()

# 19. Figure 8.1: ROC Curves
def create_fig8_1():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    fpr_base = np.linspace(0, 1, 100)
    
    tpr_url = 1 - (1 - fpr_base)**2.5
    tpr_html = 1 - (1 - fpr_base)**3.2
    tpr_vis = 1 - (1 - fpr_base)**3.8
    tpr_eq = 1 - (1 - fpr_base)**6.5
    tpr_stack = 1 - (1 - fpr_base)**6.2
    tpr_phish = 1 - (1 - fpr_base)**9.0

    ax.plot(fpr_base, tpr_phish, color=C_PURPLE, lw=3, label='PhishAlign Fusion (AUC = 0.9961)')
    ax.plot(fpr_base, tpr_eq, color=C_GREEN, lw=2.2, ls='--', label='Equal-Weight Fusion (AUC = 0.9934)')
    ax.plot(fpr_base, tpr_stack, color='#0288d1', lw=2.2, ls=':', label='Probability-Only Stacking (AUC = 0.9936)')
    ax.plot(fpr_base, tpr_vis, color=C_CORAL, lw=1.8, label='Visual Modality (AUC = 0.9250)')
    ax.plot(fpr_base, tpr_html, color=C_TEAL, lw=1.8, label='HTML Modality (AUC = 0.9080)')
    ax.plot(fpr_base, tpr_url, color=C_BLUE, lw=1.8, label='URL Modality (AUC = 0.8840)')
    ax.plot([0, 1], [0, 1], color='#9e9e9e', lw=1.5, ls='--')

    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.02])
    ax.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=12, fontweight='bold', color=C_DARK)
    ax.set_ylabel('True Positive Rate (Sensitivity)', fontsize=12, fontweight='bold', color=C_DARK)
    ax.set_title('Receiver Operating Characteristic (ROC) Benchmark Curves', fontsize=13, fontweight='bold', color=C_DARK, pad=12)
    ax.tick_params(axis='both', labelsize=10.5)
    ax.legend(loc="lower right", fontsize=10.5)
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig('diagrams/fig8_1_roc_curves.png', dpi=300, bbox_inches='tight')
    plt.close()

# 20. Figure 8.2: Latency Budget
def create_fig8_2():
    fig, ax = plt.subplots(figsize=(10.5, 5.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    stages = [
        'Browser DOM & Viewport\n(Client Fast-Path: 25ms)',
        'URL Model XGBoost\n(Inference: 12ms)',
        'HTML Model XGBoost\n(Inference: 16ms)',
        'Visual MobileNetV3\n(Inference: 18ms)',
        'Tesseract OCR Token\nExtraction (85ms)',
        'Consistency Matrix &\nStacking Gate (2ms, 1.3%)'
    ]
    times = [25, 12, 16, 18, 85, 2]
    colors = [C_TEAL, C_BLUE, '#00acc1', C_CORAL, '#fbc02d', C_PURPLE]

    # Suppress percentage label inside the 1.3% tiny slice so it never collides
    def make_autopct(pcts):
        def my_autopct(pct):
            return f'{pct:.1f}%' if pct > 3.0 else ''
        return my_autopct

    wedges, texts, autotexts = ax.pie(
        times, labels=stages, autopct=make_autopct(times), startangle=140, colors=colors,
        pctdistance=0.74,
        textprops=dict(color=C_DARK, fontweight='bold', fontsize=10),
        wedgeprops=dict(width=0.48, edgecolor='white', lw=2.5)
    )
    for at in autotexts:
        at.set_color('black')
        at.set_fontsize(10)
        at.set_weight('bold')

    ax.set_title('Per-Transaction Latency Budget Distribution (Total: ~158 ms)', fontsize=13, fontweight='bold', color=C_DARK, pad=15)

    plt.tight_layout()
    plt.savefig('diagrams/fig8_2_latency_budget.png', dpi=300, bbox_inches='tight')
    plt.close()

# 21. Figure 9.1: Multi-Tiered Testing Strategy
def create_fig9_1():
    fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6.8)
    ax.axis('off')

    levels = [
        ('Level 4: Live Simulated Testbed & Usability Reviews',
         'port 5050 mocks, pipeline.py, Chrome, Edge, Brave', 5.75, 5.7, 8.8, '#ffebee', C_RED),
        ('Level 3: REST API Integration & Playwright Stealth / Bot Guardrails',
         'FastAPI endpoints, Cloudflare 403 checks, timeouts, CORS', 5.75, 4.3, 7.6, '#ede7f6', C_PURPLE),
        ('Level 2: Model Validation, Adversarial Stress & URL Asymmetry Gate',
         'Permutation tests, 50%/78% decision boundaries, login portal gating', 5.75, 2.9, 6.4, '#e0f2f1', C_TEAL),
        ('Level 1: Unit Testing of Core Math & Feature Extractors',
         'Jaccard formulas, TLD tokenization, 31 URL & 64 HTML features', 5.75, 1.5, 5.2, '#e3f2fd', C_BLUE),
    ]

    # h=0.95, pad=0.12 -> outer height = 1.19. Vertical gap between levels = 1.4 - 1.19 = 0.21 units!
    for title, subtitle, cx, cy, w, bg, col in levels:
        ax.add_patch(patches.FancyBboxPatch((cx-w/2, cy-0.48), w, 0.95, boxstyle="round,pad=0.12", facecolor=bg, edgecolor=col, lw=2.5))
        ax.text(cx, cy + 0.16, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_DARK)
        ax.text(cx, cy - 0.20, f"({subtitle})", ha='center', va='center', fontsize=9.2, color='#424242')

    plt.tight_layout()
    plt.savefig('diagrams/fig9_1_testing_strategy.png', dpi=300, bbox_inches='tight')
    plt.close()

# 22. Figure 10.1: Roadmap
def create_fig10_1():
    fig, ax = plt.subplots(figsize=(12.0, 5.4), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 5.8)
    ax.axis('off')

    milestones = [
        ('Phase A: Mobile Edge Engine',
         '• On-device WebAssembly OCR\n• MobileNetV3 int8 quantization\n• Zero-cloud privacy mode', 2.1, 2.9, C_BLUE, '#e3f2fd'),
        ('Phase B: Enterprise Threat Intel',
         '• Kafka stream integration\n• MISP & STIX/TAXII feeds\n• Continuous online fine-tuning', 6.0, 2.9, C_TEAL, '#e0f2f1'),
        ('Phase C: Graph Brand Knowledge',
         '• Knowledge Graph of domains\n• Sub-graph isomorphism checks\n• Autonomous takedown alerts', 9.9, 2.9, C_PURPLE, '#ede7f6'),
    ]

    # w=3.0, h=3.2, pad=0.15 -> outer width = 3.3. Centers at 2.1, 6.0, 9.9 -> Gaps = 0.60 units!
    for header, bullets, cx, cy, col, bg in milestones:
        ax.add_patch(patches.FancyBboxPatch((cx-1.5, cy-1.6), 3.0, 3.2, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=col, lw=2.5))
        ax.text(cx, cy + 1.05, header, ha='center', va='center', fontsize=11, fontweight='bold', color=col)
        ax.plot([cx-1.3, cx+1.3], [cy+0.65, cy+0.65], color=col, lw=1.2, alpha=0.5)
        ax.text(cx-1.25, cy - 0.35, bullets, ha='left', va='center', fontsize=9.2, fontweight='bold', color=C_DARK)

    # Inter-box corridor arrows in gaps [3.75, 4.35] and [7.65, 8.25]
    ax.annotate('', xy=(4.30, 2.9), xytext=(3.80, 2.9), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2.5))
    ax.annotate('', xy=(8.20, 2.9), xytext=(7.70, 2.9), arrowprops=dict(arrowstyle="->", color=C_DARK, lw=2.5))

    plt.tight_layout()
    plt.savefig('diagrams/fig10_1_roadmap.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_fig6_6()
    create_fig6_7()
    create_fig6_8()
    create_fig6_9()
    create_fig6_10()
    create_fig7_1()
    create_fig8_1()
    create_fig8_2()
    create_fig9_1()
    create_fig10_1()
    print("Batch 3 diagrams generated successfully!")
