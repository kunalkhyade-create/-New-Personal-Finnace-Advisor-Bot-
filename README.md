# 💰 FinanceBot — AI Personal Finance Advisor

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=flat-square&logo=flask&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-4285F4?style=flat-square&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

An AI-powered personal finance advisor built with **Flask** and **Google Gemini 2.0 Flash**. Enter your monthly income and expenses, set a financial goal, and receive a personalised budget plan, spending analysis, and saving suggestions — instantly.

> 🤖 **No API key? No problem.** The built-in **Smart Advisory Engine** works fully offline using the 50/30/20 rule and Indian household benchmarks — zero configuration required.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **AI Budget Generator** | Personalised monthly budget via Gemini 2.0 Flash or Smart Fallback Engine |
| 📊 **Spending Analyser** | Category-by-category analysis with visual status badges (Over / On-Track / Under) |
| 💡 **Saving Suggestions** | 4–6 specific, rupee-quantified saving recommendations tailored to your goal |
| 📝 **Financial Summary** | Two-sentence AI-written overall financial health overview |
| 🔑 **In-App API Key Manager** | Set or update your Gemini API key live without restarting the server |
| 🌍 **Public Deployment** | One-command Ngrok tunnel for sharing the app with anyone |
| 🔒 **Secure & Validated** | All inputs validated server-side; API key never committed to version control |

---

## 🗂️ Project Structure

```
personal-finance-advisor-bot/
├── app.py                  # Flask backend + Gemini AI integration + Smart Fallback Engine
├── run_public.py           # Ngrok public deployment launcher
├── requirements.txt        # Python dependencies
├── .env.example            # Template for environment variables
├── .env                    # Your local secrets (NOT committed to git)
├── .gitignore
├── templates/
│   └── index.html          # Single-page UI (Inter font + Font Awesome icons)
└── static/
    ├── css/
    │   └── style.css       # Dark glassmorphism design system
    └── js/
        └── main.js         # Async form handling + dynamic result rendering
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/personal-finance-advisor-bot.git
cd personal-finance-advisor-bot
```

### 2. Create & activate a virtual environment

```powershell
# Windows
python -m venv myenv
myenv\Scripts\activate
```

```bash
# macOS / Linux
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and add your Gemini API key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_flask_secret_key_here
```

> 🔑 **Get your free Gemini API key** → [https://aistudio.google.com](https://aistudio.google.com) → **Get API Key** → **Create API Key**
>
> ℹ️ **No API key?** The app still works fully using the built-in **Smart Advisory Engine**.

### 5. Run locally

```bash
python app.py
```

Open your browser at: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🖥️ How to Use

### Step 1 — Enter your Monthly Income
Type your net monthly take-home income in Indian Rupees (₹).

### Step 2 — Log your Expenses
Fill in amounts for any applicable expense categories:

| Category | Recommended Budget (% of income) |
|---|---|
| 🏠 Rent / Housing | ≤ 30% |
| 🛒 Groceries & Food | ≤ 15% |
| 🚗 Transport | ≤ 10% |
| 🍽️ Dining Out | ≤ 8% |
| 🎬 Entertainment | ≤ 8% |
| ⚡ Utilities | ≤ 8% |
| 🛍️ Shopping | ≤ 8% |
| 💊 Health & Medical | ≤ 5% |
| 🎓 Education | ≤ 10% |
| 🐷 Savings | ≥ 20% |
| 📦 Miscellaneous | ≤ 10% |

### Step 3 — Choose a Financial Goal

| Goal | Description |
|---|---|
| 🛡️ `emergency_fund` | Build a 6-month safety net covering essential expenses |
| ✈️ `vacation` | Save for a dream trip within 12 months |
| 💻 `gadget` | Save for a major tech purchase (laptop, smartphone) |
| 📈 `investment` | Start a disciplined SIP / mutual fund portfolio |
| 💳 `debt_repayment` | Pay down debts using the avalanche strategy |
| 🏡 `home_purchase` | Build a property down-payment corpus |
| 🌅 `retirement` | Maximise long-term compounding via EPF/PPF + equity |
| 🎓 `education` | Save for higher education or certifications |

### Step 4 — Analyse
Click **Analyse My Finances** and receive:
- ✅ **Budget Plan** — recommended vs actual spending per category with tips
- 📊 **Spending Analysis** — status badges and one-sentence insights per category
- 💡 **Saving Suggestions** — 4–6 actionable tips with specific ₹ amounts
- 📝 **Financial Summary** — overall financial health in two sentences

---

## 🤖 AI Modes

### 🟢 Gemini Mode (Live AI)
When a valid `GEMINI_API_KEY` is configured, the app queries **Google Gemini 2.0 Flash** (with automatic fallback to Gemini 1.5 Flash) for a personalised, context-aware financial analysis.

### 🔵 Smart Advisory Engine (Offline Fallback)
When no API key is present or the Gemini API is unreachable, the app automatically switches to the built-in **Smart Advisory Engine** — an algorithmic financial planner based on:
- The **50/30/20 rule**
- Indian household spending benchmarks
- Goal-specific allocation strategies (SIP, avalanche debt, RD, etc.)

### Switching Modes at Runtime
Click the ⚡ **AI Status** button in the top-right of the app to enter your Gemini API key. The key is saved to `.env` for persistence across restarts.

---

## 🌍 Public Deployment (Ngrok)

Share your locally running app with anyone on the internet using a free Ngrok tunnel.

### 1. Sign up at [ngrok.com](https://ngrok.com) and copy your authtoken

### 2. Edit `run_public.py` and paste your authtoken

```python
TOKEN = "YOUR_NGROK_AUTHTOKEN_HERE"
```

### 3. Run the public launcher

```bash
python run_public.py
```

Output:

```
============================================================
  YOUR PUBLIC WEBSITE URL IS LIVE!
  URL: https://xxxx-xx-xx-xxx-xx.ngrok-free.app
============================================================
  Share this URL with anyone to access your Finance Bot.
  Press Ctrl+C to stop.
```

> ⚠️ Free Ngrok URLs change on every restart. Upgrade to a paid plan for a fixed custom domain.

---

## 📡 API Reference

### `GET /`
Renders the main single-page UI.

---

### `POST /analyse`
Analyses financial data and returns a full budget plan.

**Request Body (JSON):**
```json
{
  "income": 75000,
  "expenses": {
    "rent": 20000,
    "food": 8000,
    "transport": 3000,
    "dining": 4000,
    "entertainment": 2000,
    "utilities": 2500,
    "savings": 10000
  },
  "goal": "emergency_fund",
  "api_key": "optional_override_key"
}
```

**Response (JSON):**
```json
{
  "success": true,
  "source": "gemini",
  "budget": [
    {
      "category": "Rent / Housing",
      "recommended": 22500,
      "actual": 20000,
      "percentage": 30,
      "status": "ok",
      "tip": "Housing expenses are well balanced within the 30% threshold."
    }
  ],
  "analysis": [
    {
      "category": "Rent / Housing",
      "actual": 20000,
      "recommended": 22500,
      "percentage_used": 27,
      "status": "ok",
      "insight": "Rent is well-controlled at 27% of your monthly take-home income."
    }
  ],
  "suggestions": [
    "Automate a SIP of ₹12,500 in Nifty 50 index funds on the 1st of every month."
  ],
  "summary": "Your total expenses are ₹49,500 (66% of income), generating a healthy surplus. Stay consistent with your goal to build your emergency fund."
}
```

---

### `GET /api/key-status`
Returns the current AI mode.

**Response:**
```json
{
  "configured": true,
  "mode": "gemini"
}
```

---

### `POST /api/key-status`
Sets a new Gemini API key at runtime (saves to `.env`).

**Request Body:**
```json
{ "api_key": "AIza..." }
```

---

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "mode": "smart_engine",
  "api_key_configured": false
}
```

---

## 🏗️ Architecture

```
Browser  (HTML / CSS / JS — Glassmorphism UI, Inter font, Font Awesome)
        │  POST /analyse  →  { income, expenses, goal }
        ▼
