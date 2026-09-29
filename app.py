"""
Personal Finance Advisor Bot — Flask Backend
Uses Google Gemini 2.0 Flash to deliver personalised budget plans,
spending analysis, and saving suggestions. Includes a high-precision
Smart Advisory Engine fallback to guarantee seamless prototype demo functionality.
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

PLACEHOLDER_KEYS = {
    "your_gemini_api_key_here",
    "YOUR_GEMINI_API_KEY_HERE",
    "your_api_key_here",
    "YOUR_API_KEY_HERE",
    "",
}

def get_active_api_key(client_key=None):
    """Resolve API key from client request, GEMINI_API_KEY, or GOOGLE_API_KEY."""
    if client_key and isinstance(client_key, str) and client_key.strip() not in PLACEHOLDER_KEYS:
        return client_key.strip()
    
    env_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
    env_key = env_key.strip()
    if env_key and env_key not in PLACEHOLDER_KEYS:
        return env_key
    return None

# ---------------------------------------------------------------------------
# Category & Goal Metadata
# ---------------------------------------------------------------------------
CATEGORY_TIPS = {
    "rent": {
        "max_pct": 30,
        "label": "Rent / Housing",
        "icon": "fa-home",
        "over_tip": "Housing exceeds 30% of income; consider subletting, negotiating rent, or reducing utility bills.",
        "under_tip": "Great job keeping housing costs low! Direct the surplus directly into investments.",
        "ok_tip": "Housing expenses are well balanced within the 30% threshold."
    },
    "food": {
        "max_pct": 15,
        "label": "Groceries & Food",
        "icon": "fa-shopping-basket",
        "over_tip": "Grocery spending is high; plan weekly meals, buy staple grains in bulk, and minimize food wastage.",
        "under_tip": "Food budget is lean; ensure nutritional balance isn't being compromised.",
        "ok_tip": "Food spending aligns well with the recommended 15% allocation."
    },
    "transport": {
        "max_pct": 10,
        "label": "Transport",
        "icon": "fa-car",
        "over_tip": "Commute costs are high; explore public transit passes, carpooling, or hybrid commute options.",
        "under_tip": "Transport spending is highly economical.",
        "ok_tip": "Commute and transit expenses are in a healthy range."
    },
    "dining": {
        "max_pct": 8,
        "label": "Dining Out",
        "icon": "fa-utensils",
        "over_tip": "Dining out exceeds 8%; limit takeout orders to once a week to recover substantial monthly cash flow.",
        "under_tip": "Disciplined dining habits! You're saving significant discretionary cash.",
        "ok_tip": "Dining out is well controlled and within safe discretionary limits."
    },
    "entertainment": {
        "max_pct": 8,
        "label": "Entertainment",
        "icon": "fa-film",
        "over_tip": "Entertainment spend is above 8%; audit OTT streaming and gaming subscriptions and share family plans.",
        "under_tip": "Minimal entertainment drain; keeping leisure costs low.",
        "ok_tip": "Recreational spending is modest and sustainable."
    },
    "utilities": {
        "max_pct": 8,
        "label": "Utilities",
        "icon": "fa-bolt",
        "over_tip": "Utility bills are elevated; switch to LED lights, unplug idle electronics, and review mobile/broadband plans.",
        "under_tip": "Utility usage is energy-efficient and low-cost.",
        "ok_tip": "Utilities are well within optimal spending parameters."
    },
    "savings": {
        "max_pct": 20,
        "label": "Savings",
        "icon": "fa-piggy-bank",
        "over_tip": "Superb savings rate! Consider diversifying into index mutual funds or PPF.",
        "under_tip": "Savings rate is below the 20% golden benchmark; automate transfers on salary day.",
        "ok_tip": "Savings meet the 20% benchmark; maintain automated monthly transfers."
    },
    "health": {
        "max_pct": 5,
        "label": "Health & Medical",
        "icon": "fa-heartbeat",
        "over_tip": "Medical expenses are high; check health insurance claims or corporate group coverages.",
        "under_tip": "Healthcare expenses are low; ensure you have adequate health and term life insurance.",
        "ok_tip": "Health spending is manageable and within healthy bounds."
    },
    "education": {
        "max_pct": 10,
        "label": "Education",
        "icon": "fa-graduation-cap",
        "over_tip": "High education costs; seek scholarships, employer reimbursement, or tax-deductible education loans.",
        "under_tip": "Low education spending; consider setting aside funds for continuous upskilling.",
        "ok_tip": "Education spending is an investment with strong long-term payoff."
    },
    "shopping": {
        "max_pct": 8,
        "label": "Shopping",
        "icon": "fa-bag-shopping",
        "over_tip": "Shopping exceeds 8%; introduce a strict 48-hour cooling-off rule before non-essential purchases.",
        "under_tip": "Excellent shopping restraint; avoiding retail impulse buying.",
        "ok_tip": "Shopping spending is disciplined and reasonable."
    },
    "other": {
        "max_pct": 10,
        "label": "Miscellaneous",
        "icon": "fa-ellipsis-h",
        "over_tip": "Miscellaneous expenses are leaking cash; maintain a digital expense tracker to plug unidentified leaks.",
        "under_tip": "Low miscellaneous leakage.",
        "ok_tip": "Incidental expenses are properly controlled."
    },
}

GOAL_DESCRIPTIONS = {
    "emergency_fund": "build a 6-month emergency fund covering essential expenses",
    "vacation":        "save for a dream vacation within the next 12 months",
    "gadget":          "save for a major gadget purchase (e.g., laptop, smartphone) within 3-6 months",
    "investment":      "begin a disciplined investment portfolio (mutual funds / SIPs)",
    "debt_repayment":  "aggressively pay down existing debts or credit-card balances",
    "home_purchase":   "accumulate a down payment for a home within 2-5 years",
    "retirement":      "maximise long-term retirement corpus through consistent compounding",
    "education":       "save for higher education or professional certifications",
}

# ---------------------------------------------------------------------------
# Prompt Builder & Gemini Calling
# ---------------------------------------------------------------------------
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
    """Robustly extract a JSON object from raw text response."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    cleaned = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError("Could not extract valid JSON from model response.")


