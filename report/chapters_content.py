"""
chapters_content.py - Exhaustive Academic Text for PhishAlign Project Report Chapters
Provides in-depth prose, formulas, and structural content for Chapters 1 through 10, Bibliography, and Annexures.
"""

# ============================================================
# CHAPTER 1: INTRODUCTION
# ============================================================

CH1_TITLE = "INTRODUCTION"

CH1_P1 = (
    "The World Wide Web has evolved into the indispensable backbone of global commerce, digital communication, "
    "and critical financial infrastructure. However, this ubiquity has simultaneously amplified the attack surface "
    "for cybercriminals, with phishing remaining the preeminent attack vector for credential theft, corporate espionage, "
    "and financial fraud. Modern phishing campaigns have shifted far beyond crude, mass-emailed deceptive links with obvious "
    "typographical errors. Attackers now deploy sophisticated, automated phishing toolkits, adversary-in-the-middle (AiTM) "
    "reverse proxies (such as Evilginx), dynamic single-page applications, and high-fidelity visual clones of trusted enterprise "
    "and banking portals. These malicious landing pages mimic legitimate login interfaces with pixel-perfect accuracy, while "
    "actively evading traditional perimeter security filters."
)

CH1_P2 = (
    "Traditional automated phishing website detection techniques predominantly rely on single-modality inspection. "
    "These approaches analyze isolated characteristics of a target website: lexical and structural URL heuristics, "
    "HTML Document Object Model (DOM) syntactic features, or rendered webpage screenshots using computer vision algorithms. "
    "While single-modality models provide valuable defensive signals, each suffers from fundamental blind spots. Lexical URL "
    "classifiers are easily circumvented by hosting phishing kits on legitimate cloud platforms, content delivery networks (CDNs), "
    "or compromised trusted servers. HTML-based classifiers fail against dynamic JavaScript rendering, client-side obfuscation, "
    "and canvas-drawn forms. Visual similarity classifiers require immense computational resources to match rendered screenshots "
    "against massive reference banks of protected corporate logos, frequently yielding false positives on legitimate websites "
    "that share common UI design frameworks."
)

CH1_P3 = (
    "More recently, multimodal architectures have been proposed that combine features from multiple channels. However, "
    "conventional multimodal approaches typically employ late feature concatenation or simple probability averaging, "
    "treating each channel as an independent source of evidence. This conventional paradigm fails to examine whether the "
    "information presented across different channels is mutually consistent. In an adversarial phishing attack, an attacker "
    "frequently creates a webpage whose visual appearance and HTML content strongly mimic a well-known brand (such as PayPal, "
    "Microsoft, or Google), yet the hosting domain name belongs to an unrelated, newly registered, or typosquatted address. "
    "Conventional fusion models that blindly average modality probabilities risk being misled when one or more modalities "
    "exhibit ambiguous or weakly suspicious scores."
)

CH1_P4 = (
    "To address this critical architectural limitation, this project presents PhishAlign, a novel multimodal phishing website "
    "detection system powered by explicit cross-modal consistency analysis. PhishAlign simultaneously inspects the website URL, "
    "the HTML DOM structure, and the visual appearance rendered in a screenshot. Crucially, rather than relying solely on isolated "
    "modality predictions, PhishAlign introduces twenty-five (25) explicit cross-modal consistency features that quantify the "
    "semantic, structural, and identity relationships between the URL hostname, HTML text tokens, document title, and optical "
    "character recognition (OCR) tokens extracted from the rendered screenshot. Figure 1.1 illustrates the conceptual distinction "
    "between conventional multimodal architectures and the proposed consistency-aware paradigm."
)

CH1_P5 = (
    "Furthermore, practical deployment of cybersecurity AI requires addressing the conflicting needs of diverse user cohorts. "
    "Security Operations Center (SOC) analysts and threat researchers require exhaustive forensic transparency, detailed "
    "modality decompositions, and explainable feature attributions to audit decisions and investigate emerging campaigns. "
    "Conversely, everyday web consumers and corporate employees require a zero-overhead, frictionless browser companion that "
    "operates invisibly in the background, evaluates active webpages in sub-second time, and intervenes decisively only when "
    "imminent danger is detected. To resolve this duality, PhishAlign is engineered with a dual-client ecosystem: a rich React/Vite "
    "Web Analytical Dashboard for deep forensic auditing, and a lightweight Chromium Browser Extension (Manifest V3) for "
    "real-time zero-click protection. Figure 1.2 illustrates this dual-client operational architecture."
)

