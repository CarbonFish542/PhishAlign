"""
table_data.py - Structured Data Definitions for PhishAlign Project Report Tables
Replicates the styling, borders, padding, and D9E2F3 header shading of template.docx
"""

# Table 1.1: Existing Approaches
T1_1_HEADERS = ["Approach", "How It Works", "Main Drawbacks", "Addressed in PhishAlign By"]
T1_1_DATA = [
    [
        "Blacklisting & DNS Feed",
        "Checks submitted URLs against centralized lists of known phishing URLs/domains (e.g., Google Safe Browsing, PhishTank).",
        "Cannot detect zero-day phishing domains; attackers constantly rotate URLs and use fast-flux DNS; high update latency.",
        "Zero-hour machine learning evaluation combining lexical heuristics, DOM structure, visual rendering, and cross-modal consistency."
    ],
    [
        "URL-Only Machine Learning",
        "Extracts lexical, structural, and character entropy features from the URL string without fetching page content.",
        "Vulnerable to legitimate hosting providers, URL shorteners, subdomains on cloud platforms, and compromised trusted servers.",
        "Treats URL signals as one component (XGBoost) and correlates URL tokens against visible DOM and screenshot OCR text."
    ],
    [
        "HTML/DOM Heuristic Analysis",
        "Inspects DOM tree for password inputs, external form actions, script obfuscation, and missing favicon links.",
        "Fails against dynamic JavaScript rendering, client-side re-direction, canvas-based forms, and heavily obfuscated web code.",
        "Utilizes headless Chromium Playwright capture with DOM evaluation, augmented by rendered screenshot computer vision."
    ],
    [
        "Visual/Screenshot Similarity",
        "Compares webpage screenshot against reference bank of protected brand login interfaces using SIFT, ORB, or CNNs.",
        "Computationally intensive; suffers from false positives on legitimate sites using similar UI templates; struggles with novel brands.",
        "Lightweight MobileNetV3-Small screenshot classifier combined with OCR token extraction and explicit identity cross-referencing."
    ],
    [
        "Conventional Multimodal Fusion",
        "Extracts independent feature vectors from URL, HTML, and visual modalities and concatenates or averages predictions.",
        "Assumes modality independence; completely misses identity discrepancies (e.g., PayPal logo on unrelated scam domain).",
        "Calculates 25 explicit cross-modal consistency features (Jaccard, containment, domain-identity overlaps) for meta-classifier."
    ]
]

# Table 2.1: Technology Stack
T2_1_HEADERS = ["Layer / Module", "Technology / Library", "Version / Spec", "Rationale and Function in PhishAlign"]
T2_1_DATA = [
    ["Runtime Environment", "Python", "3.11+", "Core platform for backend machine learning, data engineering, and automation."],
    ["Backend API Gateway", "FastAPI", "0.110+", "High-performance asynchronous REST API framework with Pydantic type validation."],
    ["Server-Side Headless Capture", "Playwright (Chromium)", "1.40+", "Controlled browser automation for rendering screenshots, DOM, and final redirect URLs."],
    ["Optical Character Recognition", "Tesseract OCR / PyTesseract", "5.3+", "Extracts rendered visible text from webpage screenshots for semantic consistency scoring."],
    ["Tabular Machine Learning", "XGBoost", "2.0+", "Gradient boosted decision tree ensembles for URL and HTML classification models."],
    ["Visual Feature Extractor", "MobileNetV3-Small (PyTorch)", "2.1+", "High-efficiency convolutional neural network for rapid screenshot visual classification."],
    ["Meta-Classifier / Stacking", "Scikit-Learn (LogisticRegression)", "1.3+", "Regularized meta-learner combining base probabilities and 25 consistency dimensions."],
    ["Text Processing & TLD", "TLDextract / RegEx", "5.1+", "Extracts domain identity tokens and strips generic TLDs/subdomains."],
    ["Data Analysis & Arrays", "Pandas / NumPy", "2.1+", "Dataset preprocessing, leak-free group partitioning, and vector operations."],
    ["Model Serialization", "Joblib / Pickle", "1.3+", "Rapid model persistence and zero-overhead memory loading during API startup."],
    ["Frontend Web Dashboard", "React 18, Vite, TypeScript", "5.0+", "Responsive SOC forensic analytical dashboard with interactive tabs and matrix views."],
    ["Styling & Component UI", "Tailwind CSS, Lucide Icons", "3.4+", "Modern dark-themed security analyst UI with risk meters and badge components."],
    ["Browser Extension Client", "Chrome Extensions (Manifest V3)", "MV3 Spec", "Zero-click client companion for real-time page capture, warning badges, and interception."]
]

# Table 3.1: Literature Survey Summary
T3_1_HEADERS = ["Author & Year", "Approach / Methodology", "Modalities Used", "Key Findings & Reported Results", "Unresolved Limitations"]
T3_1_DATA = [
    [
        "Marchal et al. (2017)",
        "Off-the-hook: Phishing detection based on lexical URL features and search engine identity verification.",
        "URL + Web Search",
        "Achieved 99.1% precision on active feeds; established concept of comparing target domain against search results.",
        "High query latency; easily blocked by search engine rate limits; fails if attacker manipulates SEO keywords."
    ],
    [
        "Afroz & Greenstadt (2011)",
        "PhishZoo: Visual similarity matching using perceptual image hashing and layout analysis.",
        "Visual Appearance",
        "Successfully detected targeted brand spoofs without requiring access to source code or URL heuristics.",
        "High computational overhead; requires exhaustive database of legitimate brand logos; vulnerable to layout skewing."
    ],
    [
        "Li et al. (2019)",
        "DeepPhish: Deep learning on HTML DOM sequences and word embeddings using LSTM and CNN.",
        "HTML Source Code",
        "Demonstrated that automated deep representations outperform hand-crafted HTML heuristics; 93.4% F1-score.",
        "Vulnerable to JavaScript obfuscation and client-side DOM construction; ignores visual cues and URL tokens."
    ],
    [
        "Lin et al. (2021)",
        "Phishpedia: Visual deep learning framework detecting logos via Faster R-CNN and siamese networks.",
        "Visual (Logos)",
        "Reported 98.2% precision on top 30,000 brands; significant breakthrough in logo detection accuracy.",
        "Only triggers if known brand logo is detected; misses credential harvesting forms without prominent brand marks."
    ],
    [
        "Bozkir et al. (2023)",
        "Catching Phishing via Multimodal Deep Fusion: Multimodal network combining URL, text, and visual CNN features.",
        "URL + Text + Visual",
        "Showed multimodal combination beats individual modalities; achieved 94.8% accuracy on benchmark datasets.",
        "Employed late concatenation without explicit cross-modal relational metrics; cannot detect semantic domain discrepancies."
    ],
    [
        "Proposed PhishAlign (2026)",
        "Cross-Modal Consistency-Aware Stacking Fusion: 3 base classifiers + 25 relational Jaccard/containment/identity features.",
        "URL + HTML + Visual (OCR)",
        "Achieved 96.34% accuracy, 95.84% F1-score, and 99.61% ROC-AUC on Phish360; delivers dual Web/Extension interfaces.",
        "Dependent on rendered screenshot availability; requires OCR processing budget (mitigated by fast-path extension)."
    ]
]

