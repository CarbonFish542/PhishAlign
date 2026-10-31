"""
report_content.py - Exhaustive Academic Content Definitions for PhishAlign Project Report
Contains full text for Preliminaries, Chapters 1 to 10, Bibliography, and Annexures.
"""

# ============================================================
# PRELIMINARY PAGES CONTENT
# ============================================================

CERTIFICATE_TITLE = "CERTIFICATE"
CERTIFICATE_BODY = (
    "This is to certify that the project report entitled \"PHISHALIGN: CROSS-MODAL CONSISTENCY-BASED "
    "PHISHING WEBSITE DETECTION\" is a bonafide work carried out in partial fulfillment "
    "of the requirements for the award of the degree of Bachelor of Technology in Computer Engineering "
    "from Bharati Vidyapeeth (Deemed to be University) College of Engineering, Pune during the academic year 2026-2027.\n\n"
    "To the best of our knowledge, the work reported herein does not form part of any other thesis or dissertation "
    "on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate."
)

DECLARATION_TITLE = "DECLARATION"
DECLARATION_BODY = (
    "We hereby declare that the project entitled \"PHISHALIGN: CROSS-MODAL CONSISTENCY-BASED PHISHING WEBSITE DETECTION\" "
    "is an authentic record of our own work carried out as the final year project for the award of the degree of Bachelor "
    "of Technology in Computer Engineering from Bharati Vidyapeeth (Deemed to be University) College of Engineering, Pune.\n\n"
    "We further declare that we have not submitted this work elsewhere for the award of any degree or diploma. All sources "
    "of literature and technical materials utilized in this research have been duly acknowledged."
)

EXAMINER_APPROVAL_TITLE = "EXAMINER'S APPROVAL CERTIFICATE"
EXAMINER_APPROVAL_BODY = (
    "This project report entitled \"PHISHALIGN: CROSS-MODAL CONSISTENCY-BASED PHISHING WEBSITE DETECTION\" "
    "is approved for the award of the degree of Bachelor of Technology in Computer Engineering.\n\n"
    "Internal Examiner: _______________________          External Examiner: _______________________"
)

ACKNOWLEDGEMENT_TITLE = "ACKNOWLEDGEMENT"
ACKNOWLEDGEMENT_BODY = (
    "We express our deep gratitude and heartfelt thanks to our project guide, Department of Computer "
    "Engineering, Bharati Vidyapeeth (Deemed to be University) College of Engineering, Pune, for constant encouragement, "
    "intellectual guidance, constructive critique, and invaluable suggestions throughout the development of this project.\n\n"
    "We are extremely grateful to the Head of the Department of Computer Engineering for providing us "
    "with excellent computational laboratory infrastructure and administrative support that facilitated this research.\n\n"
    "We also extend our sincere appreciation to the respected Principal for visionary leadership "
    "and institutional encouragement. Finally, we thank our parents, faculty members, and fellow students who supported us "
    "directly and indirectly in bringing this research project to fruition."
)

