import os
import sys

# Ensure working directory is set to this script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('diagrams', exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def create_fig_c1():
    fig, ax = plt.subplots(figsize=(13.0, 7.0), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#fafafa')
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 7.0)
    ax.axis('off')

    # Main Title
    ax.text(6.5, 6.65, "PhishAlign User Empathy & Human-Centered Engineering Framework",
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1a237e')
    ax.text(6.5, 6.35, "Aligning End-User Browsing Friction and SOC Analyst Cognitive Load to Dedicated Interfaces",
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#455a64')

    # Card 1: Everyday Web Consumer (Left)
    card1 = patches.FancyBboxPatch((0.5, 0.4), 5.7, 5.7, boxstyle="round,pad=0.1,rounding_size=0.15",
                                  facecolor='#ffffff', edgecolor='#0288d1', linewidth=2.0)
    ax.add_patch(card1)
    
    # Header 1
    hdr1 = patches.FancyBboxPatch((0.5, 5.5), 5.7, 0.6, boxstyle="round,pad=0.05,rounding_size=0.1",
                                 facecolor='#0288d1', edgecolor='#0288d1', linewidth=1.0)
    ax.add_patch(hdr1)
    ax.text(3.35, 5.8, "PERSONA A: Everyday Consumer / Enterprise User",
            ha='center', va='center', fontsize=11.5, fontweight='bold', color='#ffffff')

    # Quadrants for Persona A
    boxes_a = [
        ("SAYS & THINKS", "'I just want to do my banking safely without inspecting SSL certs.'\n'Security tools are annoying when they block normal websites.'", 4.4, '#e1f5fe', '#0288d1'),
        ("DOES & FEELS", "Clicks links rapidly in emails/chats; trusts visual logos blindly.\nFeels anxious about credential theft; frustrated by slow browsing.", 3.2, '#e1f5fe', '#0288d1'),
        ("CORE FRICTION / PAIN", "Sluggish browser extension lag (>500ms) and false positive friction\non legitimate corporate login portals (Teams, Microsoft 365).", 2.0, '#ffebee', '#c62828'),
        ("ENGINEERED SOLUTION", "PhishAlign Chromium Extension (MV3):\n• Ultra-fast <160ms background analysis (Layer 1 fast path)\n• Silent green badge on safe sites; unmissable full-screen blocking overlay", 0.75, '#e8f5e9', '#2e7d32')
    ]
    for title, desc, y_pos, bg, border in boxes_a:
        bx = patches.FancyBboxPatch((0.7, y_pos), 5.3, 1.05, boxstyle="round,pad=0.08,rounding_size=0.1",
                                   facecolor=bg, edgecolor=border, linewidth=1.2)
        ax.add_patch(bx)
        ax.text(0.85, y_pos + 0.85, title, fontsize=9.5, fontweight='bold', color=border)
        ax.text(0.85, y_pos + 0.42, desc, fontsize=8.5, color='#212121', va='center')

    # Card 2: SOC Security Analyst (Right)
    card2 = patches.FancyBboxPatch((6.8, 0.4), 5.7, 5.7, boxstyle="round,pad=0.1,rounding_size=0.15",
                                  facecolor='#ffffff', edgecolor='#4527a0', linewidth=2.0)
    ax.add_patch(card2)

    # Header 2
    hdr2 = patches.FancyBboxPatch((6.8, 5.5), 5.7, 0.6, boxstyle="round,pad=0.05,rounding_size=0.1",
                                 facecolor='#4527a0', edgecolor='#4527a0', linewidth=1.0)
    ax.add_patch(hdr2)
    ax.text(9.65, 5.8, "PERSONA B: SOC Threat Analyst & Incident Responder",
            ha='center', va='center', fontsize=11.5, fontweight='bold', color='#ffffff')

    # Quadrants for Persona B
    boxes_b = [
        ("SAYS & THINKS", "'A single percentage score is useless without forensic evidence.'\n'I need to know why this URL was flagged before isolating the host.'", 4.4, '#ede7f6', '#4527a0'),
        ("DOES & FEELS", "Audits quarantined URLs, inspects raw DOM, cross-references OCR.\nFeels overwhelmed by alert fatigue and opaque black-box ML decisions.", 3.2, '#ede7f6', '#4527a0'),
        ("CORE FRICTION / PAIN", "Lack of interpretability in conventional neural network detectors;\nzero visibility into cross-channel semantic contradictions.", 2.0, '#ffebee', '#c62828'),
        ("ENGINEERED SOLUTION", "PhishAlign Web Analytical Dashboard (React/Vite):\n• Multi-tab forensic workbench (URL, DOM, MobileNetV3 visual inspector)\n• Interactive 3x3 Jaccard matrix, domain identity token breakdown & SHAP", 0.75, '#e8f5e9', '#2e7d32')
    ]
    for title, desc, y_pos, bg, border in boxes_b:
        bx = patches.FancyBboxPatch((7.0, y_pos), 5.3, 1.05, boxstyle="round,pad=0.08,rounding_size=0.1",
                                   facecolor=bg, edgecolor=border, linewidth=1.2)
        ax.add_patch(bx)
        ax.text(7.15, y_pos + 0.85, title, fontsize=9.5, fontweight='bold', color=border)
        ax.text(7.15, y_pos + 0.42, desc, fontsize=8.5, color='#212121', va='center')

    plt.tight_layout()
    plt.savefig('diagrams/fig_c1_empathy_map.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved diagrams/fig_c1_empathy_map.png")

if __name__ == '__main__':
    create_fig_c1()