# ---------------------------------------------------------------------------
# Smart Advisory Fallback Engine
# Provides immediate, high-accuracy financial planning when Gemini API key
# is missing, invalid, or during offline prototype demonstrations.
# ---------------------------------------------------------------------------
def generate_smart_fallback(income, expenses, goal):
    """
    Generate an expert financial analysis using algorithmic rules matching
    standard financial planning frameworks (50/30/20 rule, Indian household benchmarks).
    """
    total_expenses = sum(expenses.values())
    disposable = income - total_expenses
    savings_rec = int(round(income * 0.20))
    
    budget = []
    analysis = []
    
    for cat, amt in expenses.items():
        meta = CATEGORY_TIPS.get(cat, {
            "max_pct": 10,
            "label": cat.title(),
            "over_tip": "Review and trim spending in this category.",
            "under_tip": "Good expense control here.",
            "ok_tip": "Spending is balanced."
        })
        
        max_pct = meta["max_pct"]
        label = meta["label"]
        recommended = int(round(income * (max_pct / 100)))
        actual = int(round(amt))
        pct_used = int(round((actual / income) * 100)) if income > 0 else 0
        
        if cat == "savings":
            if actual >= recommended:
                status = "ok"
                tip = meta.get("ok_tip", "Great savings discipline!")
            elif actual > 0:
                status = "under"
                tip = f"Current savings (Rs.{actual:,}) are below recommended 20% (Rs.{recommended:,}). Aim to bridge Rs.{recommended - actual:,}."
            else:
                status = "under"
                tip = f"Allocate at least Rs.{recommended:,} (20% of income) towards automated monthly savings."
        else:
            if actual > recommended * 1.05:
                status = "over"
                diff = actual - recommended
                tip = f"{label} is over recommended budget by Rs.{diff:,}. {meta.get('over_tip', '')}"
            elif actual < recommended * 0.80 and actual > 0:
                status = "under"
                diff = recommended - actual
                tip = f"{label} is Rs.{diff:,} below max threshold. {meta.get('under_tip', '')}"
            else:
                status = "ok"
                tip = meta.get("ok_tip", f"{label} is aligned with financial targets.")
                
        budget.append({
            "category": label,
            "recommended": recommended,
            "actual": actual,
            "percentage": max_pct,
            "status": status,
            "tip": tip
        })
        
        # Spending insight
        if status == "over":
            insight = f"{label} consumes {pct_used}% of monthly income, exceeding the {max_pct}% threshold by Rs.{actual - recommended:,}."
        elif status == "under":
            insight = f"{label} utilizes only {pct_used}% of income, leaving a surplus of Rs.{recommended - actual:,}."
        else:
            insight = f"{label} is well-controlled at {pct_used}% of your monthly take-home income."
            
        analysis.append({
            "category": label,
            "actual": actual,
            "recommended": recommended,
            "percentage_used": pct_used,
            "status": status,
            "insight": insight
        })
        
    # Generate 4-6 targeted, actionable suggestions with Rupee amounts
    suggestions = []
    
    # 1. Dining/Food optimization if present
    if expenses.get("dining", 0) > (income * 0.08):
        trim_dining = int(round(expenses["dining"] * 0.35))
        suggestions.append(f"Trim dining out and food delivery by 35% to redirect Rs.{trim_dining:,} monthly towards your core financial goal.")
    elif expenses.get("dining", 0) > 0:
        suggestions.append(f"Cap weekend social dining at Rs.{int(expenses['dining'] * 0.8):,} to free up Rs.{int(expenses['dining'] * 0.2):,} each month.")

    # 2. Shopping/Entertainment trim if present
    if expenses.get("shopping", 0) > (income * 0.08):
        trim_shop = int(round(expenses["shopping"] * 0.30))
        suggestions.append(f"Apply a 48-hour cooling-off rule on e-commerce shopping to save approximately Rs.{trim_shop:,} per month.")
        
    if expenses.get("entertainment", 0) > (income * 0.08):
        trim_ent = int(round(expenses["entertainment"] * 0.25))
        suggestions.append(f"Consolidate multiple streaming and subscription services to save around Rs.{trim_ent:,} monthly.")
        
    # 3. Utilities / Commute optimization
    if expenses.get("transport", 0) > (income * 0.10):
        trim_transport = int(round(expenses["transport"] * 0.20))
        suggestions.append(f"Switch 2 commute days per week to public transit or carpooling to save Rs.{trim_transport:,} every month.")
    else:
        suggestions.append("Perform a quarterly audit of utility tariffs and internet plans to conserve Rs.500 to Rs.1,500 monthly.")

    # 4. Goal-specific calculated suggestion
    goal_monthly_alloc = max(int(round(disposable * 0.5)), savings_rec)
    if goal == "emergency_fund":
        target_fund = int(round(total_expenses * 6))
        months = max(1, round(target_fund / max(goal_monthly_alloc, 1000)))
        suggestions.append(f"Direct Rs.{goal_monthly_alloc:,} monthly into a liquid mutual fund or auto-sweep fixed deposit to reach your 6-month safety net of Rs.{target_fund:,} in ~{months} months.")
    elif goal == "investment":
        suggestions.append(f"Automate a diversified SIP of Rs.{goal_monthly_alloc:,} in Nifty 50 and mid-cap index mutual funds on the 1st of every month.")
    elif goal == "debt_repayment":
        suggestions.append(f"Employ the debt avalanche strategy: allocate Rs.{goal_monthly_alloc:,} monthly towards paying down your highest-interest credit balance.")
    elif goal == "vacation":
        suggestions.append(f"Set up a dedicated recurring deposit (RD) of Rs.{goal_monthly_alloc:,} monthly to fund your vacation debt-free.")
    elif goal == "gadget":
        suggestions.append(f"Park Rs.{goal_monthly_alloc:,} monthly into a separate short-term savings account until you meet your purchase price without credit card EMIs.")
    elif goal == "home_purchase":
        suggestions.append(f"Channel Rs.{goal_monthly_alloc:,} monthly into low-volatility hybrid funds and PPF to build your property down-payment corpus.")
    elif goal == "retirement":
        suggestions.append(f"Maximize long-term compounding by allocating Rs.{goal_monthly_alloc:,} monthly across EPF/PPF and broad-market equity funds.")
    else:
        suggestions.append(f"Allocate Rs.{goal_monthly_alloc:,} monthly into a dedicated goal-tracker fund to stay financially resilient.")

    # 5. Golden savings benchmark rule
    suggestions.append(f"Target saving at least 20% of your net income (Rs.{savings_rec:,}) immediately when your salary is credited, before incurring variable expenses.")

    # Ensure 4-6 suggestions
    suggestions = suggestions[:6]

    # Summary
    expense_pct = int(round((total_expenses / income) * 100)) if income > 0 else 0
    if disposable >= 0:
        health_status = f"Your total expenses are Rs.{total_expenses:,} ({expense_pct}% of income), generating a healthy disposable surplus of Rs.{disposable:,}."
    else:
        health_status = f"Your total expenses of Rs.{total_expenses:,} exceed your income by Rs.{abs(disposable):,} ({expense_pct}% burn rate), requiring immediate spending rationalisation."
        
    summary = f"{health_status} Following the recommended allocations will keep you disciplined on your journey to {GOAL_DESCRIPTIONS.get(goal, 'financial independence')}."

    return {
        "budget": budget,
        "analysis": analysis,
        "suggestions": suggestions,
        "summary": summary,
        "source": "smart_engine"
    }


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
    has_api_key = bool(get_active_api_key())
    return render_template("index.html", categories=categories, goals=goals, has_api_key=has_api_key)


