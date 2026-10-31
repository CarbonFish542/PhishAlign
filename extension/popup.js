/**
 * PhishAlign — Popup Controller (v2.0 3-Tier Risk Architecture)
 */

const STATES = ["pending", "analyzed", "error", "none"];

function showState(name) {
  STATES.forEach((s) => {
    const el = document.getElementById(`state-${s}`);
    if (el) el.classList.toggle("active", s === name);
  });
}

function fmt(prob) {
  if (prob == null || isNaN(prob)) return "—";
  return `${(prob * 100).toFixed(1)}%`;
}

function setHeaderPill(text, tierClass) {
  const pill = document.getElementById("status-pill");
  if (!pill) return;
  pill.textContent = text;
  pill.className = `status-pill ${tierClass}`;
}

function renderPending() {
  setHeaderPill("Scanning", "pending");
  showState("pending");
}

function renderError(result) {
  setHeaderPill("Offline", "error");
  const isNet = result?.isNetworkError;
  document.getElementById("err-icon").textContent = isNet ? "🔌" : "⚠️";
  document.getElementById("err-title").textContent = isNet
    ? "Backend Disconnected"
    : "Analysis Failed";
  document.getElementById("err-msg").textContent =
    result?.error ?? "Could not reach the PhishAlign API on port 8000.";
  showState("error");
}

