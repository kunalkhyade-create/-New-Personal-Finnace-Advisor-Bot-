/**
 * main.js — Personal Finance Advisor Bot
 * Handles form submission, async fetch to /analyse, dynamic result rendering,
 * and seamless API key configuration / Smart Advisory engine toggling.
 */

"use strict";

/* ------------------------------------------------------------------
   DOM References
------------------------------------------------------------------ */
const form               = document.getElementById("finance-form");
const submitBtn          = document.getElementById("submit-btn");
const btnText            = document.getElementById("btn-text");
const btnLoader          = document.getElementById("btn-loader");
const errorBanner        = document.getElementById("error-banner");
const resultsSection     = document.getElementById("results-section");
const summaryText        = document.getElementById("summary-text");
const engineBadge        = document.getElementById("engine-badge");
const budgetContainer    = document.getElementById("budget-container");
const analysisContainer  = document.getElementById("analysis-container");
const suggestionsContainer = document.getElementById("suggestions-container");

// API Key Modal Elements
const apiKeyBtn          = document.getElementById("api-key-btn");
const navModeText        = document.getElementById("nav-mode-text");
const apiKeyModal        = document.getElementById("api-key-modal");
const modalCloseBtn      = document.getElementById("modal-close-btn");
const geminiKeyInput     = document.getElementById("gemini-key-input");
const toggleKeyVisBtn    = document.getElementById("toggle-key-visibility");
const saveKeyBtn         = document.getElementById("save-key-btn");
const clearKeyBtn        = document.getElementById("clear-key-btn");
const modalFeedback      = document.getElementById("modal-feedback");

/* ------------------------------------------------------------------
   Category icon map (mirrors CATEGORY_TIPS in app.py)
------------------------------------------------------------------ */
const CATEGORY_ICONS = {
  "rent":          "fa-home",
  "food":          "fa-shopping-basket",
  "transport":     "fa-car",
  "dining":        "fa-utensils",
  "entertainment": "fa-film",
  "utilities":     "fa-bolt",
  "savings":       "fa-piggy-bank",
  "health":        "fa-heartbeat",
  "education":     "fa-graduation-cap",
  "shopping":      "fa-bag-shopping",
  "other":         "fa-ellipsis",
};

/* ------------------------------------------------------------------
   API Key Management
------------------------------------------------------------------ */
const STORAGE_KEY = "financebot_gemini_key";

function getStoredApiKey() {
  const key = localStorage.getItem(STORAGE_KEY) || "";
  return key.trim();
}

function updateNavAiStatus(isGeminiActive) {
  if (!navModeText || !apiKeyBtn) return;
  if (isGeminiActive) {
    navModeText.innerHTML = '<i class="fa-solid fa-sparkles"></i> Gemini 2.0 AI';
    apiKeyBtn.classList.add("active-ai");
  } else {
    navModeText.innerHTML = '<i class="fa-solid fa-bolt"></i> Smart Advisor';
    apiKeyBtn.classList.remove("active-ai");
  }
}

async function syncApiKeyStatus() {
  const localKey = getStoredApiKey();
  if (localKey) {
    updateNavAiStatus(true);
    return;
  }

  // Check backend .env configuration
  try {
    const res = await fetch("/api/key-status");
    if (res.ok) {
      const data = await res.json();
      updateNavAiStatus(data.configured);
    }
  } catch (e) {
    console.debug("Could not reach /api/key-status", e);
  }
}

// Modal open/close handlers
if (apiKeyBtn) {
  apiKeyBtn.addEventListener("click", () => {
    const currentKey = getStoredApiKey();
    if (geminiKeyInput) geminiKeyInput.value = currentKey;
    if (modalFeedback) {
      modalFeedback.className = "modal-feedback hidden";
      modalFeedback.textContent = "";
    }
    apiKeyModal.classList.remove("hidden");
    if (geminiKeyInput) geminiKeyInput.focus();
  });
}

if (modalCloseBtn) {
  modalCloseBtn.addEventListener("click", () => {
    apiKeyModal.classList.add("hidden");
  });
}

// Close when clicking modal backdrop
if (apiKeyModal) {
  apiKeyModal.addEventListener("click", (e) => {
    if (e.target === apiKeyModal) {
      apiKeyModal.classList.add("hidden");
    }
  });
}

// Toggle password visibility
if (toggleKeyVisBtn && geminiKeyInput) {
  toggleKeyVisBtn.addEventListener("click", () => {
    const isPassword = geminiKeyInput.type === "password";
    geminiKeyInput.type = isPassword ? "text" : "password";
    toggleKeyVisBtn.innerHTML = isPassword
      ? '<i class="fa-regular fa-eye-slash"></i>'
      : '<i class="fa-regular fa-eye"></i>';
  });
}