ABSTRACT_TITLE = "ABSTRACT"
ABSTRACT_BODY = (
    "Phishing attacks remain one of the most pervasive cyber-threats across the modern web ecosystem, increasingly relying "
    "on sophisticated evasion tactics, cloud-hosted reverse proxies, and visual spoofing that easily deceive both human victims "
    "and traditional single-modality security filters. Existing automated defenses generally analyze isolated channels—such as "
    "lexical URL patterns, HTML Document Object Model (DOM) heuristics, or rendered webpage screenshots—or rely on late "
    "concatenation where modality scores are blindly averaged without verifying whether the content across channels agrees. "
    "This fundamental architectural blindness allows sophisticated adversaries to host legitimate-looking pages on unrelated domains "
    "or mimic well-known brand aesthetics while bypassing single-modality alarms.\n\n"
    "To resolve this challenge, this project presents PhishAlign, a novel cross-modal consistency-aware multimodal phishing website "
    "detection system. PhishAlign simultaneously ingests and processes three independent webpage modalities: the URL string, the "
    "HTML DOM structure, and the visual appearance captured via webpage screenshot. Individual base classifiers (XGBoost for lexical "
    "and structural URL features, XGBoost for HTML DOM tree metrics, and MobileNetV3-Small for screenshot visual embeddings) produce "
    "isolated modality threat probabilities. Simultaneously, an Optical Character Recognition (OCR) engine extracts rendered textual tokens, "
    "enabling the computation of twenty-five (25) explicit cross-modal consistency features. These consistency dimensions evaluate pairwise "
    "Jaccard similarity, token containment ratios, and domain-identity overlaps across the URL hostname, HTML body, page title, and "
    "screenshot text. A regularized stacking meta-classifier (Logistic Regression) combines the 3 base probabilities and the 25 consistency "
    "features into a unified 28-dimensional representation to predict the final phishing verdict.\n\n"
    "PhishAlign addresses the needs of distinct user cohorts through a dual-interface architecture: a lightweight Chromium Browser Extension "
    "(Manifest V3) engineered for everyday consumers that performs sub-160ms zero-click evaluations and full-screen threat interception, "
    "and a comprehensive React/Vite Web Analytical Dashboard tailored for SOC analysts and security researchers offering deep forensic "
    "auditing, interactive Jaccard matrix heatmaps, and game-theoretic SHAP feature attributions. Evaluated on 2,757 complete cases from "
    "the official Phish360 benchmark using leak-free group-based partitioning, PhishAlign achieves 96.34% accuracy, 99.40% precision, "
    "95.84% F1-score, and 99.61% ROC-AUC, outperforming conventional equal-weight fusion (+1.03% F1) and probability-only stacking (+1.17% F1) "
    "with statistical significance confirmed via group-bootstrap confidence intervals."
)

# Nomenclature and Abbreviations
NOMENCLATURE_SYMBOLS = [
    ["P_url", "Phishing probability predicted by the URL-only XGBoost classifier [0.0, 1.0]"],
    ["P_html", "Phishing probability predicted by the HTML-only XGBoost classifier [0.0, 1.0]"],
    ["P_visual", "Phishing probability predicted by the screenshot MobileNetV3-Small classifier [0.0, 1.0]"],
    ["P_phish", "Final calibrated phishing probability output by the PhishAlign stacking meta-learner"],
    ["T_url", "Set of meaningful alphanumeric lexical tokens extracted from the URL path and query"],
    ["T_host", "Set of hostname tokens extracted from the domain name excluding generic TLDs"],
    ["T_html", "Set of lowercased alphanumeric tokens extracted from the webpage HTML body text"],
    ["T_ocr", "Set of lowercased optical text tokens extracted from the webpage screenshot via Tesseract OCR"],
    ["T_title", "Set of textual tokens extracted from the HTML `<title>` tag attribute"],
    ["T_domain", "Set of identity-bearing tokens belonging strictly to the registered second-level domain"],
    ["J(A, B)", "Jaccard similarity coefficient between token sets A and B: |A ∩ B| / |A ∪ B|"],
    ["C(A, B)", "Containment ratio of token set A within set B: |A ∩ B| / |A|"],
    ["w^T x + b", "Linear margin produced by the regularized stacking logistic regression meta-learner"],
    ["σ(z)", "Standard logistic sigmoid activation function: 1 / (1 + e^(-z)) converting margin to probability"],
    ["φ_i", "Shapley additive feature attribution value quantifying the marginal contribution of feature i"]
]