CH1_SEC2_TITLE = "Problem Statement"
CH1_SEC2_P1 = (
    "Existing automated phishing website detection solutions exhibit four recurring technical deficiencies that undermine "
    "their efficacy in real-world operational environments:\n"
    "1. Modality Isolation and Semantic Blindness: Single-modality models evaluate URLs, HTML code, or visual screenshots in isolation, "
    "ignoring the semantic contradictions that naturally arise when an attacker impersonates a brand on an unrelated domain.\n"
    "2. High Latency and Computational Overhead: Heavy visual models and server-side browser rendering pipelines incur multi-second delays, "
    "rendering them impractical for real-time client-side web navigation.\n"
    "3. Binary Decision Rigidity and False Positives: Single approve-or-block thresholds force ambiguous, edge-case websites into high-risk "
    "interventions, disrupting legitimate user workflows on novel or non-standard web interfaces.\n"
    "4. Lack of Explainable Forensic Evidence: Opaque black-box neural networks provide raw numerical probabilities without auditable "
    "evidence, leaving SOC analysts incapable of justifying blocked destinations to compliance regulators or corporate users."
)
CH1_SEC2_P2 = (
    "Therefore, the formal problem statement of this project is: To design, implement, and evaluate an automated, real-time "
    "multimodal phishing website detection system that extracts explicit cross-modal consistency features across URL, HTML, "
    "and visual screenshot channels, integrates these relational dimensions into a regularized stacking meta-classifier, and "
    "delivers calibrated risk decisions through a dual-interface architecture comprising a deep forensic analytical web dashboard "
    "and a low-latency real-time browser extension. \n\n"
    "The primary research question investigated in this work is: "
    "\"Can explicit cross-modal consistency between URL, HTML content, and webpage appearance improve phishing website detection compared with conventional multimodal fusion?\""
)

CH1_SEC3_TITLE = "Existing Work"
CH1_SEC3_P1 = (
    "A variety of techniques have been deployed in commercial products and academic literature to detect phishing websites. "
    "These methods can be broadly categorized into blacklist-based systems, lexical URL classifiers, DOM heuristic engines, "
    "visual screenshot matchers, and conventional multimodal neural networks. Each family provides distinct operational advantages, "
    "yet each leaves critical vulnerabilities unaddressed. Table 1.1 summarizes these existing approaches, highlights their "
    "intrinsic drawbacks, and outlines how PhishAlign resolves them."
)

CH1_SEC4_TITLE = "Motivation"
CH1_SEC4_P1 = (
    "The motivation behind PhishAlign stems from three profound cybersecurity realities. First, credential phishing continues "
    "to account for over 36% of all global data breaches, with average enterprise financial losses exceeding $4.45 million per "
    "incident according to recent IBM Security reports. Second, the democratization of generative AI and automated phishing "
    "frameworks allows attackers to generate pristine, grammatically flawless, and visually impeccable deceptive pages in seconds, "
    "rendering traditional email and content filters obsolete. Third, existing machine learning defenses operate as black-box "
    "silos that fail to capture the most fundamental signature of deception: inconsistency between what a website claims to be "
    "(its visual and textual brand identity) and where it is actually hosted (its registered domain authority).\n\n"
    "As final-year engineering students specializing in computer systems, machine learning, and applied cybersecurity, we were "
    "compelled to build a platform that bridges the gap between academic multimodal research and practical, human-centered security "
    "tooling. By synthesizing computer vision, natural language processing, tabular gradient boosting, and browser systems engineering, "
    "PhishAlign seeks to provide a resilient, transparent, and universally accessible defense for the modern web."
)

CH1_SEC5_TITLE = "Objectives"
CH1_SEC5_P1 = (
    "To achieve the stated research goals, the project is structured around the following concrete engineering and research objectives:\n"
    "1. Multimodal Phishing Detection System: To develop a unified multimodal detection system that simultaneously ingests URL strings, raw HTML DOM, and rendered webpage screenshots.\n"
    "2. Specialized Modality Models: To build individual, high-performance machine learning models for each modality—XGBoost for lexical URL features (Model 1), XGBoost for HTML DOM tree metrics (Model 2), and MobileNetV3-Small deep CNN for visual screenshot analysis (Model 3).\n"
    "3. Explicit Cross-Modal Consistency Engine: To extract twenty-five (25) explicit consistency features measuring semantic token overlap, Jaccard similarity, containment ratios, and domain-identity alignment between URL hostnames, HTML text, page titles, and optical character recognition (OCR) visible text.\n"
    "4. Regularized Stacking Meta-Learner: To combine the three base modality probabilities with the 25 consistency features into a unified 28-dimensional input vector and train a regularized Logistic Regression meta-learner (Model 4) to produce calibrated threat probabilities.\n"
    "5. Dynamic Identity and Alignment Gating: To engineer an NLP Dynamic Identity & Alignment Gate that inspects verified brand identities against registered hostnames and enforces a calibrated three-tier decision policy (Safe, Caution, Phishing).\n"
    "6. Baseline Comparison and Empirical Evaluation: To benchmark PhishAlign against single-modality baselines, equal-weight probability fusion, and probability-only stacking on the official Phish360 benchmark (2,757 complete cases) using leak-free group-based partitioning and bootstrap confidence intervals.\n"
    "7. Dual-Client Practical Deployment: To construct both a full-featured React/Vite Web Analytical Dashboard for SOC threat analysts and a lightweight Chromium Browser Extension (Manifest V3) for real-time zero-click consumer protection with full-screen threat interception."
)