// Save Key
if (saveKeyBtn && geminiKeyInput) {
  saveKeyBtn.addEventListener("click", async () => {
    const key = geminiKeyInput.value.trim();
    if (!key) {
      showModalFeedback("Please enter a valid Gemini API key or click 'Use Smart Engine'.", "error");
      return;
    }

    try {
      // Send to server to persist in .env if writable
      const res = await fetch("/api/key-status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: key }),
      });
      const data = await res.json();
      
      localStorage.setItem(STORAGE_KEY, key);
      updateNavAiStatus(true);
      showModalFeedback("Key activated! Live Gemini 2.0 AI mode is now on.", "success");
      setTimeout(() => {
        apiKeyModal.classList.add("hidden");
      }, 1200);
    } catch (err) {
      // Fallback: save to localStorage anyway so request can pass it
      localStorage.setItem(STORAGE_KEY, key);
      updateNavAiStatus(true);
      showModalFeedback("Key saved in browser! Live Gemini AI is active.", "success");
      setTimeout(() => {
        apiKeyModal.classList.add("hidden");
      }, 1200);
    }
  });
}

// Clear key / revert to Smart Advisory Engine
if (clearKeyBtn) {
  clearKeyBtn.addEventListener("click", () => {
    localStorage.removeItem(STORAGE_KEY);
    if (geminiKeyInput) geminiKeyInput.value = "";
    updateNavAiStatus(false);
    showModalFeedback("Switched to built-in Smart Advisory Engine (No key needed).", "success");
    setTimeout(() => {
      apiKeyModal.classList.add("hidden");
    }, 1000);
  });
}

function showModalFeedback(msg, type) {
  if (!modalFeedback) return;
  modalFeedback.textContent = msg;
  modalFeedback.className = `modal-feedback ${type}`;
}

/* ------------------------------------------------------------------
   Helpers
------------------------------------------------------------------ */

/**
 * Format a number as an Indian-locale rupee string.
 */
function formatRupee(amount) {
  if (typeof amount !== "number" || isNaN(amount)) return "₹0";
  return "₹" + Math.round(amount).toLocaleString("en-IN");
}

/**
 * Derive icon class from category name.
 */
function iconFor(category) {
  const key = category.toLowerCase().replace(/[^a-z]/g, "");
  for (const [k, v] of Object.entries(CATEGORY_ICONS)) {
    if (key.includes(k) || k.includes(key)) return v;
  }
  return "fa-circle-dot";
}

/**
 * Clamp a value between min and max.
 */
function clamp(val, min, max) {
  return Math.min(Math.max(val, min), max);
}

/**
 * Show or hide loading state on the submit button.
 */
function setLoading(loading) {
  submitBtn.disabled = loading;
  btnText.classList.toggle("hidden", loading);
  btnLoader.classList.toggle("hidden", !loading);
}

/**
 * Display an error message in the error banner.
 */