NOMENCLATURE_ABBREVIATIONS = [
    ["API", "Application Programming Interface"],
    ["AUC", "Area Under the Curve (specifically ROC-AUC)"],
    ["CORS", "Cross-Origin Resource Sharing"],
    ["CNN", "Convolutional Neural Network"],
    ["CSS", "Cascading Style Sheets"],
    ["DFD", "Data Flow Diagram"],
    ["DNS", "Domain Name System"],
    ["DOM", "Document Object Model"],
    ["DPI", "Dots Per Inch"],
    ["FPR", "False Positive Rate"],
    ["HTTP", "Hypertext Transfer Protocol"],
    ["HTTPS", "Hypertext Transfer Protocol Secure"],
    ["JSON", "JavaScript Object Notation"],
    ["LR", "Logistic Regression"],
    ["ML", "Machine Learning"],
    ["MV3", "Manifest Version 3 (Chrome Extension Specification)"],
    ["OCR", "Optical Character Recognition"],
    ["REST", "Representational State Transfer"],
    ["ROC", "Receiver Operating Characteristic"],
    ["SHAP", "Shapley Additive exPlanations"],
    ["SOC", "Security Operations Center"],
    ["SRS", "Software Requirement Specification"],
    ["SSL", "Secure Sockets Layer"],
    ["TLD", "Top-Level Domain"],
    ["TPR", "True Positive Rate"],
    ["UML", "Unified Modeling Language"],
    ["URI", "Uniform Resource Identifier"],
    ["URL", "Uniform Resource Locator"],
    ["Vite", "Next Generation Frontend Tooling"],
    ["XGBoost", "eXtreme Gradient Boosting"]
]

