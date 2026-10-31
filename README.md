# PhishAlign 🛡️
### Cross-Modal Consistency-Based Phishing Website Detection System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19.2-61dafb?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0%2B-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-8.0-646cff?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS v4](https://img.shields.io/badge/Tailwind_CSS-v4.0-38bdf8?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Chrome Manifest V3](https://img.shields.io/badge/Chrome_Extension-Manifest_V3-4285f4?logo=googlechrome&logoColor=white)](https://developer.chrome.com/docs/extensions/mv3/intro/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**PhishAlign** is a next-generation cyber defense platform designed to detect evasive, zero-day phishing websites by modeling **cross-modal consistency** across URL lexical semantics, HTML DOM structural attributes, and rendered visual imagery. 

Unlike conventional phishing detection systems that evaluate modalities in isolation (and are easily fooled by deceptive domain masking, brand logo impersonation, or obfuscated source code), PhishAlign evaluates whether what a website **claims to be** (URL), what it **is built with** (HTML DOM), and what it **looks like** (Visual rendering) are semantically and forensically aligned.

The platform provides a unified **dual-client ecosystem**:
1. 🛡️ **Chrome / Edge Browser Extension (Client Protection)** — Passive, automated, zero-click real-time navigation defense that hard-blocks malicious websites.
2. 🌐 **React Web Dashboard (Security Analyst Portal)** — Rich, forensic investigation suite featuring interactive feature inspections, SHAP explainability charts, rendered screenshot analysis, and research comparison modes.
3. 🧠 **Unified FastAPI AI Engine** — High-performance backend hosting 3 unimodal ML models, Tesseract OCR, a 25-feature cross-modal consistency engine, and a stacking meta-classifier.

---

## 📑 Table of Contents

