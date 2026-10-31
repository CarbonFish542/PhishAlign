/**
 * PhishAlign — background service worker (Manifest V3)
 *
 * Lifecycle Flow:
 *  1. webNavigation.onCommitted: Marks tab PENDING and shows scanning overlay.
 *  2. webNavigation.onCompleted: Waits briefly for SPA hydration, verifies tab
 *     is active before capturing viewport screenshot, extracts live DOM, and
 *     dispatches to FastAPI (/analyze_content or fallback /analyze).
 */

const API_BASE = "http://127.0.0.1:8000";
const MIN_VALID_HTML_LENGTH = 250;
const SPA_HYDRATION_DELAY_MS = 450;

// In-memory cache: tabId → result | "pending" | "error"
const tabResults = new Map();

const TRUSTED_DOMAINS = [
  // Google
  "google.com", "gmail.com", "youtube.com", "youtube-nocookie.com",
  "googleapis.com", "gstatic.com", "googlevideo.com", "ggpht.com",
  "googleusercontent.com", "gemini.google.com", "accounts.google.com",
  // Microsoft
  "microsoft.com", "live.com", "outlook.com", "office.com",
  "office365.com", "microsoftonline.com", "bing.com", "azure.com",
  "cloud.microsoft", "sharepoint.com", "skype.com", "teams.microsoft.com",
  "microsoft",
  // Apple
  "apple.com", "icloud.com",
  // Social / Productivity / Dev
  "github.com", "gitlab.com", "twitter.com", "x.com",
  "facebook.com", "instagram.com", "linkedin.com", "reddit.com",
  "wikipedia.org", "wikimedia.org", "stackoverflow.com", "stackexchange.com",
  // Shopping & Education
  "amazon.com", "amazon.in", "flipkart.com", "apnacollege.in",
  // Streaming
  "netflix.com", "spotify.com", "twitch.tv", "discord.com",
  // Cloud / CDN
  "cloudflare.com", "fastly.net", "akamai.net",
];

function isTrustedDomain(url) {
  try {
    const hostname = new URL(url).hostname.toLowerCase();
    return TRUSTED_DOMAINS.some(
      (trusted) => hostname === trusted || hostname.endsWith("." + trusted)
    );
  } catch {
    return false;
  }
}

function isAnalyzable(url) {
  if (!url) return false;
  try {
    const u = new URL(url);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch {
    return false;
  }
}

async function persistResult(tabId, result) {
  await chrome.storage.local.set({ [`tab_${tabId}`]: result });
}

async function clearResult(tabId) {
  await chrome.storage.local.remove(`tab_${tabId}`);
}

async function messageTab(tabId, msg) {
  try {
    await chrome.tabs.sendMessage(tabId, msg);
  } catch {
    // Content script not ready or restricted browser page
  }
}

function setBadge(tabId, result) {
  if (!result || result === "pending") {
    chrome.action.setBadgeText({ text: "…", tabId });
    chrome.action.setBadgeBackgroundColor({ color: "#9e9e9e", tabId });
    return;
  }
  if (result === "error" || result.error) {
    chrome.action.setBadgeText({ text: "?", tabId });
    chrome.action.setBadgeBackgroundColor({ color: "#ff9800", tabId });
    return;
  }

  const pct = Math.round((result.phishalign_probability ?? 0) * 100);
  const tier = result.risk_tier ?? (result.prediction === "phishing" ? "phishing" : "legitimate");

  if (tier === "phishing") {
    chrome.action.setBadgeText({ text: `${pct}%`, tabId });
    chrome.action.setBadgeBackgroundColor({ color: "#d32f2f", tabId }); // Red
  } else if (tier === "suspicious") {
    chrome.action.setBadgeText({ text: `${pct}%`, tabId });
    chrome.action.setBadgeBackgroundColor({ color: "#f57c00", tabId }); // Amber
  } else {
    chrome.action.setBadgeText({ text: "✓", tabId });
    chrome.action.setBadgeBackgroundColor({ color: "#388e3c", tabId }); // Green
  }
}

/**
 * Captures the viewport screenshot ONLY if `tabId` is currently the active
 * foreground tab in its window, preventing background-tab screenshot mix-ups.
 */
async function captureTabScreenshotSafely(tabId) {
  try {
    const tab = await chrome.tabs.get(tabId);
    if (!tab || !tab.active) {
      return null;
    }
    const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, { format: "png" });
    return dataUrl.replace(/^data:image\/\w+;base64,/, "");
  } catch {
    return null;
  }
}