# Table of Contents Structure
TOC_ITEMS = [
    ("Certificate", "i", False),
    ("Certificate (From Industry / Lab, if any)", "ii", False),
    ("Declaration", "iii", False),
    ("Examiner's Approval Certificate", "iv", False),
    ("Acknowledgement", "v", False),
    ("Abstract", "vi", False),
    ("Contents", "vii", False),
    ("List of Figures", "x", False),
    ("List of Tables", "xi", False),
    ("Nomenclature and Abbreviations", "xii", False),
    ("Chapter 1   INTRODUCTION", "1", True),
    ("1.1   Introduction", "1", False),
    ("1.2   Problem Statement", "2", False),
    ("1.3   Existing Work", "3", False),
    ("1.4   Motivation", "4", False),
    ("1.5   Objectives", "4", False),
    ("1.6   Scope", "5", False),
    ("1.7   Organisation of the Report", "5", False),
    ("Chapter 2   CONCEPTS AND METHODS", "6", True),
    ("2.1   Definitions", "6", False),
    ("2.2   Class Imbalance and Evaluation Metrics", "7", False),
    ("2.3   Gradient Boosted Trees and XGBoost", "8", False),
    ("2.4   Deep Convolutional Vision and MobileNetV3-Small", "9", False),
    ("2.5   Cross-Modal Consistency Theory", "10", False),
    ("2.6   Stacking Meta-Learning Architecture", "11", False),
    ("2.7   Dual-Interface Architecture: Web Analytics vs. Extension Guard", "11", False),
    ("2.8   Technology Stack", "12", False),
    ("Chapter 3   LITERATURE SURVEY", "13", True),
    ("3.1   Lexical and URL-Based Phishing Detection", "13", False),
    ("3.2   Content and DOM-Based Heuristic Classifiers", "14", False),
    ("3.3   Visual Similarity and Screenshot-Based Analysis", "14", False),
    ("3.4   Multimodal Fusion in Cybersecurity", "15", False),
    ("3.5   Browser Extension Real-Time Defense Systems", "16", False),
    ("3.6   Summary of the Surveyed Literature", "16", False),
    ("3.7   Research Gap and PhishAlign Positioning", "17", False),
    ("Chapter 4   PROJECT PLAN", "18", True),
    ("4.1   Development Methodology", "18", False),
    ("4.2   Project Phases and Deliverables", "18", False),
    ("4.3   Project Schedule and Milestones", "19", False),
    ("4.4   Resource Requirements", "20", False),
    ("4.5   Risk Analysis and Mitigation Strategies", "20", False),
    ("Chapter 5   SOFTWARE REQUIREMENT SPECIFICATION", "22", True),
    ("5.1   Project Scope", "22", False),
    ("5.2   Overall Description", "22", False),
    ("5.3   User Classes and Characteristics", "23", False),
    ("5.4   Functional Requirements", "23", False),
    ("5.5   Use Cases", "24", False),
    ("5.6   External Interface Requirements", "25", False),
    ("5.7   Non-Functional Requirements", "26", False),
    ("5.8   Hardware and Software Requirements", "26", False),
    ("Chapter 6   SYSTEM DESIGN", "28", True),
    ("6.1   Architectural Overview", "28", False),
    ("6.2   Design Principles", "29", False),
    ("6.3   Data Flow Diagrams", "29", False),
    ("6.4   Process Flow and Pipeline Architecture", "31", False),
    ("6.5   Sequence Diagram", "32", False),
    ("6.6   Class Design and API Data Contracts", "33", False),
    ("6.7   Feature Engineering Design", "35", False),
    ("6.8   Machine-Learning Engine Design", "37", False),
    ("6.9   Cross-Modal Consistency Engine and Identity Resolution", "38", False),
    ("6.10  Dual-Interface Design: Web Analytics vs. Extension Guard", "39", False),
    ("6.11  Deployment View", "41", False),
    ("6.12  Security, Safety, and Privacy Considerations", "42", False),
    ("Chapter 7   IMPLEMENTATION", "43", True),
    ("7.1   Development Environment", "43", False),
    ("7.2   Dataset Curation and Leak-Free Group-Based Splitting", "43", False),
    ("7.3   Feature Engineering and Consistency Extractor Implementation", "44", False),
    ("7.4   Model Training and Hyperparameter Optimization", "45", False),
    ("7.5   Optical Character Recognition (OCR) and Headless Capture", "46", False),
    ("7.6   Backend REST API Implementation", "47", False),
    ("7.7   Frontend Web Application Implementation", "47", False),
    ("7.8   Browser Extension Implementation", "48", False),
    ("7.9   Implementation Challenges and Solutions Adopted", "49", False),
    ("Chapter 8   RESULTS AND DISCUSSION", "51", True),
    ("8.1   Experimental Setup", "51", False),
    ("8.2   Model Performance and Ablation Analysis", "51", False),
    ("8.3   Statistical Significance and Group-Bootstrap Analysis", "53", False),
    ("8.4   Latency and Computational Budget", "53", False),
    ("8.5   Benchmark Test Scenario Results", "54", False),
    ("8.6   Dual-Interface Evaluation: Webpage View vs. Browser Extension", "55", False),
    ("8.7   Discussion of Findings", "74", False),
    ("Chapter 9   SOFTWARE TESTING", "75", True),
    ("9.1   Testing Objectives and Strategy", "75", False),
    ("9.2   Unit Testing of Feature Engineering and Consistency Math", "75", False),
    ("9.3   Model Validation and Adversarial Stress Testing", "76", False),
    ("9.4   API, Headless Capture, and Integration Testing", "76", False),
    ("9.5   System Testing with Benchmark Phishing Scenarios", "77", False),
    ("9.6   Performance, Latency, and Throughput Testing", "77", False),
    ("9.7   Usability Review and Cross-Browser Verification", "78", False),
    ("9.8   Summary of Test Results", "78", False),
    ("Chapter 10  CONCLUSION AND FUTURE WORK", "79", True),
    ("10.1  Conclusion", "79", False),
    ("10.2  Limitations", "79", False),
    ("10.3  Future Work", "80", False),
    ("BIBLIOGRAPHY", "81", True),
    ("ANNEXURE A: LIST OF PUBLICATIONS AND RESEARCH PAPER", "83", True),
    ("ANNEXURE B: PLAGIARISM REPORT", "84", True),
    ("ANNEXURE C: EMPATHY CHART AND SOLUTION DOCUMENT", "85", True),
    ("ANNEXURE D: PROJECT TRACKER", "86", True)
]