CH1_SEC6_TITLE = "Scope"
CH1_SEC6_P1 = (
    "The scope of this project encompasses the end-to-end design, implementation, evaluation, and deployment of the PhishAlign system. "
    "Specifically, the project addresses HTML-based and visual web phishing attacks targeting desktop web browsers running Chromium-compatible "
    "engines. The evaluation is conducted on the curated Phish360 academic benchmark, covering both legitimate and malicious websites across "
    "financial, social, corporate, and technological domains. The scope includes server-side headless capture, client-side browser extension "
    "capture, optical character recognition via Tesseract, tabular feature extraction, deep CNN visual inference, regularized meta-learning, "
    "and interactive web visualization.\n\n"
    "The project explicitly excludes non-HTTP protocols, native mobile applications (iOS/Android binaries), SMS-based phishing (smishing) "
    "without a web component, and voice phishing (vishing). While the current implementation focuses primarily on Latin-character domain "
    "names and English webpage text, the underlying mathematical framework of cross-modal consistency is designed to be language-agnostic."
)

CH1_SEC7_TITLE = "Organisation of the Report"
CH1_SEC7_P1 = (
    "The remainder of this report is organized as follows:\n"
    "• Chapter 2 (Concepts and Methods) establishes the theoretical foundations of phishing detection, class imbalance, gradient boosted trees, "
    "deep vision architectures, cross-modal consistency formulation, and the dual-interface architecture.\n"
    "• Chapter 3 (Literature Survey) provides an extensive critical survey of existing academic literature and commercial techniques across "
    "URL heuristics, DOM analysis, visual logo matching, and multimodal fusion, identifying the unresolved research gap.\n"
    "• Chapter 4 (Project Plan) outlines the iterative engineering methodology, project phases, work breakdown schedule (Gantt chart), resource "
    "specifications, and risk mitigation strategies.\n"
    "• Chapter 5 (Software Requirement Specification) specifies the functional, non-functional, external interface, hardware, software, and use "
    "case requirements of the system.\n"
    "• Chapter 6 (System Design) details the end-to-end architectural topology, data flow diagrams (Level 0 and Level 1), process flows, UML "
    "sequence diagrams, class designs, feature engineering schemas, and security considerations.\n"
    "• Chapter 7 (Implementation) discusses the development environment, dataset preprocessing, leak-free group partitioning, model training, "
    "OCR integration, FastAPI backend services, React web dashboard, and the Chrome extension.\n"
    "• Chapter 8 (Results and Discussion) presents the experimental benchmark evaluation, ablation studies, statistical bootstrap analysis, "
    "latency profiling, live testbed scenario results, and snapshot evaluations.\n"
    "• Chapter 9 (Software Testing) covers the comprehensive quality assurance methodology, unit testing, model stress testing, API integration "
    "tests, and system verification.\n"
    "• Chapter 10 (Conclusion and Future Work) concludes the report with a summary of contributions, operational limitations, and a future roadmap.\n"
    "• Bibliography and Annexures provide complete academic citations, publication drafts, plagiarism verification, empathy charts, and project trackers."
)

# ============================================================
# CHAPTER 2: CONCEPTS AND METHODS
# ============================================================

CH2_TITLE = "CONCEPTS AND METHODS"

CH2_P1 = (
    "This chapter establishes the core mathematical formulations, algorithmic paradigms, and systems concepts underpinning PhishAlign. "
    "It covers formal definitions, the challenges of class imbalance, gradient boosted decision trees (XGBoost), deep convolutional "
    "vision networks (MobileNetV3-Small), the mathematical theory of cross-modal consistency, the dual-client interface design, "
    "and the complete technology stack."
)