- [Architectural Overview](#-architectural-overview)
- [Dual-Client Ecosystem](#-dual-client-ecosystem)
  - [1. Chrome / Edge Browser Extension](#1-chrome--edge-browser-extension-client-protection)
  - [2. React Web Analyst Dashboard](#2-react-web-analyst-dashboard-analyst-portal)
- [Machine Learning & Consistency Pipeline](#-machine-learning--consistency-pipeline)
- [Project Directory Structure](#-project-directory-structure)
- [Prerequisites](#-prerequisites)
- [Quick Start Guide (Step-by-Step)](#-quick-start-guide-step-by-step)
  - [Step 1: Start the FastAPI AI Backend](#step-1-start-the-fastapi-ai-backend)
  - [Step 2: Start the React Web Dashboard](#step-2-start-the-react-web-dashboard)
  - [Step 3: Load the Browser Extension](#step-3-load-the-browser-extension)
  - [Step 4: Launch the Phishing Simulation Testbed](#step-4-launch-the-phishing-simulation-testbed)
- [Testing & Demonstration Scenarios](#-testing--demonstration-scenarios)
- [API Reference](#-api-reference)
- [Academic Report & Research Artifacts](#-academic-report--research-artifacts)
- [Troubleshooting & FAQs](#-troubleshooting--faqs)

---

## 🏛️ Architectural Overview

```
                                  ┌──────────────────────────────────────────────┐
                                  │            TARGET WEB TRANSACTION            │
                                  └──────────────────────┬───────────────────────┘
                                                         │
                         ┌───────────────────────────────┴───────────────────────────────┐
                         ▼                                                               ▼
        ┌──────────────────────────────────┐                            ┌──────────────────────────────────┐
        │    CHROME / EDGE EXTENSION       │                            │       REACT WEB DASHBOARD        │
        │  (Automated Passive Protection)  │                            │    (Security Analyst Portal)     │
        │                                  │                            │                                  │
        │ • Navigation Interception        │                            │ • Forensic URL Submission        │
        │ • Active DOM & Viewport Capture  │                            │ • Live Pipeline Animation        │
        │ • Dynamic Toolbar Badges         │                            │ • 25 Consistency Feature Matrix  │
        │ • Full-Screen Hard Blocking      │                            │ • SHAP Attribution Waterfall     │
        │ • Quick Threat Popup             │                            │ • Research Mode Model Comparison │
        └────────────────┬─────────────────┘                            └────────────────┬─────────────────┘
                         │                                                               │
                         │ POST /analyze_content (Layer 1 Direct)                        │ POST /analyze (Layer 2/3)
                         └───────────────────────────────┬───────────────────────────────┘
                                                         ▼
                         ┌───────────────────────────────────────────────────────────────┐
                         │              FASTAPI INFERENCE BACKEND (:8000)                │
                         ├───────────────────────────────────────────────────────────────┤
                         │  1. Ingestion: Direct Browser Capture OR Playwright Stealth   │
                         │  2. Modality 1: URL Lexical Classifier (XGBoost, 31 feats)    │
                         │  3. Modality 2: HTML DOM Classifier (XGBoost, 64 feats)       │
                         │  4. Modality 3: Visual MobileNetV3 + Tesseract OCR (128 dims) │
                         │  5. Fusion: 25 Cross-Modal Consistency Feature Extractor      │
                         │  6. Meta-Classifier: Stacking Ensemble (28-dimensional vector)│
                         │  7. Decision Engine: 3-Tier Risk (Safe / Caution / Danger)    │
                         └───────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Dual-Client Ecosystem

### 1. Chrome / Edge Browser Extension (Client Protection)

The PhishAlign Browser Extension runs transparently inside Chromium-based browsers (Google Chrome, Microsoft Edge, Brave, Opera) to protect everyday users with zero friction:

* **Zero-Click Automated Protection**: Intercepts `webNavigation.onCommitted` lifecycle events and performs an instant pre-render security check.
* **Dual-Layer Capture Architecture**:
  * **Layer 1 (Direct In-Browser Capture)**: Grabs the live hydrated DOM and active viewport screenshot via `chrome.tabs.captureVisibleTab`, avoiding bot-protection walls (Cloudflare, DDoS-Guard).
  * **Layer 2 / 3 (Playwright Fallback)**: Server-side headless capture with randomized fingerprints and bot-challenge guardrails when direct capture is unavailable.
* **Dynamic Toolbar Badges**:
  * 🟢 `✓` **Safe** — Legitimate site (`Risk < 50%`)
  * 🟠 `[X]%` **Caution** — Suspicious anomalies detected (`50% ≤ Risk < 78%`)
  * 🔴 `[X]%` **Danger** — Phishing detected (`Risk ≥ 78%`)
  * ⚠️ `?` **Offline** — Backend disconnected
* **Full-Screen Hard-Block Intercept Screen**:
  * Prevents users from interacting with verified phishing login forms.
  * Displays overall phishing probability along with per-modality risk breakdowns (URL, HTML, Visual).
  * Lists detected consistency violations (e.g., *Brand Name Claimed in Title ≠ Registered Domain Name*).
  * Provides a prominent **"Go Back to Safety"** button and an explicit **"Proceed Anyway (Unsafe Override)"** bypass.
* **Interactive Popup Inspector**:
  * Click the shield icon in your toolbar to see live risk meters, individual model confidence scores, and page intent chips.
  * One-click shortcut to launch the current page into the Web Dashboard for forensic drill-down.

---

### 2. React Web Analyst Dashboard (Analyst Portal)

Built with React 19, TypeScript, Vite, and Tailwind CSS v4, the Web Dashboard provides security operations center (SOC) analysts and researchers with an interactive investigation interface:

* **Forensic URL Submission (`/`)**: Submit any suspicious URL for immediate analysis or trigger one-click presets from the simulated testbed.
* **Live Pipeline Monitor (`/analyze`)**: Visual step-by-step scanner animating data collection across all 6 stages (URL analysis, DOM parsing, Screenshot capture, OCR recognition, Cross-modal verification, and Meta-classification).
* **Comprehensive Investigation Dashboard (`/results`)**:
  * **Executive Verdict & Risk Meter**: Real-time gauge visualizing risk tier and probability calibrated against the empirical 78% operational threshold.
  * **Unimodal Probability Cards**: Isolated confidence ratings for URL, HTML, and Computer Vision models.
  * **Research Mode (Model Comparison)**: Side-by-side performance comparison showing why PhishAlign outperforms:
    * *Equal-Weight Fusion* ($P_{avg} = \frac{P_{url} + P_{html} + P_{vis}}{3}$)
    * *Naive Probability Stacking* ($\text{MetaLR}(P_{url}, P_{html}, P_{vis})$)
    * *PhishAlign Cross-Modal Fusion* ($\text{MetaLR}(P_{url}, P_{html}, P_{vis}, C_1, \dots, C_{25})$)
  * **25 Cross-Modal Consistency Matrix**: Interactive matrix checking URL-to-DOM asymmetry, DOM-to-Visual text overlap, brand identity consensus, and credential harvester flags.
  * **Visual Screenshot & OCR Viewer**: Inspect the captured page screenshot side-by-side with recognized text tokens and highlighted brand logos.
  * **SHAP Explainability Waterfall**: Interpretable bar chart ranking the top positive and negative feature contributions that drove the final classification.
* **Methodology & Publications (`/about`)**: Complete technical reference covering mathematics, benchmark metrics on Phish360, and research background.

---

## 🧠 Machine Learning & Consistency Pipeline

PhishAlign addresses the core failure mode of unimodal classifiers: **inter-modal deception**.

| Pipeline Stage | Algorithm / Framework | Dimensionality / Features | Execution Latency |
| :--- | :--- | :--- | :--- |
| **URL Analysis** | XGBoost Classifier | **31 Lexical Features** (entropy, token ratios, IP format, tld presence) | 12.0 ms |
| **HTML Analysis** | XGBoost Classifier | **64 Structural Features** (external action URLs, iframe hidden, password inputs) | 16.0 ms |
| **Visual Analysis** | MobileNetV3 + Tesseract OCR | **128-dim Embedding** + Brand Vector + OCR token alignment | 85.0 ms |
| **Consistency Engine** | Cross-Modal Verification | **25 Relational Features** (containment ratios, brand mismatch, visual-textual distance) | 18.0 ms |
| **Meta-Classifier** | Stacking Logistic Regression | **28-dim Vector** ($P_{url}, P_{html}, P_{vis} + 25\text{ consistency features}$) | 2.0 ms |
| **End-to-End** | **PhishAlign Stacking Model** | **ROC-AUC: 98.40% \| Precision: 96.80% \| Recall: 95.90%** | **~158 ms Total** |

---

## 📂 Project Directory Structure

```text
PhishAlign/
├── backend/                         # FastAPI AI Inference Backend
│   ├── app/
│   │   ├── main.py                  # API routes (/health, /analyze, /analyze_content)
│   │   ├── inference.py             # Inference coordinator & model pipeline
│   │   ├── page_capture.py          # Playwright stealth browser capture
│   │   ├── consistency.py           # 25 Cross-modal consistency feature extraction
│   │   ├── url_model.py             # 31-feature URL lexical model
│   │   ├── html_model.py            # 64-feature HTML DOM model
│   │   ├── visual_model.py          # MobileNetV3 visual brand matcher
│   │   └── ocr.py                   # Tesseract OCR extraction engine
│   ├── models/                      # Serialized ML model weights (.pkl / .pth)
│   └── main.py                      # Uvicorn entrypoint (Port 8000)
│
├── extension/                       # Chrome / Edge Browser Extension (Manifest V3)
│   ├── manifest.json                # MV3 extension configuration
│   ├── background.js                # Service worker: navigation interception & API bridge
│   ├── content.js                   # Content script: scanning banner & hard-block overlay
│   ├── popup.html                   # Extension toolbar popup interface
│   ├── popup.js                     # Popup state manager and visual risk meter
│   └── icons/                       # Shield icons (16px, 48px, 128px)
│
├── src/                             # React Web Dashboard (Analyst Portal)
│   ├── pages/                       # Route views (HomePage, AnalyzePage, ResultsPage, AboutPage)
│   ├── components/                  # UI components (RiskScore, ConsistencyMatrix, ResearchComparison, etc.)
│   ├── services/api.ts              # Live backend API client connection
│   └── App.tsx                      # Main routing & state setup
│
├── demo-phish/                      # Local Phishing Simulation Testbed Pages
│   ├── index.html                   # PayPal credential harvester simulation
│   ├── microsoft.html               # Microsoft 365 login spoof simulation
│   ├── google.html                  # Google accounts spoof simulation
│   └── server.py                    # Lightweight HTTP testbed server
│
├── report/                          # Academic Documentation & Engineering Report
│   ├── final_project_report.docx    # Complete 10-chapter academic report (~13 MB)
│   ├── build_report.py              # Automated Word document generation engine
│   ├── strict_verification_audit.py # 61-point automated verification audit suite
│   ├── diagrams/                    # 24 rendered 300-DPI high-contrast architecture figures
│   └── snapshots/                   # 24 uncropped evaluation and interface screenshots
│
├── pipeline.py                      # Demo testbed runner & automated scenario validator
├── start_pipeline.bat               # Windows double-click pipeline launcher
├── package.json                     # Node.js dependencies (React, Vite, Tailwind v4)
└── README.md                        # Unified project documentation
```

---

## ⚙️ Prerequisites

Before getting started, make sure you have the following installed on your machine:

1. **Python 3.10 to 3.13** (64-bit)
2. **Node.js 18+** (with `npm`)
3. **Google Chrome** or **Microsoft Edge** (for the extension)
4. *(Optional)* **Tesseract OCR**: If not installed system-wide, the backend will cleanly fall back to pure visual embeddings.

---

## 🚀 Quick Start Guide (Step-by-Step)

Follow these steps to run the complete PhishAlign ecosystem on your local machine:

### Step 1: Start the FastAPI AI Backend

Open a terminal and start the ML inference server:

```powershell
cd backend
python main.py
```
* **Host**: `http://127.0.0.1:8000`
* **Health Check**: `http://127.0.0.1:8000/health`
* **Swagger Interactive API Docs**: `http://127.0.0.1:8000/docs`

> [!TIP]
> Keep this terminal open. Both the Web Dashboard and the Browser Extension connect directly to port 8000.

---

### Step 2: Start the React Web Dashboard

Open a second terminal in the project root and launch the Vite development server:

```powershell
npm install
npm run dev
```
* **Web Dashboard**: `http://localhost:5173`

You can now navigate to `http://localhost:5173` in your browser to explore the Security Analyst Portal.

---

### Step 3: Load the Browser Extension

Load the extension into your browser in under 30 seconds:

1. Open **Google Chrome** and browse to `chrome://extensions` *(or **Edge** at `edge://extensions`)*.
2. Toggle on **Developer mode** in the top-right corner.
3. Click the **"Load unpacked"** button in the top-left toolbar.
4. Select the **`extension`** folder located in this repository:
   ```text
   C:\Users\<YourUser>\Desktop\projects\PhishAlign\extension
   ```
5. The **PhishAlign Shield Icon** 🛡️ will appear in your browser's extension bar. Pin it for easy viewing!

---

### Step 4: Launch the Phishing Simulation Testbed

To safely test the system against realistic phishing attacks without visiting active malicious sites on the internet, launch the built-in phishing testbed:

```powershell
python pipeline.py start
```
*(Or simply double-click `start_pipeline.bat` on Windows)*

* **Simulation Testbed Port**: `http://127.0.0.1:5050`
* **Available Simulated Scenarios**:
  * 🔴 **PayPal Harvester**: `http://127.0.0.1:5050/`
  * 🔴 **Microsoft 365 Spoof**: `http://127.0.0.1:5050/microsoft.html`
  * 🔴 **Google Accounts Spoof**: `http://127.0.0.1:5050/google.html`

---

## 🧪 Testing & Demonstration Scenarios

### Scenario A: Testing the Browser Extension
1. Ensure the backend (`:8000`) and testbed (`:5050`) are running.
2. In your browser, navigate to: `http://127.0.0.1:5050/`
3. **Observation**:
   - The extension immediately shows a scanning indicator in the top-right corner.
   - Within ~150 ms, the extension displays the **Red Full-Screen Hard-Block Intercept**.
   - The toolbar badge turns red with `98%`.
   - The block explains that while the visual branding looks like PayPal, the hosting domain is `127.0.0.1`, flagging an extreme cross-modal asymmetry.
   - Click **"Go Back to Safety"** to return or **"Proceed anyway"** to temporarily dismiss.

### Scenario B: Testing the Web Dashboard
1. Go to `http://localhost:5173`.
2. Under **Quick Demo Scenarios**, click **"PayPal Harvester"** (or type `http://127.0.0.1:5050/`).
3. Click **"Analyze Website"**.
4. Watch the 6-stage analysis pipeline animate in real time.
5. On the Results page:
   - Check the **Risk Meter** (displays Danger tier, ~98.4%).
   - Switch on **Research Mode** to observe how Equal-Weighting underestimates risk while PhishAlign catches the attack.
   - Open the **Consistency Matrix** to inspect the 25 cross-modal features.
   - Review the **SHAP Attribution Chart** to see which features drove the score.

### Scenario C: Testing Legitimate Websites
1. In the Web Dashboard or browser, navigate to a legitimate site such as:
   - `https://www.google.com`
   - `https://www.wikipedia.org`
   - `https://github.com`
2. **Observation**:
   - The Browser Extension badge displays a green checkmark `✓`.
   - The Web Dashboard classifies the site as **Safe (Risk < 10%)**, confirming zero false alarms on legitimate domains.

---

## 📡 API Reference

The FastAPI backend exposes the following REST endpoints:

### `GET /health`
Verifies backend connectivity and service availability.
```json
{
  "status": "ok"
}
```

---

### `POST /analyze_content`
**Used primarily by the Browser Extension (Layer 1 Direct)**. Accepts pre-captured live DOM and viewport screenshot directly from the browser context to eliminate scraping overhead and bypass anti-bot challenges.

**Request Body:**
```json
{
  "url": "http://127.0.0.1:5050/",
  "final_url": "http://127.0.0.1:5050/",
  "html": "<html>...</html>",
  "screenshot_b64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "page_title": "PayPal: Log In"
}
```

---

### `POST /analyze`
**Used by the Web Dashboard & Automated Scripts (Layer 2/3)**. Accepts a URL, navigates using Playwright Chromium with anti-detection headers, extracts the full page state, and runs inference.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response Payload (Summary):**
```json
{
  "requested_url": "http://127.0.0.1:5050/",
  "final_url": "http://127.0.0.1:5050/",
  "page_title": "PayPal: Log In",
  "prediction": "phishing",
  "risk_tier": "phishing",
  "phishalign_probability": 0.9842,
  "url_probability": 0.5210,
  "html_probability": 0.6840,
  "visual_probability": 0.9610,
  "equal_weight_probability": 0.7220,
  "probability_only_probability": 0.8140,
  "intent_signals": ["login_form_present", "credential_input", "brand_impersonation"],
  "consistency_features": {
    "brand_domain_match": 0.0,
    "html_visual_brand_similarity": 0.94,
    "url_dom_asymmetry_score": 0.89,
    "action_url_external_ratio": 1.0
  }
}
```

---

## 📚 Academic Report & Research Artifacts

All formal academic documentation, LaTeX/Word publication sources, 300-DPI publication figures, and audit scripts are isolated in the [`report/`](./report) directory:

- 📄 **[`final_project_report.docx`](./report/final_project_report.docx)**: Full 10-chapter academic project report formatted to university engineering guidelines.
- ⚙️ **Rebuild the Report**:
  ```powershell
  python report/build_report.py
  ```
- 🧪 **Run Strict 61-Test Verification Suite**:
  ```powershell
  python report/strict_verification_audit.py
  ```
  *(Audits section breaks, figure numbering, table consistency, equation syntax, and media references — 0 warnings, 0 issues).*

---

## ❓ Troubleshooting & FAQs

#### 1. The Browser Extension shows "Backend Disconnected 🔌"
* Ensure your backend server is running in a terminal:
  ```powershell
  cd backend
  python main.py
  ```
* Verify `http://127.0.0.1:8000/health` responds with `{"status": "ok"}` in your browser.

#### 2. Web Dashboard reports "Cannot connect to the PhishAlign backend"
* Ensure the backend is active on port `8000`. If you modified the port, update `API_BASE_URL` in `src/services/api.ts`.

#### 3. Playwright browser dependencies missing
* If running `POST /analyze` without the extension, install the Chromium headless binary:
  ```powershell
  playwright install chromium
  ```

#### 4. Demo testbed port 5050 already in use
* Check status or stop the existing testbed process with:
  ```powershell
  python pipeline.py status
  python pipeline.py stop
  ```

---

## 👥 Project & Academic Context

* **Project**: PhishAlign — Cross-Modal Consistency-Based Phishing Website Detection
* **Department**: Department of Computer Engineering
* **License**: MIT License