# List of Figures Structure
FIGURES_TOC = [
    ("Figure 1.1: Conventional isolated phishing detection compared with PhishAlign cross-modal fusion", "2"),
    ("Figure 1.2: PhishAlign dual-client ecosystem: Browser Extension for users and Web Dashboard for analysts", "3"),
    ("Figure 2.1: Tri-modality feature space and 25-dimensional cross-modal consistency vector representation", "8"),
    ("Figure 2.2: Stacking classifier architecture combining base modality probabilities and consistency vector", "10"),
    ("Figure 4.1: Iterative and incremental engineering research methodology used for PhishAlign", "18"),
    ("Figure 4.2: PhishAlign project milestone schedule and work breakdown Gantt chart", "19"),
    ("Figure 5.1: Use case diagram of PhishAlign illustrating End User, SOC Analyst, and System Admin interactions", "24"),
    ("Figure 6.1: PhishAlign end-to-end system architecture across ingestion, modeling, and client interfaces", "28"),
    ("Figure 6.2: Dual-interface topology: Webpage detailed analytical dashboard vs. Extension real-time guard", "30"),
    ("Figure 6.3: Data flow diagram, Level 0 (Context diagram)", "30"),
    ("Figure 6.4: Data flow diagram, Level 1 (Decomposed processing pipeline)", "31"),
    ("Figure 6.5: End-to-end scoring, consistency evaluation, and decision policy flowchart", "32"),
    ("Figure 6.6: UML sequence diagram for real-time website scoring and interception", "34"),
    ("Figure 6.7: Conceptual class diagram and component hierarchy of the backend service", "35"),
    ("Figure 6.8: Composition of the 28-dimensional PhishAlign input feature vector", "36"),
    ("Figure 6.9: Cross-modal pairwise Jaccard matrix computation and domain identity overlap analysis", "37"),
    ("Figure 6.10: PhishAlign Browser Extension real-time multi-modal detection pipeline and NLP dynamic identity gate", "38"),
    ("Figure 6.11: Chrome Extension management interface displaying PhishAlign 1.0.0 MV3 Service Worker enabled", "39"),
    ("Figure 6.12: Chrome Extension real-time active scanning overlay banner during background page inspection", "40"),
    ("Figure 6.13: Chrome Extension in action: non-intrusive popup verification on legitimate site (GeeksforGeeks, 0.9% risk)", "41"),
    ("Figure 6.14: Chrome Extension cross-modal calibration on Adobe Photoshop (10.4% risk, overriding visual false alarm)", "42"),
    ("Figure 6.15: Chrome Extension active defense: full-screen blocking overlay on simulated phishing page (100.0% risk)", "43"),
    ("Figure 7.1: Offline model development, leak-free group partitioning, and serialization pipeline", "45"),
    ("Figure 8.1: Model performance comparison across individual modalities and fusion strategies on Phish360", "50"),
    ("Figure 8.2: Receiver Operating Characteristic (ROC) comparative curves on official test partition", "51"),
    ("Figure 8.3: Per-transaction pipeline latency breakdown compared against real-time 200ms interactive budget", "53"),
    ("Figure 8.4: PhishAlign Web Application research prototype landing page", "55"),
    ("Figure 8.5: PhishAlign Web Application real-time 8-stage pipeline analysis progress view", "56"),
    ("Figure 8.6: Web Application Overview tab: Wikipedia legitimate verification (1.1% risk, modality breakdown)", "57"),
    ("Figure 8.7: Web Application URL Analysis tab: Lexical attributes, HTTPS validation, and entropy for Wikipedia", "58"),
    ("Figure 8.8: Web Application HTML Analysis tab: Structural metrics, form count, and external links for Wikipedia", "59"),
    ("Figure 8.9: Web Application Visual Model inspector: MobileNetV3 visual score (72.31%) and OCR metrics", "60"),
    ("Figure 8.10: Web Application Captured Website Analysis: Static rendered page view of Wikipedia", "61"),
    ("Figure 8.11: Web Application Cross-Modal Text Overlap: Tri-modal Jaccard network graph for Wikipedia", "62"),
    ("Figure 8.12: Web Application Text-Overlap Matrix: Pairwise 3x3 Jaccard token overlap for Wikipedia", "63"),
    ("Figure 8.13: Web Application Website Identity Signals: 100.0% Domain-to-Title lexical match for Wikipedia", "64"),
    ("Figure 8.14: Web Application SHAP Live Analysis Evidence: Individual feature contribution breakdown for Wikipedia", "65"),
    ("Figure 8.15: Web Application SHAP TreeExplainer feature importance bar chart pushing score towards legitimacy", "66"),
    ("Figure 8.16: Web Application Overview tab: High Phishing Risk alert (98.2% probability) on typosquatted telegr.am", "67"),
    ("Figure 8.17: Web Application URL Analysis tab: Typosquatted domain, entropy 3.95, and suspicious token detection", "68"),
    ("Figure 8.18: Web Application HTML Analysis tab: Credential harvesting form with 1 password field and 2 external links", "69"),
    ("Figure 8.19: Web Application Captured Website Analysis: Visual inspection of fake Telegram login form (96.7% visual probability)", "70"),
    ("Figure 8.20: Web Application Cross-Modal Text Overlap: Asymmetry detection (HTML-OCR 70% vs URL-HTML 0%)", "71"),
    ("Figure 8.21: Web Application Text-Overlap Matrix and 0.0% Domain Identity Overlap on telegr.am", "72"),
    ("Figure 8.22: Web Application SHAP TreeExplainer feature importance bar chart displaying massive phishing attribution spikes", "73"),
    ("Figure 9.1: Multi-tiered software testing and verification strategy of PhishAlign", "75"),
    ("Figure 10.1: PhishAlign future architectural enhancement and research roadmap", "80"),
    ("Figure C.1: Multi-stakeholder empathy map and user-centered solution architecture", "85")
]