CH2_SEC1_TITLE = "Definitions"
CH2_SEC1_P1 = (
    "To establish rigorous terminology, the primary concepts utilized throughout this research are formally defined:\n"
    "• Phishing Website: A malicious web resource created by an unauthorized entity that deceptively imitates the visual appearance, "
    "branding, or functionality of a legitimate organization to solicit sensitive credentials, personal data, or unauthorized payments.\n"
    "• Modality: An independent channel of informational representation describing a webpage. In PhishAlign, three primary modalities "
    "are ingested: the URL string (M_url), the HTML Document Object Model (M_html), and the rendered screenshot image (M_visual).\n"
    "• Cross-Modal Consistency: The mathematical degree of mutual agreement, vocabulary overlap, and identity alignment between information "
    "extracted across two or more distinct modalities of the same web entity.\n"
    "• Jaccard Similarity: A set-theoretic metric quantifying the overlap between two token sets A and B, defined as J(A, B) = |A ∩ B| / |A ∪ B|.\n"
    "• Containment Ratio: The directional fraction of a specific query token set A that is completely subsumed within a target reference set B, "
    "defined as C(A, B) = |A ∩ B| / |A|.\n"
    "• Overlap Coefficient (Szymkiewicz–Simpson): A size-normalized overlap metric between two token sets of disparate cardinalities, defined as "
    "O(A, B) = |A ∩ B| / min(|A|, |B|). In PhishAlign, this formulation is specifically utilized for html_ocr_containment to evaluate mutual text "
    "containment without allowing the extensive size of the HTML DOM to unfairly dilute the visual OCR token match.\n"
    "• Identity Anchor: An authoritative, verifiable token or set of tokens representing the registered domain identity (e.g., 'paypal' from "
    "'paypal.com') against which claimed visual and textual brand identities are verified."
)

CH2_SEC2_TITLE = "Class Imbalance and Evaluation Metrics"
CH2_SEC2_P1 = (
    "In live operational web traffic, phishing is an extreme minority phenomenon. Standard internet telemetry indicates that benign "
    "web browsing accounts for over 99.9% of all HTTP transactions. In such an imbalanced regime, traditional accuracy is an intrinsically "
    "misleading metric; a naive classifier that predicts every single webpage as 'legitimate' would achieve 99.9% accuracy while offering zero "
    "protection against active cyberattacks. Therefore, model evaluation must prioritize metrics that isolate positive class performance:\n\n"
    "• Precision = TP / (TP + FP): Measures the exactness of the classifier; high precision ensures that legitimate websites are not falsely "
    "blocked, preventing disruption to user workflows.\n"
    "• Recall (Sensitivity) = TP / (TP + FN): Measures completeness; high recall ensures that malicious phishing pages are not allowed to pass "
    "undetected into the user's browser.\n"
    "• F1-Score = 2 × (Precision × Recall) / (Precision + Recall): The harmonic mean of precision and recall, providing a balanced single metric.\n"
    "• Receiver Operating Characteristic Area Under the Curve (ROC-AUC): Evaluates the classifier's ability to rank positive instances above "
    "negative instances across all possible decision thresholds, invariant to class distribution skew."
)

CH2_SEC3_TITLE = "Gradient Boosted Trees and XGBoost"
CH2_SEC3_P1 = (
    "For tabular feature representations extracted from URLs and HTML source code, decision tree ensembles remain the gold standard in "
    "cybersecurity applications. Gradient boosted decision trees iteratively construct an additive ensemble of K regression trees that "
    "minimize a regularized objective function. At each iteration t, a new decision tree f_t(x) is fit to the pseudo-residuals (negative "
    "gradients) of the loss function evaluated at the previous ensemble prediction:\n\n"
    "L^(t) ≈ ∑ [ l(y_i, y_hat_i^(t-1)) + g_i f_t(x_i) + 0.5 h_i f_t^2(x_i) ] + Ω(f_t)\n\n"
    "where g_i and h_i represent the first and second-order Taylor expansion gradients of the loss function, and Ω(f_t) = γ T + 0.5 λ ∑ w_j^2 "
    "penalizes tree complexity (number of leaves T and leaf weights w_j). XGBoost is selected because it evaluates tabular feature vectors "
    "in microseconds, resists overfitting on noisy features, handles missing attribute values natively, and yields deterministic decision boundaries."
)

CH2_SEC4_TITLE = "Deep Convolutional Vision and MobileNetV3-Small"
CH2_SEC4_P1 = (
    "Visual screenshot analysis requires deep convolutional representations to detect visual brand impersonation, high-contrast credential "
    "input fields, and suspicious layout configurations. However, traditional deep CNNs (such as ResNet-50 or VGG-16) contain tens of millions "
    "of parameters and require hundreds of milliseconds of GPU compute per image, violating real-time browser latency constraints. "
    "PhishAlign incorporates MobileNetV3-Small, a lightweight convolutional neural network optimized through hardware-aware Neural Architecture "
    "Search (NAS). MobileNetV3-Small employs depthwise separable convolutions, inverted residual blocks, lightweight Squeeze-and-Excitation (SE) "
    "channel attention, and computationally efficient hard-swish activation functions:\n\n"
    "h-swish(x) = x × [ ReLU6(x + 3) / 6 ]\n\n"
    "Operating with under 2.5 million parameters and requiring only ~0.06 GFLOPs per 224×224 image, MobileNetV3-Small executes in under 45ms "
    "on consumer CPUs while delivering high visual classification accuracy."
)