function showError(message) {
  errorBanner.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${message}`;
  errorBanner.classList.remove("hidden");
  errorBanner.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

/**
 * Hide the error banner.
 */
function clearError() {
  errorBanner.classList.add("hidden");
  errorBanner.textContent = "";
}

/* ------------------------------------------------------------------
   Form Collection
------------------------------------------------------------------ */
function collectFormData() {
  const income = parseFloat(document.getElementById("income").value);
  if (!income || income <= 0) {
    showError("Please enter a valid monthly income greater than ₹0.");
    return null;
  }

  const goal = document.getElementById("goal").value;

  const expenseInputs = document.querySelectorAll(".expense-input");
  const expenses = {};
  expenseInputs.forEach((input) => {
    const val = parseFloat(input.value);
    if (val > 0) {
      expenses[input.name] = val;
    }
  });

  if (Object.keys(expenses).length === 0) {
    showError("Please enter at least one expense amount.");
    return null;
  }

  const payload = { income, expenses, goal };
  const storedKey = getStoredApiKey();
  if (storedKey) {
    payload.api_key = storedKey;
  }

  return payload;
}

/* ------------------------------------------------------------------
   Render Functions
------------------------------------------------------------------ */
function renderBudget(budget) {
  budgetContainer.innerHTML = "";

  if (!budget || budget.length === 0) {
    budgetContainer.innerHTML = '<p style="color:var(--clr-text-dim);font-size:0.85rem;">No budget data available.</p>';
    return;
  }

  budget.forEach((item) => {
    const status      = (item.status || "ok").toLowerCase();
    const actual      = item.actual     || 0;
    const recommended = item.recommended || 0;
    const pct         = item.percentage  || 0;

    const usagePct = recommended > 0
      ? clamp(Math.round((actual / recommended) * 100), 0, 100)
      : 0;

    const icon     = iconFor(item.category || "");
    const category = item.category || "Category";
    const tip      = item.tip || "";

    const el = document.createElement("div");
    el.className = "budget-item";
    el.innerHTML = `
      <div class="budget-item-header">
        <div class="budget-category">
          <i class="fa-solid ${icon}"></i>
          <span>${escapeHtml(category)}</span>
        </div>
        <span class="status-badge ${status}">${status.toUpperCase()}</span>
      </div>
      <div class="budget-amounts">
        <span class="actual">${formatRupee(actual)}</span>
        <span class="divider">/</span>
        <span class="recommended">${formatRupee(recommended)}</span>
        <span style="color:var(--clr-text-dim);margin-left:4px;">(${pct}%)</span>
      </div>
      <div class="progress-bar-track">
        <div class="progress-bar-fill ${status}" style="width: 0%" data-target="${usagePct}"></div>
      </div>
      ${tip ? `<p class="budget-tip"><i class="fa-solid fa-lightbulb" style="color:var(--clr-warn);margin-right:4px;"></i>${escapeHtml(tip)}</p>` : ""}
    `;

    budgetContainer.appendChild(el);

    requestAnimationFrame(() => {
      const fill = el.querySelector(".progress-bar-fill");
      if (fill) {
        setTimeout(() => {
          fill.style.width = fill.dataset.target + "%";
        }, 80);
      }
    });
  });
}

function renderAnalysis(analysis) {
  analysisContainer.innerHTML = "";

  if (!analysis || analysis.length === 0) {
    analysisContainer.innerHTML = '<p style="color:var(--clr-text-dim);font-size:0.85rem;">No analysis data available.</p>';
    return;
  }

  analysis.forEach((item) => {
    const status     = (item.status || "ok").toLowerCase();
    const pctUsed    = item.percentage_used || 0;
    const insight    = item.insight || "";
    const category   = item.category || "Category";

    const chip = document.createElement("div");
    chip.className = `analysis-chip ${status}`;
    chip.innerHTML = `
      <div class="chip-left">
        <div class="chip-category">${escapeHtml(category)}</div>
        ${insight ? `<div class="chip-insight">${escapeHtml(insight)}</div>` : ""}
      </div>
      <div class="chip-pct ${status}">${pctUsed}%</div>
    `;

    analysisContainer.appendChild(chip);
  });
}

function renderSuggestions(suggestions) {
  suggestionsContainer.innerHTML = "";

  if (!suggestions || suggestions.length === 0) {
    suggestionsContainer.innerHTML = '<li style="color:var(--clr-text-dim);font-size:0.85rem;list-style:none;">No suggestions available.</li>';
    return;
  }

  suggestions.forEach((suggestion) => {
    const li = document.createElement("li");
    li.textContent = suggestion;
    suggestionsContainer.appendChild(li);
  });
}

function renderResults(data) {
  if (data.summary) {
    summaryText.textContent = data.summary;
  }

  // Update engine badge
  if (engineBadge) {
    if (data.source === "gemini") {
      engineBadge.className = "engine-badge gemini";
      engineBadge.innerHTML = '<i class="fa-solid fa-sparkles"></i> Gemini 2.0 AI';
    } else {
      engineBadge.className = "engine-badge smart";
      engineBadge.innerHTML = '<i class="fa-solid fa-brain"></i> Smart Advisor';
    }
  }

  renderBudget(data.budget);
  renderAnalysis(data.analysis);
  renderSuggestions(data.suggestions);

  resultsSection.classList.remove("hidden");
  setTimeout(() => {
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 100);
}

function escapeHtml(str) {
  const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
  return String(str).replace(/[&<>"']/g, (m) => map[m]);
}

/* ------------------------------------------------------------------
   Form Submit Handler
------------------------------------------------------------------ */
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();

  const payload = collectFormData();
  if (!payload) return;

  setLoading(true);

  try {
    const headers = { "Content-Type": "application/json" };
    const storedKey = getStoredApiKey();
    if (storedKey) {
      headers["X-Gemini-API-Key"] = storedKey;
    }

    const response = await fetch("/analyse", {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      const errMsg = data.error || `Server error (${response.status}). Please try again.`;
      showError(errMsg);
      return;
    }

    renderResults(data);

  } catch (err) {
    console.error("Fetch error:", err);
    showError("Network connection error. Please make sure the Flask server is running.");
  } finally {
    setLoading(false);
  }
});

/* ------------------------------------------------------------------
   Live input listeners
------------------------------------------------------------------ */
form.querySelectorAll("input, select").forEach((el) => {
  el.addEventListener("input", () => {
    clearError();
  });
});

// Initialise API status on page load
document.addEventListener("DOMContentLoaded", () => {
  syncApiKeyStatus();
});
