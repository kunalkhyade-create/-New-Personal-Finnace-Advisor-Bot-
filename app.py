"""
Personal Finance Advisor Bot — Flask Backend
Uses Google Gemini 2.0 Flash to deliver personalised budget plans,
spending analysis, and saving suggestions.
"""

import os
import re
import json
import logging

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

# ---------------------------------------------------------------------------
# Gemini model setup
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not set. Add it to your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

generation_config = genai.types.GenerationConfig(
    temperature=0.7,
    max_output_tokens=2048,
)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

# ---------------------------------------------------------------------------
# Prompt-engineering helpers
# ---------------------------------------------------------------------------

CATEGORY_TIPS: dict = {
    "rent":          {"max_pct": 30, "label": "Rent / Housing",    "icon": "fa-home"},
    "food":          {"max_pct": 15, "label": "Groceries & Food",  "icon": "fa-shopping-basket"},
    "transport":     {"max_pct": 10, "label": "Transport",         "icon": "fa-car"},
    "dining":        {"max_pct":  8, "label": "Dining Out",        "icon": "fa-utensils"},
    "entertainment": {"max_pct":  8, "label": "Entertainment",     "icon": "fa-film"},
    "utilities":     {"max_pct":  8, "label": "Utilities",         "icon": "fa-bolt"},
    "savings":       {"max_pct": 20, "label": "Savings",           "icon": "fa-piggy-bank"},
    "health":        {"max_pct":  5, "label": "Health & Medical",  "icon": "fa-heartbeat"},
    "education":     {"max_pct": 10, "label": "Education",         "icon": "fa-graduation-cap"},
    "shopping":      {"max_pct":  8, "label": "Shopping",          "icon": "fa-bag-shopping"},
    "other":         {"max_pct": 10, "label": "Miscellaneous",     "icon": "fa-ellipsis-h"},
}

GOAL_DESCRIPTIONS: dict = {
    "emergency_fund": "build a 6-month emergency fund covering all essential expenses",
    "vacation":        "save for a dream vacation within the next 12 months",
    "gadget":          "save for a major gadget purchase (e.g., laptop, smartphone) within 3-6 months",
    "investment":      "begin a disciplined investment portfolio (mutual funds / SIPs)",
    "debt_repayment":  "aggressively pay down existing debts or credit-card balances",
    "home_purchase":   "accumulate a down payment for a home within 2-5 years",
    "retirement":      "maximise long-term retirement corpus through consistent investing",
    "education":       "save for higher education or a professional certification",
}


def build_prompt(income, expenses, goal):
    """Construct a structured financial prompt for the Gemini model."""
    goal_desc = GOAL_DESCRIPTIONS.get(goal, "achieve general financial wellness")

    expense_lines = "\n".join(
        "  - {}: Rs.{:,.0f}".format(
            CATEGORY_TIPS.get(cat, {}).get("label", cat.title()), amt
        )
        for cat, amt in expenses.items()
        if amt > 0
    )

    tips_lines = "\n".join(
        "  - {}: recommended <= {}% of income".format(
            CATEGORY_TIPS.get(cat, {}).get("label", cat.title()),
            CATEGORY_TIPS.get(cat, {}).get("max_pct", 10)
        )
        for cat in expenses
        if cat in CATEGORY_TIPS and expenses[cat] > 0
    )

    total_expenses = sum(expenses.values())
    disposable = income - total_expenses

    prompt = (
        "You are an expert personal finance advisor. Analyse the following financial data "
        "and return STRICTLY valid JSON (no markdown, no extra text).\n\n"
        "## Financial Profile\n"
        "- Monthly Income: Rs.{income:,.0f}\n"
        "- Total Monthly Expenses: Rs.{total:,.0f}\n"
        "- Disposable Income: Rs.{disposable:,.0f}\n"
        "- Primary Financial Goal: {goal}\n\n"
        "## Reported Expenses\n{expense_lines}\n\n"
        "## Recommended Budget Thresholds\n{tips_lines}\n"
        "  - Savings: recommended >= 20% of income (Rs.{savings:,.0f})\n\n"
        "## Instructions\n"
        'Return a single JSON object with EXACTLY these keys:\n'
        '{{\n'
        '  "budget": [\n'
        '    {{\n'
        '      "category": "<category name>",\n'
        '      "recommended": <recommended monthly amount as integer in INR>,\n'
        '      "actual": <actual monthly amount as integer in INR>,\n'
        '      "percentage": <recommended percentage of income as integer>,\n'
        '      "status": "ok" | "over" | "under",\n'
        '      "tip": "<one actionable tip for this category>"\n'
        '    }}\n'
        '  ],\n'
        '  "analysis": [\n'
        '    {{\n'
        '      "category": "<category name>",\n'
        '      "actual": <actual amount as integer>,\n'
        '      "recommended": <recommended amount as integer>,\n'
        '      "percentage_used": <actual/income*100 as integer>,\n'
        '      "status": "ok" | "over" | "under",\n'
        '      "insight": "<one-sentence spending insight>"\n'
        '    }}\n'
        '  ],\n'
        '  "suggestions": [\n'
        '    "<specific, actionable saving suggestion with rupee amounts>"\n'
        '  ],\n'
        '  "summary": "<two-sentence overall financial health summary>"\n'
        '}}\n\n'
        "Rules:\n"
        "- suggestions must contain 4-6 items, each mentioning a specific rupee amount.\n"
        "- All monetary values must be integers (no decimals).\n"
        "- status is 'over' when actual > recommended, 'under' when actual < recommended by > 10%, else 'ok'.\n"
        "- Do NOT wrap the JSON in markdown code fences."
    ).format(
        income=income,
        total=total_expenses,
        disposable=disposable,
        goal=goal_desc,
        expense_lines=expense_lines,
        tips_lines=tips_lines,
        savings=income * 0.20,
    )

    return prompt.strip()