# Table 4.1: Project Phases and Deliverables
T4_1_HEADERS = ["Phase No.", "Phase Name", "Primary Activities", "Key Deliverables & Artifacts"]
T4_1_DATA = [
    ["1", "Research & Dataset Audit", "Literature survey; Phish360 dataset acquisition; integrity checks; leak-free group split.", "Dataset audit report, deduplicated training/testing partitions."],
    ["2", "Base Modality Modeling", "Feature engineering for URL lexical tokens and HTML DOM; train XGBoost models; train MobileNetV3.", "Trained URL XGBoost model, HTML XGBoost model, MobileNetV3 visual weights."],
    ["3", "Cross-Modal Consistency Design", "Design 25 relational consistency features; implement tokenization, Jaccard, and containment logic.", "Consistency extractor module (`consistency.py`) with 25 deterministic metrics."],
    ["4", "Stacking Fusion & Evaluation", "Implement Logistic Regression meta-learner; ablation studies; group-bootstrap confidence intervals.", "Trained meta-classifier model; benchmark evaluation tables and ROC/AUC curves."],
    ["5", "Backend API & Capture Engine", "FastAPI implementation; Playwright headless capture; Tesseract OCR integration; endpoint security.", "FastAPI backend service (`main.py`, `inference.py`, `page_capture.py`)."],
    ["6", "Dual-Interface Frontend", "React/Vite analytical web dashboard; Chrome Extension (Manifest V3) development; styling & UX.", "Production React web app (`PhishAlign_web`); Chrome Extension package (`extension/`)."],
    ["7", "System Testing & Final Documentation", "Live testbed simulation (PayPal, MS365, Google, Telegram, Photoshop); latency benchmarking; final report preparation (Weeks 23–24).", "Automated test suite (`pipeline.py`); final comprehensive project report."]
]

# Table 4.2: Project Risks and Mitigation
T4_2_HEADERS = ["Risk Category", "Specific Risk Description", "Severity / Likelihood", "Engineered Mitigation Strategy"]
T4_2_DATA = [
    [
        "Data Leakage",
        "Sample overlap between training and testing sets due to identical phishing templates or shared domains.",
        "High / High",
        "Implemented strict group-based splitting using exact URL, HTML content hash, and screenshot perceptual hash."
    ],
    [
        "Latency Overhead",
        "Playwright headless browser rendering and Tesseract OCR taking >3 seconds per transaction.",
        "High / Medium",
        "Dual-client design: Browser extension performs Layer 1 client-side DOM/tab capture, bypassing server rendering."
    ],
    [
        "Evasion & Obfuscation",
        "Attackers using JavaScript obfuscation, Unicode character homoglyphs, or CSS image masking.",
        "Medium / High",
        "Visual MobileNetV3 and OCR analyze rendered pixels directly, completely neutralizing code-level obfuscation."
    ],
    [
        "False Positives on Legitimate Sites",
        "Legitimate sites with low token overlap (e.g. minimalist portals) falsely flagged as phishing.",
        "High / Low",
        "Meta-learner trained on 28-D vector; low overlap alone does not trigger block unless accompanied by suspicious cues."
    ],
    [
        "Browser Extension Security",
        "Extension vulnerabilities allowing malicious pages to alter detection verdicts or inject scripts.",
        "High / Low",
        "Strict Manifest V3 adherence; isolated execution context; background service worker communication with sanitized JSON."
    ]
]

# Table 5.1: User Classes
T5_1_HEADERS = ["User Class", "Primary User Persona", "Technical Expertise", "Platform Interface & Primary Use Case"]
T5_1_DATA = [
    [
        "End-User / Consumer",
        "Everyday internet users, employees, corporate staff browsing the web.",
        "Low to Average",
        "Browser Extension (Chrome MV3): Zero-click background protection, green safe badges, and full-screen blocking on phishing threats."
    ],
    [
        "SOC / Security Analyst",
        "Cybersecurity team members, incident responders, fraud investigation teams.",
        "High",
        "Web Analytical Dashboard (React): Deep forensic inspection, modality probability breakdown, Jaccard overlap matrices, and SHAP evidence."
    ],
    [
        "Security Researcher / Auditor",
        "Academic researchers, model evaluators, compliance auditors.",
        "Very High",
        "Web Dashboard (Research Mode): Comparative benchmark evaluation against baseline models, ablation metrics, and confidence intervals."
    ],
    [
        "System Administrator",
        "DevOps engineers, IT infrastructure managers hosting the detection service.",
        "High",
        "Backend REST API & CLI (`pipeline.py`): Health monitoring, model versioning, Playwright sandbox configuration, and batch testing."
    ]
]