CH2_SEC5_TITLE = "Cross-Modal Consistency Theory"
CH2_SEC5_P1 = (
    "The central theoretical thesis of PhishAlign is that explicit cross-modal consistency features capture deception signatures that "
    "are undetectable by isolated modality models. In legitimate web entities, there exists high semantic cohesion: a page hosted on "
    "'wikipedia.org' declares a document title containing 'Wikipedia', renders visual headings containing 'Wikipedia', and embeds HTML text "
    "describing 'Wikipedia'. Conversely, a phishing attack creates an acute cross-modal contradiction: the webpage visual screenshot and HTML "
    "DOM strongly resemble an authentic brand login interface (e.g., PayPal), yet the underlying URL domain identity belongs to an unrelated "
    "string (e.g., 'paypal-verification-portal.xyz' or 'telegr.am').\n\n"
    "To formally capture these phenomena, PhishAlign extracts deterministic token sets across four textual projections: the URL host tokens (T_host), "
    "the HTML body text tokens (T_html), the document title tokens (T_title), and the optical text tokens extracted from the screenshot via "
    "Tesseract OCR (T_ocr). The system computes 25 continuous and discrete features encompassing:\n"
    "1. Binary Availability Flags: Indicating whether HTML DOM, screenshot OCR, page title, and valid hostnames were successfully captured.\n"
    "2. Pairwise Jaccard and Containment Metrics: Measuring symmetric and asymmetric token overlap across all pairs of textual projections.\n"
    "3. Domain Identity Overlap Metrics (v3): Extracting authoritative second-level domain brand tokens (stripped of generic TLDs and "
    "subdomain prefixes) and measuring their exact containment within the HTML body, title, and visual OCR text.\n\n"
    "Figure 2.1 illustrates the tri-modality feature space and the composition of the 25-dimensional consistency vector."
)

CH2_SEC6_TITLE = "Stacking Meta-Learning Architecture"
CH2_SEC6_P1 = (
    "To combine the base modality probabilities with the 25 consistency features, PhishAlign implements a stacking meta-classifier. "
    "Stacking is an ensemble learning technique in which the predictions of multiple first-level base classifiers serve as inputs to a second-level "
    "meta-learner. In PhishAlign, the base level comprises the URL XGBoost model (outputting P_url), the HTML XGBoost model (outputting P_html), "
    "and the MobileNetV3-Small visual CNN (outputting P_visual). These three probabilities are concatenated with the 25 consistency dimensions "
    "to form a fixed 28-dimensional input vector x ∈ R^28.\n\n"
    "The meta-classifier is a regularized Logistic Regression model parameterized by weight vector w ∈ R^28 and intercept b:\n\n"
    "z = w^T x + b = w_url P_url + w_html P_html + w_vis P_visual + ∑ [ w_j C_j ] + b\n\n"
    "P_phish = σ(z) = 1 / (1 + e^(-z))\n\n"
    "This linear-in-the-logit meta-learner ensures optimal regularized weighting, prevents over-reliance on any single modality, and supports "
    "exact game-theoretic feature attribution. Figure 2.2 depicts the complete stacking classifier architecture."
)

CH2_SEC7_TITLE = "Dual-Interface Architecture: Web Analytics vs. Extension Guard"
CH2_SEC7_P1 = (
    "A crucial contribution of PhishAlign is the dual-interface architecture designed to serve two fundamentally distinct operational user classes "
    "using the exact same underlying machine learning model:\n"
    "• Web Analytical Dashboard (React / Vite): Engineered for SOC analysts, cybersecurity investigators, and compliance auditors. It provides an "
    "exhaustive, deep-dive forensic environment. Analysts can enter arbitrary external URLs, inspect headless Playwright browser captures, view "
    "full-resolution screenshots, explore the pairwise Jaccard text-overlap matrix, inspect domain identity containment scores, review SHAP feature "
    "attributions, and toggle 'Research Mode' to compare PhishAlign against baseline models.\n"
    "• Browser Extension Companion (Chrome Manifest V3): Engineered for everyday internet consumers and corporate employees. It operates silently "
    "in the browser background with zero user friction. It extracts the active tab's DOM and captures visible viewport screenshots client-side via "
    "Chrome extension APIs, submitting pre-captured data to the backend via a fast path that bypasses server-side rendering. For safe websites, "
    "it renders a non-intrusive green security badge ('Authentic Website'). If a high-risk phishing destination is detected (P_phish ≥ 0.78), the "
    "extension instantly injects a full-screen blocking overlay, preventing keyboard input and credential submission, while offering a clear "
    "'Go Back to Safety' escape action."
)

CH2_SEC8_TITLE = "Technology Stack"
CH2_SEC8_P1 = (
    "The engineering realization of PhishAlign synthesizes high-performance frameworks across Python backend services, machine learning libraries, "
    "browser automation tooling, and modern TypeScript frontend interfaces. Table 2.1 presents the complete technology stack utilized in the project."
)

