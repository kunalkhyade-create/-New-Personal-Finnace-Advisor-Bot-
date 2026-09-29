/**
 * main.js — Personal Finance Advisor Bot
 * Handles form submission, async fetch to /analyse, and dynamic result rendering.
 */

"use strict";

/* ------------------------------------------------------------------
   DOM References
------------------------------------------------------------------ */
const form            = document.getElementById("finance-form");
const submitBtn       = document.getElementById("submit-btn");
const btnText         = document.getElementById("btn-text");
const btnLoader       = document.getElementById("btn-loader");
const errorBanner     = document.getElementById("error-banner");
const resultsSection  = document.getElementById("results-section");
const summaryText     = document.getElementById("summary-text");
const budgetContainer = document.getElementById("budget-container");
const analysisContainer = document.getElementById("analysis-container");
const suggestionsContainer = document.getElementById("suggestions-container");

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
   Helpers
------------------------------------------------------------------ */

/**
 * Format a number as an Indian-locale rupee string.
 * @param {number} amount
 * @returns {string}
 */
function formatRupee(amount) {
  if (typeof amount !== "number" || isNaN(amount)) return "₹0";
  return "₹" + Math.round(amount).toLocaleString("en-IN");
}

/**
 * Derive icon class from category name.
 * @param {string} category
 * @returns {string}
 */
function iconFor(category) {
  const key = category.toLowerCase().replace(/[^a-z]/g, "");
  // Try exact match first, then partial match
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
 * Show or hide the loading state on the submit button.
 * @param {boolean} loading
 */
function setLoading(loading) {
  submitBtn.disabled = loading;
  btnText.classList.toggle("hidden", loading);
  btnLoader.classList.toggle("hidden", !loading);
}

/**
 * Display an error message in the error banner.
 * @param {string} message
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

/**
 * Read all form values and return a structured payload.
 * @returns {{ income: number, expenses: Object, goal: string } | null}
 */
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

  return { income, expenses, goal };
}

/* ------------------------------------------------------------------
   Render Functions
------------------------------------------------------------------ */

/**
 * Render the personalised budget section.
 * @param {Array} budget
 */
function renderBudget(budget) {
  budgetContainer.innerHTML = "";

  if (!budget || budget.length === 0) {
    budgetContainer.innerHTML = '<p style="color:var(--clr-text-dim);font-size:0.85rem;">No budget data available.</p>';
    return;
  }

  budget.forEach((item) => {
    const status     = (item.status || "ok").toLowerCase();
    const actual     = item.actual     || 0;
    const recommended = item.recommended || 0;
    const pct        = item.percentage  || 0;

    // Progress: how much of the recommended allocation is being used
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

    // Animate progress bar after a tick
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

/**
 * Render the spending analysis chips.
 * @param {Array} analysis
 */
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

/**
 * Render the saving suggestions list.
 * @param {string[]} suggestions
 */
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

/**
 * Render all results into the DOM and reveal the results section.
 * @param {{ budget, analysis, suggestions, summary }} data
 */
function renderResults(data) {
  // Summary
  if (data.summary) {
    summaryText.textContent = data.summary;
  }

  renderBudget(data.budget);
  renderAnalysis(data.analysis);
  renderSuggestions(data.suggestions);

  // Reveal & scroll
  resultsSection.classList.remove("hidden");
  setTimeout(() => {
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 100);
}

/* ------------------------------------------------------------------
   Security helper
------------------------------------------------------------------ */

/**
 * Escape HTML special characters to prevent XSS.
 * @param {string} str
 * @returns {string}
 */
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
    const response = await fetch("/analyse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
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
    showError("Network error. Please check your connection and try again.");
  } finally {
    setLoading(false);
  }
});

/* ------------------------------------------------------------------
   Auto-hide results section on new form interaction
------------------------------------------------------------------ */
form.querySelectorAll("input, select").forEach((el) => {
  el.addEventListener("input", () => {
    // Optionally hide results when the user starts editing again
    // resultsSection.classList.add("hidden");
    clearError();
  });
});