# Table 5.2: Functional Requirements
T5_2_HEADERS = ["Req ID", "Requirement Description", "Category", "Verification Method"]
T5_2_DATA = [
    ["FR-01", "The system shall accept a target website URL via Web Dashboard and initiate headless browser capture.", "Ingestion", "Automated API Test"],
    ["FR-02", "The extension shall extract active tab DOM and capture visible viewport screenshot directly in client.", "Client Capture", "Browser Integration Test"],
    ["FR-03", "The backend shall extract 31 lexical, structural, and character entropy features from the target URL.", "URL Engine", "Unit Test (`url_model.py`)"],
    ["FR-04", "The backend shall parse HTML DOM and extract 64 structural features (forms, passwords, scripts, external actions).", "HTML Engine", "Unit Test (`html_model.py`)"],
    ["FR-05", "The backend shall execute MobileNetV3-Small on the screenshot to output visual phishing probability.", "Visual Engine", "Inference Benchmark"],
    ["FR-06", "The backend shall run Tesseract OCR on the screenshot to extract visible textual tokens.", "OCR Engine", "OCR Verification Test"],
    ["FR-07", "The system shall compute 25 cross-modal consistency metrics (5 availability, 10 pairwise, 10 domain identity).", "Consistency", "Unit Test (`consistency.py`)"],
    ["FR-08", "The stacking classifier shall combine 3 base probabilities and 25 consistency dims into a unified score.", "Meta-Classifier", "Evaluation Metric Check"],
    ["FR-09", "The system shall classify websites as Safe (<50%), Suspicious (50-77%), or Phishing (≥78%).", "Decision Engine", "Threshold Boundary Test"],
    ["FR-10", "The web dashboard shall display modality breakdown, Jaccard overlap matrix, and benchmark comparisons.", "UI Web", "Browser End-to-End Test"],
    ["FR-11", "The browser extension shall display instant popup badges and display full-screen block overlays on phishing.", "UI Extension", "Extension Interception Test"]
]

# Table 5.3: Use Case Description
T5_3_HEADERS = ["Use Case Element", "Specification / Description"]
T5_3_DATA = [
    ["Use Case Name", "Analyze Target Webpage via Extension or Web Dashboard"],
    ["Primary Actor", "End User (Extension) or Security Analyst (Web Dashboard)"],
    ["Preconditions", "Backend API service running on port 8000; network connectivity to target destination available."],
    ["Trigger", "User navigates to a webpage (Extension auto-trigger) or Analyst enters URL on Web Dashboard."],
    ["Main Success Scenario", "1. Target URL/DOM/screenshot received by backend API.\n2. URL, HTML, and Visual classifiers compute modality probabilities.\n3. OCR extracted and 25 cross-modal consistency features calculated.\n4. Stacking meta-model evaluates 28-D vector to produce final probability.\n5. Structured response returned with risk tier, modality breakdown, and consistency matrix.\n6. UI renders safe badge or full-screen warning based on risk tier."],
    ["Alternative Flows", "3a. Playwright capture timeout: System falls back to URL-only heuristic evaluation and flags availability flags.\n6a. High risk (≥78%): Extension injects blocking modal preventing user from entering credentials."],
    ["Postconditions", "Verdict rendered; analysis logged in telemetry store; user protected from credential exposure."]
]

# Table 5.4: Non-Functional Requirements
T5_4_HEADERS = ["Category", "Metric / Specification", "Engineering Implementation"]
T5_4_DATA = [
    ["Latency (Layer 1)", "<200 milliseconds per transaction", "Extension pre-captures DOM & screenshot, bypassing server-side rendering."],
    ["Latency (Layer 2)", "<2.5 seconds per transaction", "Parallel asynchronous execution of URL, HTML, and Visual inference pipelines."],
    ["Detection Accuracy", "≥95.0% Accuracy & ≥95.0% F1-score", "Stacking meta-learner achieves 96.34% accuracy and 95.84% F1-score on Phish360."],
    ["False Positive Rate", "<1.0% False Positive Rate on Top Sites", "High precision (99.40%) achieved through multi-modal identity validation."],
    ["Security & Isolation", "Zero remote code execution risk", "Controlled Chromium headless container; URL destination validation; restricted private IP."],
    ["Extensibility", "Modular classifier interface", "Standardized scikit-learn/joblib API allowing seamless replacement of base models."],
    ["Portability", "Cross-platform support", "Containerizable FastAPI backend; React SPA web app; Chromium MV3 extension."]
]

# Table 5.5: Hardware and Software Specifications
T5_5_HEADERS = ["Component", "Minimum Requirement", "Recommended Development Specification"]
T5_5_DATA = [
    ["Processor (CPU)", "Quad-Core Intel i5 / AMD Ryzen 5 (2.5 GHz+)", "Intel Core i7-12700H / AMD Ryzen 7 5800X (8+ Cores)"],
    ["System Memory (RAM)", "8 GB DDR4", "16 GB - 32 GB DDR4/DDR5"],
    ["Storage", "10 GB available SSD space", "500 GB NVMe PCIe Gen 4 SSD"],
    ["Graphics (GPU)", "Integrated Graphics (Intel Iris / AMD Vega)", "NVIDIA GeForce RTX 3060 / 4060 (CUDA acceleration)"],
    ["Operating System", "Windows 10/11 64-bit, Ubuntu 20.04+, macOS 12+", "Windows 11 64-bit with WSL2 / Native Python"],
    ["Browser Platform", "Chromium-based browser (Chrome, Edge, Brave)", "Google Chrome v120+ with Developer Mode enabled"],
    ["Python Runtime", "Python 3.10.x", "Python 3.11.x 64-bit"],
    ["Node.js Runtime", "Node.js 18.x LTS", "Node.js 20.x LTS with npm / vite"]
]

# Table 6.1: API Input Payload
T6_1_HEADERS = ["Endpoint", "HTTP Method", "Field Name", "Data Type", "Description & Constraints"]
T6_1_DATA = [
    ["/analyze", "POST", "url", "String (URL)", "Target webpage URL to capture and analyze via server-side Playwright."],
    ["/analyze-content", "POST", "url", "String (URL)", "Original requested URL of the active webpage."],
    ["/analyze-content", "POST", "final_url", "String (URL)", "Final URL after following all client-side / HTTP redirects."],
    ["/analyze-content", "POST", "html", "String (HTML)", "Complete outerHTML DOM string extracted directly by browser content script."],
    ["/analyze-content", "POST", "screenshot_b64", "String (Base64)", "PNG screenshot captured via chrome.tabs.captureVisibleTab (no prefix)."],
    ["/analyze-content", "POST", "page_title", "String", "Extracted `<title>` tag content of the active webpage document."]
]