# ============================================================
# CHAPTER 3: LITERATURE SURVEY
# ============================================================

CH3_TITLE = "LITERATURE SURVEY"

CH3_P1 = (
    "Phishing detection has been intensely investigated across academic and industrial cybersecurity research over the past two decades. "
    "This chapter surveys the historical evolution of automated phishing defense mechanisms, categorized by their underlying modality "
    "and analytical methodology. It reviews lexical URL classifiers, DOM-based heuristic engines, visual screenshot matchers, multimodal "
    "fusion frameworks, and real-time browser extension defenses, culminating in a critical analysis of unresolved research gaps."
)

CH3_SEC1_TITLE = "Lexical and URL-Based Phishing Detection"
CH3_SEC1_P1 = (
    "Early machine learning approaches focused exclusively on lexical properties of the URL string. Ma et al. (2009) pioneered the use "
    "of online learning algorithms (Perceptron, Passive-Aggressive, and Logistic Regression) trained on lexical features such as host length, "
    "path depth, number of subdomains, and bag-of-words token presence. Blum et al. (2010) proposed Confidence-Weighted classification on "
    "character n-grams, demonstrating that malicious URLs exhibit higher entropy and non-standard lexical structures. Marchal et al. (2017) "
    "introduced 'Off-the-hook', which combined lexical URL features with search engine query identity verification, achieving 99.1% precision.\n\n"
    "However, modern phishing attackers routinely circumvent URL-only defenses by purchasing legitimate-looking domains, utilizing cloud service "
    "subdomains (e.g., workers.dev, azurewebsites.net, github.io), or employing homoglyph attacks using Internationalized Domain Names (IDNs). "
    "Without inspecting the underlying page content and visual presentation, URL-only models inevitably suffer from blind spots."
)

CH3_SEC2_TITLE = "Content and DOM-Based Heuristic Classifiers"
CH3_SEC2_P1 = (
    "To overcome the limitations of URL inspection, researchers turned to webpage source code analysis. Zhang et al. (2007) developed "
    "CANTINA, which applied the Term Frequency-Inverse Document Frequency (TF-IDF) information retrieval algorithm to identify the five "
    "most significant terms in a page's text and queried Google to verify if the domain appeared in top search results. Xiang et al. (2011) "
    "extended this into CANTINA+, introducing 15 comprehensive features covering HTML form actions, password fields, script count, and external "
    "anchor ratios. Li et al. (2019) introduced DeepPhish, applying deep Recurrent Neural Networks (RNNs) and Convolutional Neural Networks "
    "to raw HTML character streams.\n\n"
    "While DOM-based heuristics detect obvious credential-harvesting forms, they are highly fragile against dynamic Single Page Applications (SPAs) "
    "and adversarial evasion. Modern phishing kits employ heavy JavaScript obfuscation (e.g., JSFuck, polymorphic string encoding), load forms "
    "dynamically after user interaction, or draw input fields directly onto an HTML5 `<canvas>`, presenting an empty DOM tree to static scrapers."
)

CH3_SEC3_TITLE = "Visual Similarity and Screenshot-Based Analysis"
CH3_SEC3_P1 = (
    "Recognizing that human victims are deceived by visual appearance rather than source code, researchers proposed visual matching defenses. "
    "Medvet et al. (2008) utilized visual layout comparison and text chunk bounding boxes. Afroz & Greenstadt (2011) introduced PhishZoo, which "
    "stored a reference bank of protected corporate logos and matched candidate screenshots using perceptual hashing and SIFT keypoint matching. "
    "Abdelnabi et al. (2020) proposed VisualPhishNet, a deep metric learning framework that encoded screenshot visual appearance into dense "
    "triplet-loss embeddings. Lin et al. (2021) developed Phishpedia, combining Faster R-CNN for logo object detection with a siamese matching "
    "network to identify target brand marks with 98.2% precision.\n\n"
    "Despite their breakthroughs, visual-only systems carry severe operational drawbacks: they require massive reference databases of corporate "
    "logos, suffer high false positive rates when legitimate sites share standardized bootstrap UI templates, fail to detect phishing attacks "
    "targeting lesser-known brands, and incur multi-second inference latencies that disrupt browsing workflows."
)

CH3_SEC4_TITLE = "Multimodal Fusion in Cybersecurity"
CH3_SEC4_P1 = (
    "To synthesize the complementary strengths of different modalities, multimodal fusion architectures have recently gained prominence. "
    "Bozkir et al. (2023) introduced a multimodal deep learning network that concatenated feature embeddings from URLs, page text, and "
    "screenshot CNN representations. Similarly, blended approaches have combined URL character embeddings with HTML DOM graph neural networks.\n\n"
    "However, virtually all existing multimodal phishing detection frameworks rely on late concatenation or simple score averaging. They treat "
    "modalities as parallel, independent streams. They fail to explicitly evaluate the relational alignment between channels—specifically, "
    "whether the brand identity claimed in the visual appearance corresponds to the registered authority of the URL domain. Table 3.1 provides "
    "a comparative summary of the surveyed literature."
)