function renderAnalyzed(result, tabId) {
  const tier = (result.risk_tier ?? result.prediction ?? "legitimate").toLowerCase();
  const prob = result.phishalign_probability ?? 0.0;
  const pct = (prob * 100).toFixed(1);

  // 1. Header Pill
  if (tier === "phishing") {
    setHeaderPill("Phishing", "phishing");
  } else if (tier === "suspicious") {
    setHeaderPill("Suspicious", "suspicious");
  } else {
    setHeaderPill(result.isTrusted ? "Verified" : "Safe", "legitimate");
  }

  // 2. Verdict Card
  const card = document.getElementById("verdict-card");
  const icon = document.getElementById("verdict-icon");
  const title = document.getElementById("verdict-title");
  const desc = document.getElementById("verdict-desc");
  const spoofAlert = document.getElementById("spoof-alert");
  const spoofText = document.getElementById("spoof-alert-text");

  card.className = `verdict-card ${tier}`;

  const intent = result.intent_signals ?? {};
  const brand = intent.impersonated_brand;

  if (tier === "phishing") {
    icon.textContent = "🚨";
    title.textContent = "High-Risk Phishing Threat";
    desc.textContent =
      "This website attempts to deceive users by harvesting credentials or spoofing trusted entities.";
    if (brand) {
      spoofAlert.classList.add("active");
      spoofText.textContent = `Impersonating ${brand.toUpperCase()} on an unauthorized host.`;
    } else {
      spoofAlert.classList.remove("active");
    }
  } else if (tier === "suspicious") {
    icon.textContent = "⚠️";
    title.textContent = "Caution: Elevated Risk";
    desc.textContent =
      "Suspicious login or structural patterns detected. Proceed with caution and verify the domain.";
    if (brand) {
      spoofAlert.classList.add("active");
      spoofText.textContent = `Potential spoof of ${brand.toUpperCase()} detected.`;
    } else {
      spoofAlert.classList.remove("active");
    }
  } else {
    icon.textContent = "✅";
    title.textContent = result.isTrusted ? "Verified Trusted Domain" : "Authentic Website";
    desc.textContent =
      "No credential harvesting, brand impersonation, or deceptive indicators detected.";
    spoofAlert.classList.remove("active");
  }

  // 3. Risk Meter
  const scoreEl = document.getElementById("meter-score");
  const fillEl = document.getElementById("meter-fill");

  scoreEl.textContent = `${pct}%`;
  scoreEl.className = `meter-score ${tier === "phishing" ? "danger" : tier === "suspicious" ? "warn" : "safe"}`;
  fillEl.className = `meter-fill ${tier === "phishing" ? "danger" : tier === "suspicious" ? "warn" : "safe"}`;
  fillEl.style.width = `${Math.min(Math.max(prob * 100, 3), 100)}%`;

  // 4. Modalities Breakdown
  const urlEl = document.getElementById("mod-url");
  const htmlEl = document.getElementById("mod-html");
  const visEl = document.getElementById("mod-visual");

  const urlProb = result.url_probability ?? 0.0;
  const htmlProb = result.html_probability ?? 0.0;
  const visProb = result.visual_probability ?? 0.0;

  urlEl.textContent = fmt(urlProb);
  urlEl.className = `mod-val ${urlProb >= 0.78 ? "danger" : urlProb >= 0.50 ? "warn" : "safe"}`;

  htmlEl.textContent = fmt(htmlProb);
  htmlEl.className = `mod-val ${htmlProb >= 0.78 ? "danger" : htmlProb >= 0.50 ? "warn" : "safe"}`;

  visEl.textContent = fmt(visProb);
  visEl.className = `mod-val ${visProb >= 0.78 ? "danger" : visProb >= 0.50 ? "warn" : "safe"}`;

  // 5. Intent Signals Chips
  const signalsList = document.getElementById("signals-list");
  signalsList.innerHTML = "";

  if (brand) {
    const chip = document.createElement("span");
    chip.className = "signal-chip danger";
    chip.textContent = `🎯 Spoofed Brand: ${brand.toUpperCase()}`;
    signalsList.appendChild(chip);
  }

  if (intent.has_login_form) {
    const chip = document.createElement("span");
    chip.className = `signal-chip ${tier === "phishing" ? "danger" : "warn"}`;
    chip.textContent = "🔑 Credential Form";
    signalsList.appendChild(chip);
  }

  if (intent.suspicious_form_action) {
    const chip = document.createElement("span");
    chip.className = "signal-chip danger";
    chip.textContent = "📡 External Exfiltration Action";
    signalsList.appendChild(chip);
  }

  if (intent.is_free_host) {
    const chip = document.createElement("span");
    chip.className = "signal-chip warn";
    chip.textContent = "☁️ Free/Tunnel Host";
    signalsList.appendChild(chip);
  }

  if (intent.is_self_consistent) {
    const chip = document.createElement("span");
    chip.className = "signal-chip safe";
    chip.textContent = "✓ Domain Self-Consistent";
    signalsList.appendChild(chip);
  }

  if (signalsList.children.length === 0) {
    const chip = document.createElement("span");
    chip.className = "signal-chip safe";
    chip.textContent = "✓ Standard Web Surface";
    signalsList.appendChild(chip);
  }

  // 6. Action Buttons
  const actionsContainer = document.getElementById("actions-container");
  actionsContainer.innerHTML = "";

  if (tier === "phishing") {
    const backBtn = document.createElement("button");
    backBtn.className = "btn btn-danger";
    backBtn.innerHTML = "← Return to Safety";
    backBtn.addEventListener("click", () => {
      chrome.tabs.goBack(tabId);
      window.close();
    });

    const proceedBtn = document.createElement("button");
    proceedBtn.className = "btn btn-ghost";
    proceedBtn.innerHTML = "Proceed Anyway (I accept risk)";
    proceedBtn.addEventListener("click", () => {
      chrome.runtime.sendMessage({ type: "ALLOW_ONCE", tabId });
      window.close();
    });

    actionsContainer.appendChild(backBtn);
    actionsContainer.appendChild(proceedBtn);
  } else if (tier === "suspicious") {
    const reBtn = document.createElement("button");
    reBtn.className = "btn btn-warn";
    reBtn.innerHTML = "🔄 Re-scan Page";
    reBtn.addEventListener("click", () => {
      chrome.runtime.sendMessage({ type: "REANALYZE", tabId });
      renderPending();
    });

    const dismissBtn = document.createElement("button");
    dismissBtn.className = "btn btn-ghost";
    dismissBtn.innerHTML = "Acknowledge Caution";
    dismissBtn.addEventListener("click", () => {
      chrome.runtime.sendMessage({ type: "ALLOW_ONCE", tabId });
      window.close();
    });

    actionsContainer.appendChild(reBtn);
    actionsContainer.appendChild(dismissBtn);
  } else {
    const reBtn = document.createElement("button");
    reBtn.className = "btn btn-ghost";
    reBtn.innerHTML = "🔄 Re-scan Page";
    reBtn.addEventListener("click", () => {
      chrome.runtime.sendMessage({ type: "REANALYZE", tabId });
      renderPending();
    });
    actionsContainer.appendChild(reBtn);
  }

  // 7. URL Strip
  const urlStrip = document.getElementById("url-strip");
  urlStrip.textContent = result.final_url || result.url || "";

  showState("analyzed");
}

// ──────────────────────────────────────────────────────────────
// Initialization
// ──────────────────────────────────────────────────────────────

async function init() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) {
    showState("none");
    return;
  }

  const tabId = tab.id;

  // Error retry listeners
  document.getElementById("btn-err-retry")?.addEventListener("click", () => {
    chrome.runtime.sendMessage({ type: "REANALYZE", tabId });
    renderPending();
  });

  document.getElementById("btn-err-ignore")?.addEventListener("click", () => {
    chrome.runtime.sendMessage({ type: "ALLOW_ONCE", tabId });
    window.close();
  });

  // Query background for current tab status
  chrome.runtime.sendMessage({ type: "GET_RESULT", tabId }, (response) => {
    const result = response?.result;

    if (!result) {
      showState("none");
      return;
    }

    if (result === "pending" || result?.status === "pending") {
      renderPending();
      return;
    }

    if (result === "error" || result?.status === "error") {
      renderError(result);
      return;
    }

    renderAnalyzed(result, tabId);
  });
}

document.addEventListener("DOMContentLoaded", init);