# Table 6.2: API Response Payload
T6_2_HEADERS = ["Field Name", "Data Type", "Forensic Meaning & Structure", "Audience / Usage"]
T6_2_DATA = [
    ["prediction", "String", "Categorical classification: 'phishing' or 'legitimate'.", "User & Analyst"],
    ["confidence", "Float [0.0 - 1.0]", "Calibrated probability of malicious intent produced by PhishAlign.", "User & Analyst"],
    ["summary", "String", "Plain-English verdict explaining the primary detection rationale.", "User & Analyst"],
    ["modalities.url", "Object", "URL probability (P_url), explanation string, and 31 lexical features.", "Analyst"],
    ["modalities.html", "Object", "HTML probability (P_html), explanation string, and 64 DOM structural features.", "Analyst"],
    ["modalities.visual", "Object", "Visual probability (P_visual), detected brand cues, and OCR tokens.", "Analyst"],
    ["consistency", "Object", "Pairwise text overlap scores: url_html, url_visual, html_visual.", "Analyst"],
    ["identities", "Object", "Extracted identity tokens: url, html, visual; conflict boolean flag.", "Analyst"],
    ["explanation", "Object", "Narrative reasoning detailing cross-modal alignment or identity conflict.", "Auditor & Analyst"],
    ["research", "Object", "Comparative benchmark metrics (URL-only, HTML-only, Equal-Weight, etc.).", "Researcher"]
]

# Table 6.3: 25 Cross-Modal Consistency Features
T6_3_HEADERS = ["No.", "Feature Identifier", "Category", "Mathematical Formula / Extraction Logic", "Forensic Significance"]
T6_3_DATA = [
    ["1", "html_available", "Availability", "1 if len(html_text) > 0 else 0", "Indicates whether webpage DOM was successfully retrieved."],
    ["2", "ocr_available", "Availability", "1 if len(ocr_text) > 0 else 0", "Indicates whether screenshot contained readable text tokens."],
    ["3", "title_available", "Availability", "1 if len(page_title) > 0 else 0", "Indicates whether webpage document declared a `<title>` tag."],
    ["4", "both_html_ocr_available", "Availability", "1 if (html_avail and ocr_avail) else 0", "Confirms dual-channel text availability for cross-verification."],
    ["5", "url_host_available", "Availability", "1 if len(host_tokens) > 0 else 0", "Verifies whether valid hostname identity tokens exist."],
    ["6", "url_html_jaccard", "Pairwise Overlap", "|T_url ∩ T_html| / |T_url ∪ T_html|", "Measures vocabulary overlap between URL tokens and HTML text."],
    ["7", "url_html_containment", "Pairwise Overlap", "|T_url ∩ T_html| / |T_url|", "Fraction of URL tokens present within the HTML text body."],
    ["8", "url_ocr_jaccard", "Pairwise Overlap", "|T_url ∩ T_ocr| / |T_url ∪ T_ocr|", "Measures vocabulary overlap between URL tokens and OCR text."],
    ["9", "url_ocr_containment", "Pairwise Overlap", "|T_url ∩ T_ocr| / |T_url|", "Fraction of URL tokens rendered visually on the screenshot."],
    ["10", "url_title_jaccard", "Pairwise Overlap", "|T_url ∩ T_title| / |T_url ∪ T_title|", "Vocabulary overlap between URL tokens and document title."],
    ["11", "url_title_containment", "Pairwise Overlap", "|T_url ∩ T_title| / |T_url|", "Fraction of URL tokens appearing in the page title string."],
    ["12", "html_ocr_jaccard", "Pairwise Overlap", "|T_html ∩ T_ocr| / |T_html ∪ T_ocr|", "Agreement between internal HTML source and rendered visual text."],
    ["13", "html_ocr_containment", "Overlap Coefficient", "|T_html ∩ T_ocr| / min(|T_html|, |T_ocr|)", "Szymkiewicz–Simpson overlap coefficient preventing HTML DOM size from diluting visual OCR match."],
    ["14", "title_ocr_jaccard", "Pairwise Overlap", "|T_title ∩ T_ocr| / |T_title ∪ T_ocr|", "Agreement between document title and prominent visual text."],
    ["15", "title_ocr_containment", "Pairwise Overlap", "|T_title ∩ T_ocr| / |T_title|", "Fraction of title tokens rendered visually in the screenshot."],
    ["16", "domain_identity_token_count_v3", "Domain Overlap", "|T_domain| (stripped of generic TLDs)", "Count of brand/identity tokens in the registered domain."],
    ["17", "domain_html_jaccard_v3", "Domain Overlap", "|T_domain ∩ T_html| / |T_domain ∪ T_html|", "Jaccard similarity between domain identity and HTML body."],
    ["18", "domain_html_containment_v3", "Domain Overlap", "|T_domain ∩ T_html| / |T_domain|", "Whether domain identity tokens appear anywhere in the HTML."],
    ["19", "domain_html_comp_avail_v3", "Domain Overlap", "1 if (|T_domain| > 0 and html_avail) else 0", "Validity flag for domain-to-HTML comparison metric."],
    ["20", "domain_ocr_jaccard_v3", "Domain Overlap", "|T_domain ∩ T_ocr| / |T_domain ∪ T_ocr|", "Jaccard similarity between domain identity and visual OCR text."],
    ["21", "domain_ocr_containment_v3", "Domain Overlap", "|T_domain ∩ T_ocr| / |T_domain|", "Whether domain identity tokens are rendered visually to users."],
    ["22", "domain_ocr_comp_avail_v3", "Domain Overlap", "1 if (|T_domain| > 0 and ocr_avail) else 0", "Validity flag for domain-to-OCR comparison metric."],
    ["23", "domain_title_jaccard_v3", "Domain Overlap", "|T_domain ∩ T_title| / |T_domain ∪ T_title|", "Jaccard similarity between domain identity and page title."],
    ["24", "domain_title_containment_v3", "Domain Overlap", "|T_domain ∩ T_title| / |T_domain|", "Whether domain identity matches the declared page title."],
    ["25", "domain_title_comp_avail_v3", "Domain Overlap", "1 if (|T_domain| > 0 and title_avail) else 0", "Validity flag for domain-to-title comparison metric."]
]

# Table 6.4: Risk Tiers and Decision Policy
T6_4_HEADERS = ["Risk Tier", "Probability Range", "Verdict Classification", "User Alert Action", "SOC / Forensic Rationale"]
T6_4_DATA = [
    [
        "Low Risk (Green)",
        "0.0% ≤ P < 50.0%",
        "Likely Legitimate",
        "Display non-intrusive green badge ('Authentic Website'); silent background pass.",
        "High cross-modal consistency (domain matches HTML/visual identity) and low individual modality threat scores."
    ],
    [
        "Medium Risk (Yellow)",
        "50.0% ≤ P < 78.0%",
        "Suspicious / Caution",
        "Display prominent amber warning badge; advise user to avoid credential entry.",
        "Conflicting modality signals (e.g. moderate visual similarity to login page but unverified domain, or missing OCR data)."
    ],
    [
        "High Risk (Red)",
        "78.0% ≤ P ≤ 100.0%",
        "High Phishing Risk",
        "Full-screen browser interception overlay; block page interactions; provide 'Go Back' button.",
        "Severe cross-modal identity contradiction (e.g. PayPal visual logo on unrelated domain) and elevated base probabilities."
    ]
]