# List of Tables Structure
TABLES_TOC = [
    ("Table 1.1: Existing approaches to transaction and website phishing detection and their drawbacks", "3"),
    ("Table 2.1: Technology stack and engineering libraries utilized in PhishAlign", "12"),
    ("Table 3.1: Summary of the surveyed literature on multimodal and heuristic phishing detection", "16"),
    ("Table 4.1: Project phases, scheduled activities, and concrete deliverables", "19"),
    ("Table 4.2: Identified project risks, severity ratings, and engineered mitigation strategies", "21"),
    ("Table 5.1: User classes and operational characteristics of PhishAlign", "23"),
    ("Table 5.2: Functional requirements specification for ingestion, modeling, and client delivery", "24"),
    ("Table 5.3: Detailed use case specification: Submit and analyze website via web dashboard / extension", "25"),
    ("Table 5.4: Non-functional requirements specification governing latency, accuracy, and security", "26"),
    ("Table 5.5: Minimum and recommended hardware and software development specifications", "27"),
    ("Table 6.1: Backend REST API input payload specifications for `/analyze` and `/analyze-content`", "33"),
    ("Table 6.2: Backend REST API response payload fields, forensic types, and audience mapping", "34"),
    ("Table 6.3: Comprehensive inventory of the 25 Cross-Modal Consistency Features and formulas", "36"),
    ("Table 6.4: Three-tier risk classification policy, decision thresholds, and user alert interventions", "39"),
    ("Table 7.1: Software development tools, frameworks, and utility libraries used in implementation", "44"),
    ("Table 7.2: Machine learning model hyperparameters and optimization configurations", "45"),
    ("Table 7.3: Interface feature comparison: Webpage Detailed View vs. Browser Extension User View", "48"),
    ("Table 7.4: Technical implementation challenges encountered and engineering solutions adopted", "50"),
    ("Table 8.1: Comprehensive model performance benchmark evaluation on Phish360 test set", "52"),
    ("Table 8.2: Per-transaction execution latency breakdown across pipeline processing stages", "53"),
    ("Table 8.3: Evaluation results across seven benchmark phishing and legitimate test scenarios", "55"),
    ("Table 8.4: Unified multi-modal and cross-modal feature attribution ranking for adversarial phishing case", "74"),
    ("Table 9.1: Unit test cases and validation results for feature extraction and consistency math", "75"),
    ("Table 9.2: Decision threshold boundary test cases for risk classification engine", "76"),
    ("Table 9.3: API endpoint integration test suite and status code verification", "76"),
    ("Table 9.4: System test results across live simulated testbed environments", "77"),
    ("Table A.1: Publication details and target peer-reviewed IEEE conference/journal mapping", "83"),
    ("Table B.1: Plagiarism screening results across Turnitin and Urkund verification suites", "84"),
    ("Table C.1: Multi-stakeholder empathy mapping matrix and engineered feature alignment", "85"),
    ("Table D.1: PhishAlign engineering milestone tracker and weekly progress record", "86")
]