Flask Backend (app.py)
  ├── validate_input()           ← Sanitise & bound-check all inputs
  ├── get_active_api_key()       ← Resolve key: request → env → .env
  │
  ├── [API key present]
  │     ├── build_prompt()       ← Structured financial prompt builder
  │     ├── gemini-2.0-flash     ← Primary model
  │     │     └── gemini-1.5-flash  ← Auto-fallback
  │     └── extract_json()       ← Robust JSON parser with markdown stripping
  │
  └── [No API key / error]
        └── generate_smart_fallback()   ← 50/30/20 algorithmic engine
                                            (No internet required)
        │
        │  JSON: { budget, analysis, suggestions, summary, source }
        ▼
Frontend  renders:
  ├── Budget cards    (recommended vs actual + status badge + tip)
  ├── Analysis cards  (insight sentence + % bar)
  ├── Suggestions     (bulleted list with ₹ amounts)
  └── Summary         (overall health statement)
```

---

## 🔑 Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | Optional | — | Google Gemini API key for live AI analysis |
| `GOOGLE_API_KEY` | Optional | — | Alias for `GEMINI_API_KEY` |
| `SECRET_KEY` | Optional | `dev-secret-key-change-in-prod` | Flask session secret key |

> Copy `.env.example` to `.env` and fill in your values. The `.env` file is listed in `.gitignore` and will **never** be committed.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `Flask` | 3.0.3 | Web framework & routing |
| `google-generativeai` | 0.8.3 | Gemini AI SDK |
| `python-dotenv` | 1.0.1 | `.env` file loader |
| `pyngrok` | 7.2.0 | Ngrok tunnel for public deployment |

```bash
pip install -r requirements.txt
```

---

## 🔒 Security

- ✅ API keys loaded from `.env` — **never committed** to version control
- ✅ `.env` is listed in `.gitignore`
- ✅ All user input validated server-side before AI call (type checking, category whitelist, value bounds)
- ✅ Income capped at ₹1,00,00,000 — expense per category capped at ₹50,00,000
- ✅ HTML output escaped in JavaScript to prevent XSS
- ✅ Flask `SECRET_KEY` configurable via environment variable

---

## 🛠️ Development Tips

```bash
# Run with hot-reload
set FLASK_DEBUG=1 && python app.py   # Windows
FLASK_DEBUG=1 python app.py          # macOS/Linux

# Health check
curl http://127.0.0.1:5000/health

# Quick test of the analyse endpoint
curl -X POST http://127.0.0.1:5000/analyse \
  -H "Content-Type: application/json" \
  -d '{"income":60000,"expenses":{"rent":18000,"food":7000},"goal":"investment"}'
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT — free to use, modify, and distribute.

---

<div align="center">
Made with ❤️ using Flask + Google Gemini AI
</div>