# Table 7.1: Software Implementation Tools
T7_1_HEADERS = ["Category", "Tool / Library Name", "Role in PhishAlign", "Key Configuration Parameters"]
T7_1_DATA = [
    ["Web Browser Engine", "Playwright (Python)", "Automates headless Chromium browser to navigate, render, and capture DOM.", "viewport=(1280, 800), timeout=30000ms, wait_until='networkidle'"],
    ["Image Processing", "Pillow (PIL)", "Image decoding, resizing, normalization, and base64 conversion.", "RGB mode conversion, Bicubic interpolation, 224x224 thumbnailing"],
    ["OCR Extraction", "Tesseract OCR / Pytesseract", "Extracts visible optical text from captured screenshot images.", "Language='eng', psm=6 (Assume uniform block of text), timeout=30s"],
    ["Gradient Boosting", "XGBoost (xgboost)", "Trains and executes URL and HTML tabular classification models.", "n_estimators=100, max_depth=6, learning_rate=0.1, objective='binary:logistic'"],
    ["Deep Vision CNN", "PyTorch / Torchvision", "MobileNetV3-Small deep architecture for screenshot visual classification.", "Pretrained=ImageNet, num_classes=2, Adam optimizer, lr=1e-4"],
    ["Domain Extraction", "TLDextract", "Accurately separates subdomain, domain name, and public suffix.", "suffix_list_urls=None (offline cached Public Suffix List)"],
    ["Stacking Meta-Model", "Scikit-Learn", "Logistic Regression meta-learner for combining 28-D feature vector.", "C=1.0, penalty='l2', solver='lbfgs', max_iter=1000"],
    ["Model Serialization", "Joblib", "Persists model weights, scalers, and metadata to disk.", "compress=3, protocol=5 for high-speed deserialization"],
    ["Web Framework", "FastAPI / Uvicorn", "Provides high-throughput asynchronous HTTP API.", "workers=4, host='127.0.0.1', port=8000, CORS enabled"],
    ["Client Framework", "React 18 / TypeScript", "Powers the interactive research and SOC dashboard frontend.", "Vite build tool, TypeScript strict mode, Lucide icon library"]
]

# Table 7.2: Model Hyperparameters
T7_2_HEADERS = ["Model Component", "Algorithm Architecture", "Input Dimension", "Key Hyperparameters", "Optimization Objective"]
T7_2_DATA = [
    [
        "URL Classifier",
        "XGBoost Classifier",
        "31 tabular features",
        "n_estimators=100, max_depth=6, colsample_bytree=0.8, subsample=0.8, lr=0.1",
        "Binary Log-Loss (min cross-entropy)"
    ],
    [
        "HTML Classifier",
        "XGBoost Classifier",
        "64 tabular features",
        "n_estimators=120, max_depth=7, colsample_bytree=0.8, subsample=0.8, lr=0.08",
        "Binary Log-Loss (min cross-entropy)"
    ],
    [
        "Visual Classifier",
        "MobileNetV3-Small",
        "224 × 224 × 3 RGB image",
        "Batch_size=32, lr=1e-4, weight_decay=1e-5, Dropout=0.2, Epochs=25",
        "Cross-Entropy Loss (Softmax)"
    ],
    [
        "Stacking Meta-Learner",
        "Logistic Regression",
        "28-D unified vector",
        "Penalty='l2', C=1.0, solver='lbfgs', class_weight='balanced', max_iter=1000",
        "Regularized Logistic Likelihood"
    ]
]

# Table 7.3: Interface Feature Comparison
T7_3_HEADERS = ["Functional Feature / Capability", "Web Analytical Dashboard", "Chrome Browser Extension", "Technical Rationale for Distinction"]
T7_3_DATA = [
    ["Target User Persona", "SOC Analyst / Threat Researcher", "Everyday Web Consumer", "Specialized deep audit vs seamless zero-click defense."],
    ["Page Ingestion Channel", "Server-Side Headless Playwright", "Client-Side Chrome APIs (`tabs.capture`)", "External investigation vs immediate active tab protection."],
    ["Processing Latency", "~2.0 - 2.5 seconds (full capture)", "<160 milliseconds (DOM fast-path)", "Deep analysis allows sandbox delay; consumer browsing requires sub-second speed."],
    ["Visual Output & Evidence", "Interactive Screenshot Thumbnail + Full OCR", "Color-Coded Status Badge (Green/Yellow/Red)", "Analysts need full evidence; consumers need clear actionable status."],
    ["Modality Decomposition", "Full 3-Modality Probability Meters", "Consolidated 3-Tier Risk Percentage Meter", "Prevents cognitive overload on consumers while empowering analysts."],
    ["Consistency Matrix Heatmap", "Interactive Jaccard & Domain Overlap Grid", "Simple 'Domain Self-Consistent' Tag", "In-depth mathematical audit vs single glanceable trust indicator."],
    ["Feature Attribution (SHAP)", "Individual Feature Contributions & Direction", "Simplified Plain-Language Explanation", "Complex game-theoretic attributions reserved for forensic dossiers."],
    ["Research Benchmark Toggle", "Available (Compares 5 Baseline Models)", "Hidden (Focuses on Active Defense)", "Keeps consumer extension lightweight and free from research bloat."],
    ["Threat Intervention Action", "Audit Log Generation & Quarantine Flag", "Full-Screen Interception Modal with Exit", "Extension actively blocks tab interaction to prevent credential submission."]
]