def extract_json(raw):
    """
    Robustly extract a JSON object from the model's raw text response.
    Strategy 1 - direct parse.
    Strategy 2 - strip markdown code fences.
    Strategy 3 - regex to find the outermost { } block.
    """
    # Strategy 1
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Strategy 2
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Strategy 3
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError("Could not extract valid JSON from model response.")


# ---------------------------------------------------------------------------
# Input validation helpers
# ---------------------------------------------------------------------------

MAX_INCOME = 10_000_000
MAX_EXPENSE = 5_000_000

VALID_CATEGORIES = set(CATEGORY_TIPS.keys())
VALID_GOALS = set(GOAL_DESCRIPTIONS.keys())


def validate_input(data):
    income = data.get("income")
    expenses = data.get("expenses", {})
    goal = data.get("goal", "emergency_fund")

    if not isinstance(income, (int, float)) or income <= 0:
        return False, "Please provide a valid positive monthly income."
    if income > MAX_INCOME:
        return False, "Income value seems unusually high. Please double-check."

    if not expenses or not isinstance(expenses, dict):
        return False, "Please log at least one expense category."

    valid_expenses = {
        k: float(v)
        for k, v in expenses.items()
        if k in VALID_CATEGORIES and isinstance(v, (int, float)) and float(v) >= 0
    }
    if not valid_expenses:
        return False, "No valid expense categories found. Please check your inputs."

    for cat, amt in valid_expenses.items():
        if amt > MAX_EXPENSE:
            return False, "Expense for '{}' seems unusually high. Please verify.".format(cat)

    if goal not in VALID_GOALS:
        data["goal"] = "emergency_fund"

    data["income"] = float(income)
    data["expenses"] = valid_expenses
    return True, ""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Render the main single-page interface."""
    categories = {k: v for k, v in CATEGORY_TIPS.items()}
    goals = {k: v for k, v in GOAL_DESCRIPTIONS.items()}
    return render_template("index.html", categories=categories, goals=goals)


@app.route("/analyse", methods=["POST"])
def analyse():
    """
    POST /analyse
    Body: { "income": float, "expenses": { category: amount }, "goal": str }
    Returns: { success, budget, analysis, suggestions, summary }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON body."}), 400

    valid, err = validate_input(data)
    if not valid:
        return jsonify({"success": False, "error": err}), 400

    income   = data["income"]
    expenses = data["expenses"]
    goal     = data.get("goal", "emergency_fund")

    prompt = build_prompt(income, expenses, goal)
    logger.info("Sending prompt to Gemini (income=Rs.%s, goal=%s)", income, goal)

    try:
        response = model.generate_content(prompt)
        raw_text = response.text
        logger.debug("Raw model response: %s", raw_text[:300])
    except Exception as exc:
        logger.error("Gemini API error: %s", exc)
        return jsonify({"success": False, "error": "AI service error: {}".format(exc)}), 502

    try:
        result = extract_json(raw_text)
    except ValueError as exc:
        logger.error("JSON extraction failed: %s", exc)
        return jsonify({"success": False, "error": "Could not parse AI response. Please try again."}), 500

    required_keys = {"budget", "analysis", "suggestions", "summary"}
    missing = required_keys - result.keys()
    if missing:
        return jsonify({
            "success": False,
            "error": "AI response missing fields: {}. Please retry.".format(", ".join(missing)),
        }), 500

    return jsonify({
        "success":     True,
        "budget":      result["budget"],
        "analysis":    result["analysis"],
        "suggestions": result["suggestions"],
        "summary":     result["summary"],
    })


@app.route("/health")
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok", "model": "gemini-2.0-flash"})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