@app.route("/analyse", methods=["POST"])
def analyse():
    """
    POST /analyse
    Body: { "income": float, "expenses": { category: amount }, "goal": str, "api_key": optional str }
    Returns: { success, budget, analysis, suggestions, summary, source }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON body."}), 400

    valid, err = validate_input(data)
    if not valid:
        return jsonify({"success": False, "error": err}), 400

    income = data["income"]
    expenses = data["expenses"]
    goal = data.get("goal", "emergency_fund")
    client_key = data.get("api_key") or request.headers.get("X-Gemini-API-Key")

    active_key = get_active_api_key(client_key)

    # 1. If an active key is present, attempt live Gemini AI generation
    if active_key:
        try:
            logger.info("Configuring Gemini with active API key (length=%d)", len(active_key))
            genai.configure(api_key=active_key)
            
            generation_config = genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2048,
            )
            
            # Try gemini-2.0-flash first, fallback to gemini-1.5-flash
            for model_name in ["gemini-2.0-flash", "gemini-1.5-flash"]:
                try:
                    gemini_model = genai.GenerativeModel(
                        model_name=model_name,
                        generation_config=generation_config,
                    )
                    prompt = build_prompt(income, expenses, goal)
                    logger.info("Querying Gemini (%s)...", model_name)
                    response = gemini_model.generate_content(prompt)
                    raw_text = response.text
                    result = extract_json(raw_text)
                    
                    required_keys = {"budget", "analysis", "suggestions", "summary"}
                    if required_keys.issubset(result.keys()):
                        logger.info("Successfully received and parsed Gemini response from %s", model_name)
                        return jsonify({
                            "success":     True,
                            "budget":      result["budget"],
                            "analysis":    result["analysis"],
                            "suggestions": result["suggestions"],
                            "summary":     result["summary"],
                            "source":      "gemini",
                            "model":       model_name
                        })
                except Exception as inner_exc:
                    logger.warning("Model %s attempt failed: %s", model_name, inner_exc)
                    continue

        except Exception as exc:
            logger.warning("Gemini invocation error: %s. Using Smart Fallback.", exc)

    # 2. Smart Advisory Fallback Engine (guarantees flawless prototype execution)
    logger.info("Using Smart Advisory Engine for analysis (income=Rs.%s, goal=%s)", income, goal)
    fallback_data = generate_smart_fallback(income, expenses, goal)
    
    return jsonify({
        "success":     True,
        "budget":      fallback_data["budget"],
        "analysis":    fallback_data["analysis"],
        "suggestions": fallback_data["suggestions"],
        "summary":     fallback_data["summary"],
        "source":      "smart_engine",
        "has_api_key": bool(active_key),
        "note":        "Generated by Smart Advisory Engine. To use live Gemini 2.0 AI, set GEMINI_API_KEY in .env or via the API Key button." if not active_key else "Live AI fallback activated."
    })


@app.route("/api/key-status", methods=["GET", "POST"])
def key_status():
    """Check or update the Gemini API key status."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        new_key = data.get("api_key", "").strip()
        if new_key and new_key not in PLACEHOLDER_KEYS:
            # Update running environment variable
            os.environ["GEMINI_API_KEY"] = new_key
            os.environ["GOOGLE_API_KEY"] = new_key
            # Save to .env file for persistence
            try:
                env_path = os.path.join(os.path.dirname(__file__), ".env")
                with open(env_path, "w", encoding="utf-8") as f:
                    f.write(f"GEMINI_API_KEY={new_key}\nGOOGLE_API_KEY={new_key}\n")
                return jsonify({"success": True, "message": "API Key saved successfully! Live Gemini AI is now active."})
            except Exception as e:
                return jsonify({"success": True, "message": f"API Key active in session (could not write to .env: {e})"})
        else:
            return jsonify({"success": False, "error": "Invalid API key format."}), 400

    active_key = get_active_api_key()
    return jsonify({
        "configured": bool(active_key),
        "mode": "gemini" if active_key else "smart_engine"
    })


@app.route("/health")
def health():
    """Simple health-check endpoint."""
    active_key = get_active_api_key()
    return jsonify({
        "status": "ok",
        "mode": "gemini" if active_key else "smart_engine",
        "api_key_configured": bool(active_key)
    })


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