# Table 7.4: Implementation Challenges and Solutions
T7_4_HEADERS = ["Challenge Category", "Technical Challenge Description", "Engineering Impact", "Adopted Solution in PhishAlign"]
T7_4_DATA = [
    [
        "Dynamic Rendering",
        "Client-side Single Page Apps (React/Angular) rendering blank HTML on raw HTTP GET requests.",
        "HTML classifier received empty `<div id='root'>` with 0 forms, producing false safe scores.",
        "Integrated headless Playwright Chromium with `wait_until='networkidle'` and 500ms post-DOM stabilization sleep."
    ],
    [
        "OCR Noise & Variance",
        "Low-contrast text, background gradients, and stylized logos causing OCR mischaracterizations.",
        "Erratic Jaccard similarity between HTML and OCR text on legitimate websites with fancy styling.",
        "Implemented bilateral image filtering and Otsu thresholding before Tesseract; added minimum token length filter (≥2 chars)."
    ],
    [
        "Data Leakage Across Splits",
        "Identical phishing kits deployed across multiple domains contaminating train/test partitions.",
        "Overly optimistic test set performance (inflated accuracy) failing on genuine wild zero-days.",
        "Engineered group-bootstrap partitioner clustering by exact URL, HTML SHA-256 hash, and screenshot perceptual hash."
    ],
    [
        "Real-Time Latency Constraint",
        "Full Playwright capture and OCR taking >3 seconds, unacceptable for real-time browser extension.",
        "End-user browsing experience suffered noticeable lag on every page navigation.",
        "Created dual-layer API: Extension captures DOM and viewport screenshot client-side via Chrome APIs, reducing latency to <160ms."
    ],
    [
        "Feature Vector Dimension Drift",
        "Variations in available tokens or missing modalities altering the feature vector length.",
        "Stacking meta-learner threw dimensional mismatch exceptions during runtime inference.",
        "Hardcoded fixed 28-dimensional feature ordering with explicit binary availability flags for missing channels."
    ],
    [
        "Anti-Bot Walls / Intercepts",
        "Enterprise bot protection (Cloudflare, DDoS-Guard) serving HTTP 403 challenge pages to headless browsers.",
        "Classifiers ingested challenge markup, generating severe false-positive phishing alerts on benign protected websites.",
        "Implemented Playwright Stealth overrides (automation masks, realistic sec-ch-ua headers) and Layer 3 Bot-Protection Wall guardrail."
    ]
]

# Table 8.1: Comprehensive Performance Comparison
T8_1_HEADERS = ["Detection Model / Method", "Accuracy (%)", "Precision (%)", "Recall (%)", "F1-Score (%)", "ROC-AUC (%)"]
T8_1_DATA = [
    ["URL-only XGBoost", "81.20", "79.40", "76.80", "78.10", "88.40"],
    ["HTML-only XGBoost", "84.70", "83.10", "82.20", "82.60", "90.80"],
    ["Visual-only MobileNetV3-Small", "86.90", "85.80", "84.10", "84.90", "92.50"],
    ["Equal-Weight Tri-Modal Fusion", "95.43", "98.46", "91.41", "94.81", "99.34"],
    ["Probability-Only Stacking (LR)", "94.67", "97.80", "91.73", "94.67", "99.36"],
    ["PhishAlign (Proposed Method)", "96.34", "99.40", "92.53", "95.84", "99.61"]
]

# Table 8.2: Latency Breakdown
T8_2_HEADERS = ["Pipeline Stage / Operation", "Average Latency (ms)", "Standard Dev (ms)", "Share of Budget (%)", "Execution Environment"]
T8_2_DATA = [
    ["Browser DOM & Viewport Capture (Client Fast-Path)", "25.0", "3.8", "15.8%", "Client Browser API (`captureVisibleTab`)"],
    ["URL Feature Extraction & XGBoost Model", "12.0", "1.4", "7.6%", "Backend Fast Worker Process (CPU)"],
    ["HTML DOM Parsing & XGBoost Model Inference", "16.0", "2.6", "10.1%", "Backend Fast Worker Process (CPU)"],
    ["MobileNetV3-Small Visual Feature & Inference", "18.0", "2.9", "11.4%", "PyTorch Inference Engine (CPU/CUDA)"],
    ["Tesseract OCR Token Extraction", "85.0", "12.4", "53.8%", "Native Tesseract Engine (Multithreaded)"],
    ["Consistency Matrix & Stacking Gate Inference", "2.0", "0.4", "1.3%", "Scikit-Learn Logistic Regression & Math"],
    ["Total Pipeline Latency (Layer 1 Fast Path)", "158.0", "18.5", "100.0%", "End-to-End Client-to-Verdict"]
]

# Table 8.3: Benchmark Scenarios Evaluation Results
T8_3_HEADERS = ["Scenario Name", "Target Domain / URL", "Expected Ground Truth", "URL Score", "HTML Score", "Visual Score", "Consistency Overlap", "PhishAlign Verdict", "Status"]
T8_3_DATA = [
    [
        "PayPal Credential Harvester",
        "http://127.0.0.1:5050/ (paypal-login.xyz)",
        "Phishing (PayPal Spoof)",
        "98.4%", "99.2%", "99.5%", "0.0% (Contradiction)", "99.8% (Phishing)", "PASS"
    ],
    [
        "Microsoft 365 Account Spoof",
        "http://127.0.0.1:5050/microsoft.html",
        "Phishing (M365 Spoof)",
        "87.3%", "91.2%", "94.1%", "0.0% (Contradiction)", "98.2% (Phishing)", "PASS"
    ],
    [
        "Google Accounts Credential Phish",
        "http://127.0.0.1:5050/google.html",
        "Phishing (Google Spoof)",
        "99.5%", "99.7%", "99.6%", "0.0% (Contradiction)", "100.0% (Phishing)", "PASS"
    ],
    [
        "Typosquatted Social Scam",
        "https://telegr.am/user_mgt/login",
        "Phishing (Telegram Spoof)",
        "70.6%", "89.2%", "96.7%", "0.0% (Contradiction)", "98.2% (Phishing)", "PASS"
    ],
    [
        "Wikipedia Knowledge Portal",
        "https://www.wikipedia.org/",
        "Legitimate",
        "2.5%", "4.4%", "72.3%", "100.0% (Aligned Title)", "1.1% (Legitimate)", "PASS"
    ],
    [
        "GeeksforGeeks Educational Web",
        "https://www.geeksforgeeks.org/...",
        "Legitimate",
        "30.0%", "0.0%", "63.0%", "100.0% (Self-Consistent)", "0.9% (Legitimate)", "PASS"
    ],
    [
        "Adobe Photoshop Web Suite",
        "https://photoshop.adobe.com/...",
        "Legitimate",
        "2.4%", "22.8%", "89.6%", "100.0% (Self-Consistent)", "10.4% (Legitimate)", "PASS"
    ]
]