async function analyzeUrl(tabId, url) {
  if (isTrustedDomain(url)) {
    const trustedResult = {
      status: "done",
      url,
      prediction: "legitimate",
      risk_tier: "legitimate",
      phishalign_probability: 0.0,
      url_probability: 0.0,
      html_probability: 0.0,
      visual_probability: 0.0,
      equal_weight_probability: 0.0,
      page_title: "Trusted Domain",
      final_url: url,
      isTrusted: true,
    };
    tabResults.set(tabId, trustedResult);
    setBadge(tabId, trustedResult);
    await persistResult(tabId, trustedResult);
    await messageTab(tabId, { type: "PHISHALIGN_CLEAR" });
    return;
  }

  // Allow brief window for SPA frameworks (React/Vue/Next) to hydrate DOM after onCompleted
  await new Promise((r) => setTimeout(r, SPA_HYDRATION_DELAY_MS));

  let currentTab;
  try {
    currentTab = await chrome.tabs.get(tabId);
  } catch {
    return; // Tab was closed
  }

  // ── Layer 1: Direct capture from live browser tab ───────────
  let domData = null;
  try {
    domData = await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error("timeout")), 4000);
      chrome.tabs.sendMessage(tabId, { type: "PHISHALIGN_GET_HTML" }, (response) => {
        clearTimeout(timer);
        if (
          chrome.runtime.lastError ||
          !response?.html ||
          response.html.trim().length < MIN_VALID_HTML_LENGTH
        ) {
          reject(new Error(chrome.runtime.lastError?.message ?? "Insufficient HTML"));
        } else {
          resolve(response);
        }
      });
    });
  } catch {
    domData = null;
  }

  const screenshotB64 = await captureTabScreenshotSafely(tabId);

  let data;
  let isNetworkError = false;
  try {
    let response;

    if (domData && screenshotB64) {
      response = await fetch(`${API_BASE}/analyze_content`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url,
          final_url: domData.finalUrl ?? currentTab.url ?? url,
          html: domData.html,
          screenshot_b64: screenshotB64,
          page_title: domData.title ?? currentTab.title ?? "",
        }),
        signal: AbortSignal.timeout(30_000),
      });
    } else {
      // Fallback: /analyze via headless Playwright when tab is in background
      response = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: currentTab.url ?? url }),
        signal: AbortSignal.timeout(60_000),
      });
    }

    if (!response.ok) {
      let detail = `HTTP ${response.status}`;
      try {
        const body = await response.json();
        if (body.detail) detail = body.detail;
      } catch { /* ignore */ }
      throw new Error(detail);
    }

    data = await response.json();
  } catch (err) {
    isNetworkError = err.name === "TypeError" || err.name === "AbortError";
    const errorResult = {
      status: "error",
      url,
      error: err.message ?? "Backend unreachable",
      isNetworkError,
    };
    tabResults.set(tabId, errorResult);
    setBadge(tabId, "error");
    await persistResult(tabId, errorResult);
    await messageTab(tabId, {
      type: "PHISHALIGN_ERROR",
      error: err.message,
      isNetworkError,
    });
    return;
  }

  const result = {
    status: "done",
    url,
    prediction: data.prediction,
    risk_tier: data.risk_tier ?? data.prediction,
    phishalign_probability: data.phishalign_probability,
    raw_phishalign_probability: data.raw_phishalign_probability,
    url_probability: data.url_probability,
    html_probability: data.html_probability,
    visual_probability: data.visual_probability,
    equal_weight_probability: data.equal_weight_probability,
    intent_signals: data.intent_signals,
    page_title: data.page_title,
    final_url: data.final_url,
    screenshot_data_url: data.screenshot_data_url,
  };

  tabResults.set(tabId, result);
  setBadge(tabId, result);
  await persistResult(tabId, result);

  if (result.risk_tier === "phishing" || result.prediction === "phishing") {
    await messageTab(tabId, { type: "PHISHALIGN_PHISHING", result });
  } else if (result.risk_tier === "suspicious") {
    await messageTab(tabId, { type: "PHISHALIGN_SUSPICIOUS", result });
  } else {
    await messageTab(tabId, { type: "PHISHALIGN_CLEAR", result });
  }
}

// ──────────────────────────────────────────────────────────────
// Navigation Listeners
// ──────────────────────────────────────────────────────────────

// 1. Show scanning overlay as soon as navigation commits
chrome.webNavigation.onCommitted.addListener(
  async (details) => {
    if (details.frameId !== 0) return;
    if (!isAnalyzable(details.url)) return;

    const skipReasons = new Set(["auto_subframe", "manual_subframe"]);
    if (skipReasons.has(details.transitionType)) return;

    if (isTrustedDomain(details.url)) {
      await analyzeUrl(details.tabId, details.url);
      return;
    }

    tabResults.set(details.tabId, "pending");
    setBadge(details.tabId, "pending");
    await persistResult(details.tabId, { status: "pending", url: details.url });
    await messageTab(details.tabId, { type: "PHISHALIGN_SCANNING", url: details.url });
  },
  { url: [{ schemes: ["http", "https"] }] }
);

// 2. Capture live DOM & screenshot only after document load completes
chrome.webNavigation.onCompleted.addListener(
  async (details) => {
    if (details.frameId !== 0) return;
    if (!isAnalyzable(details.url)) return;
    if (isTrustedDomain(details.url)) return;

    await analyzeUrl(details.tabId, details.url);
  },
  { url: [{ schemes: ["http", "https"] }] }
);

chrome.tabs.onRemoved.addListener((tabId) => {
  tabResults.delete(tabId);
  clearResult(tabId);
});

// ──────────────────────────────────────────────────────────────
// Message handler
// ──────────────────────────────────────────────────────────────

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "GET_RESULT") {
    const tabId = msg.tabId;
    const inMemory = tabResults.get(tabId);
    if (inMemory !== undefined) {
      sendResponse({ result: inMemory });
      return true;
    }
    chrome.storage.local.get(`tab_${tabId}`, (items) => {
      sendResponse({ result: items[`tab_${tabId}`] ?? null });
    });
    return true;
  }

  if (msg.type === "REANALYZE") {
    const tabId = msg.tabId ?? sender?.tab?.id;
    if (tabId) {
      chrome.tabs.get(tabId, (tab) => {
        if (tab?.url && isAnalyzable(tab.url)) {
          analyzeUrl(tabId, tab.url);
        }
      });
    }
    sendResponse({ ok: true });
    return true;
  }

  if (msg.type === "ALLOW_ONCE") {
    const tabId = msg.tabId ?? sender?.tab?.id;
    if (tabId) {
      messageTab(tabId, { type: "PHISHALIGN_ALLOW" });
    }
    sendResponse({ ok: true });
    return true;
  }
});
