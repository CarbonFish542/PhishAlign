/**
 * PhishAlign — content script
 *
 * Injected at document_start into every http/https page.
 * Listens for messages from the background service worker and renders:
 *  - A grey "scanning…" overlay while the backend analyses the page
 *  - A full-page hard-block overlay when phishing is detected
 *  - Nothing when the page is legitimate
 */

(function () {
  "use strict";

  // Prevent double-injection in edge cases
  if (window.__phishAlignInjected) return;
  window.__phishAlignInjected = true;

  // ────────────────────────────────────────────────────────────
  // Overlay element management
  // ────────────────────────────────────────────────────────────

  let overlay = null;
  let allowed = false; // user clicked "Proceed anyway"

  function removeOverlay() {
    if (overlay) {
      overlay.remove();
      overlay = null;
    }
  }

  function createOverlayRoot() {
    removeOverlay();
    overlay = document.createElement("div");
    overlay.id = "__phishalign_overlay__";
    // Isolate styles from page CSS
    overlay.style.cssText = `
      all: initial;
      position: fixed;
      inset: 0;
      z-index: 2147483647;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;
    // Use a shadow root to fully isolate our UI
    const shadow = overlay.attachShadow({ mode: "closed" });
    document.documentElement.appendChild(overlay);
    return shadow;
  }

  // ────────────────────────────────────────────────────────────
  // Scanning overlay
  // ────────────────────────────────────────────────────────────

  function showScanning() {
    if (allowed) return;
    const shadow = createOverlayRoot();
    shadow.innerHTML = `
      <style>
        :host { display: block; width: 100%; height: 100%; }
        .wrap {
          width: 100%; height: 100%;
          background: rgba(30,30,30,0.82);
          backdrop-filter: blur(4px);
          display: flex; flex-direction: column;
          align-items: center; justify-content: center;
          color: #fff;
        }
        .logo { font-size: 28px; font-weight: 700; letter-spacing: 1px; margin-bottom: 12px; }
        .logo span { color: #ef5350; }
        .msg { font-size: 15px; opacity: .85; margin-top: 4px; }
        .spinner {
          width: 48px; height: 48px;
          border: 4px solid rgba(255,255,255,.3);
          border-top-color: #ef5350;
          border-radius: 50%;
          animation: spin .9s linear infinite;
          margin-bottom: 20px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
      </style>
      <div class="wrap">
        <div class="spinner"></div>
        <div class="logo">Phish<span>Align</span></div>
        <div class="msg">Scanning page for phishing threats…</div>
      </div>
    `;
  }

  // ────────────────────────────────────────────────────────────
  // Phishing block overlay
  // ────────────────────────────────────────────────────────────

  function showBlock(result) {
    if (allowed) return;

    const shadow = createOverlayRoot();
    const prob = result?.phishalign_probability ?? 0;
    const pct = (prob * 100).toFixed(1);
    const urlProb = ((result?.url_probability ?? 0) * 100).toFixed(1);
    const htmlProb = ((result?.html_probability ?? 0) * 100).toFixed(1);
    const visualProb = ((result?.visual_probability ?? 0) * 100).toFixed(1);
    const pageUrl = result?.url ?? window.location.href;

    shadow.innerHTML = `
      <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :host { display: block; width: 100%; height: 100%; }

        .page {
          width: 100%; height: 100%;
          background: linear-gradient(135deg, #1a0000 0%, #3b0000 100%);
          display: flex; align-items: center; justify-content: center;
          padding: 20px;
        }

        .card {
          background: #1e1e1e;
          border: 1.5px solid #ef5350;
          border-radius: 16px;
          max-width: 640px;
          width: 100%;
          padding: 40px 36px;
          box-shadow: 0 0 60px rgba(239,83,80,.3);
          color: #fff;
        }

        .header {
          display: flex; align-items: center; gap: 14px;
          margin-bottom: 24px;
        }
        .shield {
          width: 56px; height: 56px; flex-shrink: 0;
          background: #ef5350;
          border-radius: 50%;
          display: flex; align-items: center; justify-content: center;
          font-size: 26px;
        }
        .title-block h1 {
          font-size: 22px; font-weight: 700;
          color: #ef5350;
          line-height: 1.2;
        }
        .title-block p {
          font-size: 13px; color: #bbb; margin-top: 2px;
        }

        .risk-bar-wrap { margin-bottom: 28px; }
        .risk-label {
          display: flex; justify-content: space-between;
          font-size: 13px; color: #aaa; margin-bottom: 6px;
        }
        .risk-label strong { color: #ef5350; font-size: 20px; }
        .bar-bg {
          background: #333; border-radius: 6px; height: 10px; overflow: hidden;
        }
        .bar-fill {
          height: 100%;
          background: linear-gradient(90deg, #ff7043, #ef5350, #b71c1c);
          border-radius: 6px;
          transition: width .6s ease;
        }

        .modalities {
          display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;
          margin-bottom: 28px;
        }
        .mod {
          background: #2a2a2a; border-radius: 10px; padding: 12px 10px;
          text-align: center;
        }
        .mod-name { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: .5px; }
        .mod-val {
          font-size: 20px; font-weight: 700; margin-top: 4px;
          color: #ef5350;
        }

        .url-box {
          background: #111; border-radius: 8px; padding: 10px 14px;
          font-size: 12px; color: #bbb; word-break: break-all;
          margin-bottom: 28px;
          border: 1px solid #333;
        }
        .url-box span { color: #888; font-size: 11px; display: block; margin-bottom: 3px; }

        .actions { display: flex; flex-direction: column; gap: 10px; }
        .btn-safe {
          background: #388e3c; color: #fff;
          border: none; border-radius: 10px;
          padding: 14px 20px;
          font-size: 15px; font-weight: 600;
          cursor: pointer;
          transition: background .2s;
        }
        .btn-safe:hover { background: #2e7d32; }
        .btn-proceed {
          background: transparent; color: #888;
          border: 1px solid #444; border-radius: 10px;
          padding: 11px 20px;
          font-size: 13px;
          cursor: pointer;
          transition: all .2s;
        }
        .btn-proceed:hover { color: #ccc; border-color: #666; }

        .footer {
          margin-top: 24px; text-align: center;
          font-size: 11px; color: #555;
        }
      </style>

      <div class="page">
        <div class="card">
          <div class="header">
            <div class="shield">🛡️</div>
            <div class="title-block">
              <h1>Phishing Site Detected</h1>
              <p>PhishAlign has blocked this page for your protection.</p>
            </div>
          </div>

          <div class="risk-bar-wrap">
            <div class="risk-label">
              <span>Phishing Probability</span>
              <strong>${pct}%</strong>
            </div>
            <div class="bar-bg">
              <div class="bar-fill" style="width: ${pct}%;"></div>
            </div>
          </div>

          <div class="modalities">
            <div class="mod">
              <div class="mod-name">URL Model</div>
              <div class="mod-val">${urlProb}%</div>
            </div>
            <div class="mod">
              <div class="mod-name">HTML Model</div>
              <div class="mod-val">${htmlProb}%</div>
            </div>
            <div class="mod">
              <div class="mod-name">Visual Model</div>
              <div class="mod-val">${visualProb}%</div>
            </div>
          </div>

          <div class="url-box">
            <span>Blocked URL</span>
            ${pageUrl}
          </div>

          <div class="actions">
            <button class="btn-safe" id="__pa_back__">← Go Back to Safety</button>
            <button class="btn-proceed" id="__pa_proceed__">I understand the risk — proceed anyway</button>
          </div>

          <div class="footer">
            Powered by PhishAlign · Cross-modal consistency-based detection
          </div>
        </div>
      </div>
    `;

    shadow.getElementById("__pa_back__").addEventListener("click", () => {
      history.back();
      // If no history, close tab
      setTimeout(() => { window.close(); }, 500);
    });

    shadow.getElementById("__pa_proceed__").addEventListener("click", () => {
      allowed = true;
      removeOverlay();
    });
  }

  // ────────────────────────────────────────────────────────────
  // Error overlay (backend unreachable)
  // ────────────────────────────────────────────────────────────

  function showError(errorMsg, isNetworkError) {
    if (allowed) return;
    const shadow = createOverlayRoot();
    const title = isNetworkError
      ? "PhishAlign Backend Unreachable"
      : "Page Cannot Be Scanned";
    const hint = isNetworkError
      ? "Could not connect to the PhishAlign backend on port 8000. Make sure the FastAPI server is running."
      : (errorMsg ?? "The backend could not analyse this page.");
    shadow.innerHTML = `
      <style>
        :host { display: block; width: 100%; height: 100%; }
        .wrap {
          width: 100%; height: 100%;
          background: rgba(30,30,30,0.88);
          display: flex; flex-direction: column;
          align-items: center; justify-content: center;
          color: #fff; gap: 12px;
        }
        .icon { font-size: 40px; }
        h2 { font-size: 18px; }
        p { font-size: 13px; color: #aaa; max-width: 400px; text-align: center; }
        .detail { font-size: 11px; color: #666; max-width: 400px; text-align: center; font-family: monospace; }
        button {
          margin-top: 8px;
          background: #1565c0; color: #fff;
          border: none; border-radius: 8px;
          padding: 10px 20px; font-size: 14px; cursor: pointer;
        }
        button:hover { background: #0d47a1; }
        .dismiss {
          background: transparent; color: #888;
          border: 1px solid #555; margin-top: 4px;
        }
      </style>
      <div class="wrap">
        <div class="icon">${isNetworkError ? "🔌" : "⚠️"}</div>
        <h2>${title}</h2>
        <p>${hint}</p>
        ${!isNetworkError && errorMsg ? `<div class="detail">${errorMsg}</div>` : ""}
        <button id="__pa_retry__">🔄 Retry Scan</button>
        <button class="dismiss" id="__pa_dismiss__">Continue without protection</button>
      </div>
    `;
    shadow.getElementById("__pa_retry__").addEventListener("click", () => {
      chrome.runtime.sendMessage({ type: "REANALYZE", tabId: chrome._tabId });
    });
    shadow.getElementById("__pa_dismiss__").addEventListener("click", () => {
      allowed = true;
      removeOverlay();
    });
  }

  // ────────────────────────────────────────────────────────────
  // Suspicious floating warning banner (non-intrusive)
  // ────────────────────────────────────────────────────────────

  function showSuspiciousBanner(result) {
    if (allowed) return;
    removeOverlay();
    overlay = document.createElement("div");
    overlay.id = "__phishalign_banner__";
    overlay.style.cssText = `
      all: initial;
      position: fixed;
      top: 12px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 2147483647;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;
    const shadow = overlay.attachShadow({ mode: "closed" });
    document.documentElement.appendChild(overlay);

    const prob = ((result?.phishalign_probability ?? 0.5) * 100).toFixed(1);
    const brand = result?.intent_signals?.impersonated_brand;
    const alertMsg = brand
      ? `Potential spoof of ${brand.toUpperCase()} detected.`
      : `Elevated risk signals detected (${prob}% probability).`;

    shadow.innerHTML = `
      <style>
        .banner {
          background: #1c1917;
          color: #fef3c7;
          border: 1px solid #f59e0b;
          border-radius: 12px;
          padding: 10px 16px;
          display: flex;
          align-items: center;
          gap: 12px;
          box-shadow: 0 10px 30px rgba(0,0,0,0.6);
          font-size: 13px;
        }
        .icon { font-size: 18px; }
        .text strong { color: #fbbf24; }
        .btn-dismiss {
          background: #292524;
          border: 1px solid #78350f;
          color: #fde68a;
          border-radius: 6px;
          padding: 5px 12px;
          font-size: 11px;
          font-weight: 600;
          cursor: pointer;
          white-space: nowrap;
        }
        .btn-dismiss:hover { background: #44403c; }
      </style>
      <div class="banner">
        <span class="icon">⚠️</span>
        <div class="text">
          <strong>PhishAlign Caution:</strong> ${alertMsg} Verify authenticity before entering passwords.
        </div>
        <button class="btn-dismiss" id="__pa_dismiss_banner__">Dismiss</button>
      </div>
    `;

    shadow.getElementById("__pa_dismiss_banner__").addEventListener("click", () => {
      allowed = true;
      removeOverlay();
    });
  }

  // ────────────────────────────────────────────────────────────
  // Message listener
  // ────────────────────────────────────────────────────────────

  chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
    switch (msg.type) {
      case "PHISHALIGN_SCANNING":
        showScanning();
        break;
      case "PHISHALIGN_SUSPICIOUS":
        showSuspiciousBanner(msg.result);
        break;
      case "PHISHALIGN_PHISHING":
        showBlock(msg.result);
        break;
      case "PHISHALIGN_CLEAR":
        removeOverlay();
        break;
      case "PHISHALIGN_ERROR":
        showError(msg.error, msg.isNetworkError);
        break;
      case "PHISHALIGN_ALLOW":
        allowed = true;
        removeOverlay();
        break;

      // Layer 1: background.js requests live DOM so backend doesn't
      // need to re-fetch via Playwright (bypasses Cloudflare / login walls)
      case "PHISHALIGN_GET_HTML":
        sendResponse({
          html: document.documentElement.outerHTML,
          title: document.title,
          finalUrl: window.location.href,
        });
        return true; // keep channel open for async sendResponse
    }
  });

  // Show scanning immediately if the service worker already started
  // (handles case where content script loads after background.js fired)
  chrome.storage.local.get(`tab_${chrome.runtime.id}`, () => {
    // noop — just ensures storage is accessible (warms connection)
  });
})();