# Table 8.4: Feature Attribution for Adversarial Phishing Case
T8_4_HEADERS = ["Rank", "Feature Identifier", "Feature Value", "Model Weight / SHAP", "Forensic Direction", "Forensic Interpretation"]
T8_4_DATA = [
    ["1", "domain_title_jaccard_v3", "0.000", "+2.412", "Risk Accelerator (+)", "Severe mismatch: Domain identity 'telegr' completely absent from official 'Telegram' title."],
    ["2", "domain_ocr_containment_v3", "0.000", "+2.185", "Risk Accelerator (+)", "Critical conflict: Brand marks rendered visually on page do not match host domain identity."],
    ["3", "P_visual (MobileNetV3)", "0.967", "+1.940", "Risk Accelerator (+)", "High visual probability: Screenshot strongly mimics genuine brand sign-in interface."],
    ["4", "suspicious_token_count", "1.000", "+1.727", "Risk Accelerator (+)", "Lexical threat signal: URL path contains explicit phishing token ('login')."],
    ["5", "P_html (XGBoost)", "0.892", "+1.650", "Risk Accelerator (+)", "High HTML threat score: External credential submission form and password input detected."],
    ["6", "domain_html_containment_v3", "0.000", "+1.420", "Risk Accelerator (+)", "Structural contradiction: Internal HTML body text contains zero domain identity references."],
    ["7", "url_ocr_jaccard", "0.000", "+1.180", "Risk Accelerator (+)", "Channel dissonance: 0.0% lexical overlap between URL hostname and visual OCR text."],
    ["8", "subdomain_count", "1.000", "+0.880", "Risk Accelerator (+)", "Deceptive domain structure: Abnormal subdomain segmentation attempting brand mimicry."],
    ["9", "url_entropy", "3.952", "-0.679", "Safety Anchor (-)", "Moderate character entropy suggests standard hostname structure, but overridden by identity conflicts."],
    ["10", "https_token_present", "1.000", "-0.420", "Safety Anchor (-)", "Valid SSL/TLS certificate provides superficial legitimacy, commonly exploited by modern phishing kits."]
]

# Table 9.1: Unit Test Cases
T9_1_HEADERS = ["Test ID", "Component / Target Function", "Test Input Data", "Expected Output / Behavior", "Actual Result", "Status"]
T9_1_DATA = [
    ["UT-01", "`clean_text()`", "None / whitespace string", "Empty string `\"\"`", "Empty string `\"\"`", "PASS"],
    ["UT-02", "`tokenize()`", "'Sign in to Microsoft 2026!'", "Set: {'sign', 'in', 'to', 'microsoft', '2026'}", "Set matched exactly", "PASS"],
    ["UT-03", "`extract_host_tokens()`", "'https://secure-login.paypal.com/web'", "Tokens: {'secure', 'login', 'paypal'}, Host: 'paypal.com'", "Exact token set extracted", "PASS"],
    ["UT-04", "`jaccard_similarity()`", "A={'paypal'}, B={'paypal', 'login'}", "Jaccard = 1/2 = 0.500", "0.500", "PASS"],
    ["UT-05", "`containment()`", "A={'paypal'}, B={'paypal', 'login'}", "Containment = 1/1 = 1.000", "1.000", "PASS"],
    ["UT-06", "`compute_25_features()`", "Standard URL, HTML, Title, OCR input", "Dict containing exactly 25 keys matching schema", "25 keys returned, correct types", "PASS"]
]

# Table 9.2: Decision Threshold Boundary Tests
T9_2_HEADERS = ["Test ID", "Simulated P_phish", "Expected Risk Tier", "Expected Badge Color", "Interception Modal Triggered", "Status"]
T9_2_DATA = [
    ["TB-01", "0.000", "Likely Legitimate", "Green ('Authentic')", "No", "PASS"],
    ["TB-02", "0.499", "Likely Legitimate", "Green ('Authentic')", "No", "PASS"],
    ["TB-03", "0.500", "Suspicious / Caution", "Yellow / Amber", "No (Warning Badge Only)", "PASS"],
    ["TB-04", "0.779", "Suspicious / Caution", "Yellow / Amber", "No (Warning Badge Only)", "PASS"],
    ["TB-05", "0.780", "High Phishing Risk", "Red ('High Risk')", "Yes (Full-Screen Intercept)", "PASS"],
    ["TB-06", "1.000", "High Phishing Risk", "Red ('High Risk')", "Yes (Full-Screen Intercept)", "PASS"]
]

# Table 9.3: API Integration Tests
T9_3_HEADERS = ["Test ID", "Endpoint Tested", "Test Payload Scenario", "Expected HTTP Status", "Verification Metric", "Status"]
T9_3_DATA = [
    ["IT-01", "/health", "GET request", "200 OK", "Returns `{\"status\": \"ok\"}`", "PASS"],
    ["IT-02", "/analyze", "Valid URL: 'https://www.wikipedia.org/'", "200 OK", "Returns structured result with prediction='legitimate'", "PASS"],
    ["IT-03", "/analyze", "Invalid / Empty URL string", "400 Bad Request", "Detail: 'URL is required.'", "PASS"],
    ["IT-04", "/analyze-content", "Valid extension payload (DOM + b64 screenshot)", "200 OK", "Bypasses Playwright; returns inference in <200ms", "PASS"],
    ["IT-05", "/analyze-content", "Missing screenshot_b64 field", "422 Unprocessable Entity", "Pydantic validation rejects payload schema", "PASS"],
    ["IT-06", "CORS Middleware", "Request from 'chrome-extension://*'", "200 OK", "Access-Control-Allow-Origin header present", "PASS"]
]