CH3_SEC5_TITLE = "Browser Extension Real-Time Defense Systems"
CH3_SEC5_P1 = (
    "Client-side browser extensions represent the frontline of consumer cybersecurity. Early extensions (such as SpoofGuard and Netcraft) "
    "relied on static rules and remote blacklist lookups. However, recent architectural changes—specifically Google's transition to Manifest V3—"
    "impose strict security constraints: background pages are replaced by ephemeral Service Workers, remote script execution is strictly forbidden, "
    "and extension execution overhead must remain minimal to avoid impacting web navigation fluidity. Consequently, modern extensions require "
    "lightweight client capture architectures that stream sanitized DOM snapshots to high-throughput backend inference engines."
)

CH3_SEC6_TITLE = "Summary of the Surveyed Literature"
CH3_SEC6_P1 = (
    "Table 3.1 synthesizes the evolutionary progression of phishing detection methodologies surveyed in this chapter."
)

CH3_SEC7_TITLE = "Research Gap and PhishAlign Positioning"
CH3_SEC7_P1 = (
    "The critical research gap identified in the literature can be summarized as follows: Existing multimodal systems combine features "
    "without verifying cross-modal consistency. They assume that if each modality is independently analyzed, a simple ensemble will suffice. "
    "However, phishing is inherently an act of cross-modal contradiction: a website presents an authentic visual brand facade while operating "
    "on an unrelated domain infrastructure.\n\n"
    "PhishAlign directly resolves this gap by pioneering explicit cross-modal consistency engineering. By computing 25 deterministic Jaccard, "
    "containment, and domain identity overlap features between URL, HTML, title, and screenshot OCR projections, PhishAlign equips the fusion "
    "model with explicit relational intelligence. Furthermore, PhishAlign bridges the gap between research models and human users by delivering "
    "a dual-client interface: a deep forensic dashboard for security researchers and an ultra-fast browser extension for real-time consumer protection."
)

# ============================================================
# CHAPTER 4: PROJECT PLAN
# ============================================================

CH4_TITLE = "PROJECT PLAN"

CH4_P1 = (
    "Developing a complex, multi-tiered cybersecurity platform combining deep learning, browser automation, and real-time extensions "
    "requires rigorous software engineering planning. This chapter details the development lifecycle, structured project phases, "
    "work breakdown timeline, resource specifications, and risk mitigation strategies implemented throughout the project."
)

CH4_SEC1_TITLE = "Development Methodology"
CH4_SEC1_P1 = (
    "PhishAlign was developed using an Iterative and Incremental Development (IID) model, combining Agile sprint cadences with rigorous "
    "empirical machine learning milestones. An iterative model was selected over a traditional linear waterfall approach because research "
    "in multimodal machine learning entails continuous experimental feedback loops: feature extraction refinements, dataset leak-audit "
    "discoveries, and latency bottlenecks in browser capture necessitate regular refactoring and hyperparameter re-tuning.\n\n"
    "The development lifecycle was structured into two-week sprints. Each sprint produced working, testable software increments, transitioning "
    "from initial dataset curation to base model training, consistency feature formulation, backend API engineering, web dashboard delivery, "
    "and browser extension integration. Figure 4.1 illustrates the iterative development lifecycle and feedback loops."
)

CH4_SEC2_TITLE = "Project Phases and Deliverables"
CH4_SEC2_P1 = (
    "The engineering execution was divided into seven discrete, chronological phases. Table 4.1 enumerates the phases, planned engineering "
    "activities, and concrete deliverables produced."
)

CH4_SEC3_TITLE = "Project Schedule and Milestones"
CH4_SEC3_P1 = (
    "The project was executed over a 24-week academic development lifecycle. Figure 4.2 presents the project schedule Gantt chart, tracking "
    "the parallel execution of machine learning research, backend API development, and frontend client engineering."
)

CH4_SEC4_TITLE = "Resource Requirements"
CH4_SEC4_P1 = (
    "Execution of the project required specialized hardware and software resources:\n"
    "• Computational Hardware: High-performance workstation equipped with an Intel Core i7-12700H CPU, 32 GB DDR5 RAM, and an NVIDIA GeForce "
    "RTX 3060 Laptop GPU (6 GB VRAM) for accelerating MobileNetV3 visual training and Playwright batch rendering.\n"
    "• Dataset Infrastructure: Local storage allocation of 45 GB dedicated to the Phish360 multimodal benchmark dataset, housing raw HTML files, "
    "full-resolution PNG screenshots, metadata CSVs, and pre-extracted feature tensors.\n"
    "• Software & Tooling: Python 3.11 runtime, PyTorch 2.1 with CUDA 12.1 support, Scikit-Learn, XGBoost, Playwright Chromium, Tesseract OCR 5.3, "
    "Node.js 20.x, React 18, Vite 5.0, Google Chrome v120+, and Git version control."
)