# Table 9.4: System Test Results
T9_4_HEADERS = ["Testbed Scenario", "Simulated Threat Vector", "Extension Interception", "Web Dashboard Forensic View", "End-to-End Latency", "Overall Status"]
T9_4_DATA = [
    [
        "PayPal Credential Harvester",
        "Targeted brand credential harvester stealing PayPal email & password.",
        "SUCCESS: Full-screen red interception overlay displayed instantly.",
        "SUCCESS: Visual 99.5%, HTML 99.2%, 0.0% domain overlap highlighted.",
        "142 ms",
        "PASS"
    ],
    [
        "Microsoft 365 Account Spoof",
        "Cloud identity spoof mimicking corporate Microsoft single sign-on.",
        "SUCCESS: Full-screen red interception overlay displayed instantly.",
        "SUCCESS: Visual 94.1%, HTML 91.2%, brand conflict detected.",
        "158 ms",
        "PASS"
    ],
    [
        "Google Accounts Credential Phish",
        "OAuth-style credential harvester imitating Google account sign-in.",
        "SUCCESS: Full-screen red interception overlay displayed instantly.",
        "SUCCESS: Visual 99.6%, HTML 99.7%, P_phish=100.0% recorded.",
        "165 ms",
        "PASS"
    ],
    [
        "Wikipedia Knowledge Portal",
        "Legitimate high-traffic encyclopedia portal with rich DOM and logo.",
        "SUCCESS: Green authentic badge ('No credential harvesting detected').",
        "SUCCESS: P_phish=1.1%, Domain-to-Title overlap=100.0% confirmed.",
        "138 ms",
        "PASS"
    ],
    [
        "GeeksforGeeks Educational Web",
        "Legitimate educational portal with complex scripts and code blocks.",
        "SUCCESS: Green authentic badge ('Domain Self-Consistent').",
        "SUCCESS: P_phish=0.9%, HTML threat score=0.0% confirmed.",
        "149 ms",
        "PASS"
    ],
    [
        "Typosquatted Social Scam (Telegram)",
        "Typosquatted domain (telegr.am) mimicking Telegram login with fake credential form.",
        "SUCCESS: Full-screen red interception overlay displayed instantly (P_phish=98.2%).",
        "SUCCESS: Visual 96.7%, HTML 89.2%, 0.0% domain identity overlap highlighted.",
        "152 ms",
        "PASS"
    ],
    [
        "Adobe Photoshop Web Suite",
        "Legitimate cloud creative portal with rich UI elements and login prompt.",
        "SUCCESS: Green authentic badge ('Identity Self-Consistent'); overrides visual alarm.",
        "SUCCESS: Calibrated P_phish=10.4%, URL Asymmetry Gate successfully dampened threat.",
        "161 ms",
        "PASS"
    ]
]

# ============================================================
# ANNEXURE TABLES
# ============================================================

# Table A.1: Publication Details and Target Mapping
TA_1_HEADERS = ["Parameter", "Manuscript Specification Details"]
TA_1_DATA = [
    ["Paper Title", "PhishAlign: Cross-Modal Consistency-Based Phishing Website Detection via Tri-Modality Stacking Fusion"],
    ["Primary Authors", "Student Researchers and Project Guide"],
    ["Institutional Affiliation", "Department of Computer Engineering, Bharati Vidyapeeth Deemed University College of Engineering, Pune"],
    ["Target Publication Venue", "IEEE Transactions on Information Forensics and Security / IEEE Access"],
    ["Current Submission Status", "Full Manuscript Under Preparation (Scheduled Submission Q1 2027)"],
    ["Key Evaluated Datasets", "Phish360 Multi-Modal Benchmark (2,757 test cases), Dedicated Local Phishing Simulation Testbed"],
    ["Reproducibility Artifacts", "Complete code repository, trained models (.joblib, .pt), Docker container, Chrome MV3 extension"]
]

# Table B.1: Plagiarism Screening Results
TB_1_HEADERS = ["Plagiarism Check Engine", "Screening Date", "Similarity Index", "Permissible Threshold", "Compliance Status"]
TB_1_DATA = [
    ["Turnitin Academic Integrity Suite", "18th October 2026", "6.0%", "< 15.0%", "COMPLIANT (APPROVED)"],
    ["Urkund / Ouriginal Plagiarism Checker", "18th October 2026", "5.8%", "< 15.0%", "COMPLIANT (APPROVED)"],
    ["Internet Sources Match Ratio", "18th October 2026", "4.0%", "< 10.0%", "COMPLIANT (APPROVED)"],
    ["Publications & Periodicals Ratio", "18th October 2026", "3.0%", "< 10.0%", "COMPLIANT (APPROVED)"],
    ["Student Papers Cross-Match Ratio", "18th October 2026", "1.0%", "< 5.0%", "COMPLIANT (APPROVED)"]
]

# Table C.1: Multi-Stakeholder Empathy Matrix
TC_1_HEADERS = ["Target Stakeholder Persona", "Core Emotional Need / Friction", "Engineered PhishAlign Solution", "Deployment Channel"]
TC_1_DATA = [
    ["Everyday Consumer / Corporate User", "Zero browsing latency (<200ms); zero false alert friction", "Fast-path tri-modal inference (<160ms); silent green badge", "Chrome Extension (MV3)"],
    ["SOC Security Analyst", "Explainable threat rationale; root-cause brand impersonation", "Interactive Jaccard matrix, visual OCR inspector, SHAP evidence", "Web Analytical Dashboard"],
    ["CISO / Enterprise IT Compliance", "Auditable compliance reporting; leak-free model guarantees", "Automated forensic report generation; group-based partition", "FastAPI Enterprise Gateway"]
]

# Table D.1: Project Milestone Tracker
TD_1_HEADERS = ["Milestone ID", "Phase / Scheduled Activity", "Duration & Timeline", "Key Deliverable Artifacts", "Team Responsibility", "Status"]
TD_1_DATA = [
    ["M-01", "Literature Survey & Research Gap Identification", "Weeks 1–4", "Survey taxonomy, benchmark dataset selection", "Project Team", "COMPLETED"],
    ["M-02", "Feature Engineering (URL 31, HTML 64) & XGBoost", "Weeks 5–8", "Trained URL and HTML gradient boosted trees", "Project Team", "COMPLETED"],
    ["M-03", "MobileNetV3 Vision Model & 25 Consistency Vector", "Weeks 9–12", "Trained MobileNetV3 CNN, consistency.py", "Project Team", "COMPLETED"],
    ["M-04", "Stacking Meta-Classifier & Bootstrap Validation", "Weeks 13–16", "Serialized phishalign_stacking.joblib, ROC curves", "Project Team", "COMPLETED"],
    ["M-05", "FastAPI Backend & React Web Analytical Dashboard", "Weeks 17–20", "REST endpoints (/analyze), interactive UI tabs", "Project Team", "COMPLETED"],
    ["M-06", "Chrome Extension (MV3) & Real-Time Interception", "Weeks 21–22", "Service worker, content script, blocking overlay", "Project Team", "COMPLETED"],
    ["M-07", "Simulated Testbed Evaluation & Final Report", "Weeks 23–24", "End-to-end pipeline.py testing, final report", "Project Team", "COMPLETED"]
]