CH4_SEC5_TITLE = "Risk Analysis and Mitigation Strategies"
CH4_SEC5_P1 = (
    "Complex machine learning projects face severe risks regarding data integrity, inference latency, adversarial evasion, and software "
    "compatibility. Table 4.2 provides the comprehensive risk analysis matrix and the engineered mitigation strategies adopted in PhishAlign."
)

# ============================================================
# CHAPTER 5: SOFTWARE REQUIREMENT SPECIFICATION
# ============================================================

CH5_TITLE = "SOFTWARE REQUIREMENT SPECIFICATION"

CH5_P1 = (
    "This chapter establishes the formal Software Requirement Specification (SRS) for PhishAlign in accordance with IEEE 830 standards. "
    "It delineates the system scope, user classes, functional requirements, detailed use cases, external interface definitions, non-functional "
    "performance thresholds, and minimum hardware/software specifications."
)

CH5_SEC1_TITLE = "Project Scope"
CH5_SEC1_P1 = (
    "PhishAlign is an automated multimodal phishing detection and explainable security audit platform. The software encompasses two primary "
    "client applications (a Web Analytical Dashboard and a Chromium Browser Extension) backed by a centralized asynchronous FastAPI service. "
    "The system ingests website URLs, renders page content using headless Chromium or client-side tab capture, extracts structural and visual "
    "features, computes 25 cross-modal consistency dimensions, executes a regularized stacking meta-classifier, and renders risk verdicts "
    "with supporting forensic evidence."
)

CH5_SEC2_TITLE = "Overall Description"
CH5_SEC2_P1 = (
    "The system operates across three logical tiers:\n"
    "1. Client Tier: Dual presentation layer comprising the React web application for deep auditing and the Chrome extension for real-time browsing.\n"
    "2. Application Service Tier: FastAPI REST server managing request validation, Playwright browser orchestration, OCR extraction, and response formatting.\n"
    "3. Machine Learning Inference Tier: High-speed tabular inference engines (XGBoost), deep visual CNNs (PyTorch MobileNetV3-Small), deterministic "
    "consistency extractors, and stacking meta-classifiers."
)

CH5_SEC3_TITLE = "User Classes and Characteristics"
CH5_SEC3_P1 = (
    "PhishAlign supports four distinct user classes with varying technical requirements. Table 5.1 outlines these user classes, their operational "
    "personas, and primary platform interfaces."
)

CH5_SEC4_TITLE = "Functional Requirements"
CH5_SEC4_P1 = (
    "Table 5.2 defines the formal functional requirements of PhishAlign across ingestion, feature engineering, modeling, and client delivery."
)

CH5_SEC5_TITLE = "Use Cases"
CH5_SEC5_P1 = (
    "Figure 5.1 presents the Unified Modeling Language (UML) Use Case Diagram illustrating user interactions with the PhishAlign system boundary. "
    "Table 5.3 provides the expanded tabular specification for the primary use case: 'Analyze Webpage via Dashboard / Extension'."
)

CH5_SEC6_TITLE = "External Interface Requirements"
CH5_SEC6_P1 = (
    "PhishAlign specifies three major external interfaces:\n"
    "• User Interfaces: Modern, responsive web graphical interfaces. The Web Dashboard uses a dark-themed security analyst aesthetic with tabbed "
    "views (Overview, URL, HTML, Visual, Consistency, Explainability). The Browser Extension utilizes a compact popup modal with clear status badges.\n"
    "• Hardware Interfaces: Standard CPU and GPU memory buses for executing PyTorch tensor operations and Playwright headless Chromium instances.\n"
    "• Software / Network Interfaces: Asynchronous HTTP/1.1 and HTTP/2 REST APIs operating over TCP ports 8000 and 5173, utilizing JSON payloads "
    "and CORS headers supporting browser extension origins (`chrome-extension://*`)."
)

CH5_SEC7_TITLE = "Non-Functional Requirements"
CH5_SEC7_P1 = (
    "Table 5.4 outlines the non-functional requirements governing system latency, classification accuracy, reliability, security, and portability."
)

CH5_SEC8_TITLE = "Hardware and Software Requirements"
CH5_SEC8_P1 = (
    "Table 5.5 enumerates the minimum and recommended hardware and software specifications for running and deploying PhishAlign."
)

print("Report Content Module - Part 1 Loaded Successfully!")
