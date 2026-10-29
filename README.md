# 💰 FinanceBot — AI Personal Finance Advisor

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=flat-square&logo=flask&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-4285F4?style=flat-square&logo=google&logoColor=white)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen?style=flat-square&logo=github)](https://kunalkhyade-create.github.io/-New-Personal-Finnace-Advisor-Bot-/)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
[![Final Report](https://img.shields.io/badge/Report-View%20Here-blueviolet?style=flat-square)](./REPORT.md)

> 🚀 **Live Demo**: [https://kunalkhyade-create.github.io/-New-Personal-Finnace-Advisor-Bot-/](https://kunalkhyade-create.github.io/-New-Personal-Finnace-Advisor-Bot-/)

> An AI-powered personal finance advisor built with **Flask** and **Google Gemini 2.0 Flash**.
> Enter your monthly income and expenses, choose a financial goal, and receive a personalised budget plan,
> category-level spending analysis, and rupee-quantified saving suggestions — instantly, in your browser.

> 🤖 **No API key? No problem.** The built-in **Smart Advisory Engine** works fully offline using the
> 50/30/20 rule and Indian household spending benchmarks — zero configuration required.

---

## 📑 Table of Contents

- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Architecture Overview](#-architecture-overview)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Environment Variables](#-environment-variables)
- [How to Use](#-how-to-use)
- [AI Modes](#-ai-modes)
- [Public Deployment (Ngrok)](#-public-deployment-ngrok)
- [API Overview](#-api-overview)
- [Screenshots](#-screenshots)
- [Dependencies](#-dependencies)
- [Security](#-security)
- [Testing](#-testing)
- [Future Scope](#-future-scope)
- [Contributing](#-contributing)
- [Author and License](#-author-and-license)

---

## 🎯 Problem Statement

Managing personal finances is a challenge for many individuals, especially young professionals and students
in India. There is a lack of accessible, low-barrier tools that can provide **personalised**, **actionable**
financial advice without requiring users to pay for a financial consultant or navigate complex spreadsheets.
Most people overspend in certain categories without realising it until month-end, and rarely have a
structured savings plan tied to a concrete financial goal.

**FinanceBot** solves this by providing AI-driven financial analysis in seconds — directly in a browser,
with no login, no subscription, and no cost.

---

## 🏆 Objectives

- Provide **instant, personalised budget plans** based on user-submitted income and expense data.
- Deliver **category-level spending analysis** with clear Over / On-Track / Under status indicators.
- Generate **4–6 rupee-quantified saving suggestions** tailored to the user's chosen financial goal.
- Operate **fully offline** via a built-in Smart Advisory Engine when no API key is available.
- Enable **live AI analysis** via Google Gemini 2.0 Flash when an API key is configured.
- Allow **public sharing** of the app with a single command via an Ngrok tunnel.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **AI Budget Generator** | Personalised monthly budget via Gemini 2.0 Flash or built-in Smart Fallback Engine |
| 📊 **Spending Analyser** | Category-by-category analysis with visual status badges (Over / OK / Under) |
| 💡 **Saving Suggestions** | 4–6 specific, rupee-quantified saving recommendations tailored to your goal |
| 📝 **Financial Summary** | Two-sentence overall financial health overview |
| 🔑 **In-App API Key Manager** | Set or clear your Gemini API key at runtime without restarting the server |
| 🌍 **Public Deployment** | One-command Ngrok tunnel for sharing the running app with anyone |
| 🔒 **Input Validation** | All inputs sanitised and bound-checked server-side before any AI call |
| ⚡ **Dual-Engine Design** | Graceful automatic fallback — never crashes, always returns a result |

---

## 🛠️ Technology Stack

| Layer | Technology | Version |
|---|---|---|
| **Backend** | Python + Flask | Flask 3.0.3 |
| **AI / LLM** | Google Gemini 2.0 Flash (primary), Gemini 1.5 Flash (auto-fallback) | google-generativeai 0.8.3 |
| **Fallback Engine** | Custom algorithmic engine (50/30/20 rule + Indian benchmarks) | Built-in |
| **Frontend** | HTML5, Vanilla CSS (glassmorphism), Vanilla JavaScript (ES2022+) | — |
| **Typography** | Inter (Google Fonts) | CDN |
| **Icons** | Font Awesome 6.5 | CDN |
| **Environment** | python-dotenv | 1.0.1 |
| **Public Tunnel** | pyngrok (Ngrok wrapper) | 7.2.0 |
| **Database** | None — stateless, processed per-request | — |

---

## 🏗️ Architecture Overview

The application follows a stateless **Single-Page Application (SPA)** pattern:

```
Browser (HTML / CSS / JS)
  │  POST /analyse  →  { income, expenses, goal, api_key? }
  ▼
Flask Backend (app.py)
  ├── validate_input()           ← Sanitise and bound-check all inputs
  ├── get_active_api_key()       ← Resolve key: request body → env → .env file
  │
  ├── [API key present]
  │     ├── build_prompt()       ← Structured financial prompt builder
  │     ├── gemini-2.0-flash     ← Primary Gemini model
  │     │     └── gemini-1.5-flash  ← Automatic model fallback
  │     └── extract_json()       ← Robust JSON parser (strips markdown fences)
  │
  └── [No API key / Gemini error]
        └── generate_smart_fallback()   ← Algorithmic 50/30/20 engine (offline)
  │
  │  JSON response: { success, budget, analysis, suggestions, summary, source }
  ▼
Frontend renders:
  ├── Budget cards    (recommended vs actual + animated progress bar + tip)
  ├── Analysis chips  (insight sentence + % of income)
  ├── Suggestions     (ordered list with Rs amounts)
  └── Summary banner  (overall financial health + engine badge)
```

See [docs/architecture.md](./docs/architecture.md) for the full Mermaid diagram and component breakdown.

---

## 🗂️ Project Structure

```
personal-finance-advisor-bot/
├── app.py                   # Flask backend — routes, Gemini AI integration, Smart Engine
├── run_public.py            # Ngrok public deployment launcher
├── requirements.txt         # Python dependencies
├── .env.example             # Safe template for environment variables
├── .env                     # Your local secrets (gitignored — never committed)
├── .gitignore
├── README.md                # This file
├── REPORT.md                # Full project report
├── CONTRIBUTING.md          # Contributor guide
├── templates/
│   └── index.html           # Single-page UI (Jinja2 template)
├── static/
│   ├── css/
│   │   └── style.css        # Dark glassmorphism design system
│   └── js/
│       └── main.js          # Async form handling + dynamic result rendering
└── docs/
    ├── architecture.md      # System architecture and Mermaid diagram
    ├── database.md          # Data models (stateless — no persistent DB)
    ├── API_Documentation.md # Full REST API reference
    └── USER_GUIDE.md        # End-user guide
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10** or higher
- **pip** (comes with Python)
- *(Optional)* A free [Google Gemini API key](https://aistudio.google.com/app/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/kunalkhyade-create/-New-Personal-Finnace-Advisor-Bot-.git
cd -New-Personal-Finnace-Advisor-Bot-
```

### 2. Create and activate a virtual environment

```powershell
# Windows (PowerShell)
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

```powershell
# Windows
copy .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in your values:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=change-this-to-a-random-string-in-production
```

> 🔑 **Get a free key** at <https://aistudio.google.com> → **Get API Key**
>
> ℹ️ The app runs fully without a key using the built-in **Smart Advisory Engine**.

### 5. Run the development server

```bash
python app.py
```

Open **<http://127.0.0.1:5000>** in your browser.

---

## 🔑 Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | Optional | — | Google Gemini API key for live AI analysis |
| `GOOGLE_API_KEY` | Optional | — | Accepted as an alias for `GEMINI_API_KEY` |
| `SECRET_KEY` | Optional | `dev-secret-key-change-in-prod` | Flask session secret key — **change in production** |

> Copy `.env.example` to `.env`. The `.env` file is in `.gitignore` and will never be committed.

See [.env.example](./.env.example) for the template.

---

## 🖥️ How to Use

### Step 1 — Enter Monthly Income

Type your net monthly take-home income in Indian Rupees (Rs).

### Step 2 — Log Monthly Expenses

Fill in any applicable expense categories (leave unused ones blank):

| Category | Recommended Max (% of income) |
|---|---|
| 🏠 Rent / Housing | ≤ 30% |
| 🛒 Groceries and Food | ≤ 15% |
| 🚗 Transport | ≤ 10% |
| 🍽️ Dining Out | ≤ 8% |
| 🎬 Entertainment | ≤ 8% |
| ⚡ Utilities | ≤ 8% |
| 🛍️ Shopping | ≤ 8% |
| 💊 Health and Medical | ≤ 5% |
| 🎓 Education | ≤ 10% |
| 🐷 Savings | ≥ 20% (golden benchmark) |
| 📦 Miscellaneous | ≤ 10% |

### Step 3 — Choose a Financial Goal

| Goal Key | Description |
|---|---|
| `emergency_fund` | Build a 6-month safety net covering essential expenses |
| `investment` | Start a disciplined SIP / mutual fund portfolio |
| `vacation` | Save for a dream trip within 12 months |
| `gadget` | Save for a major tech purchase (laptop, smartphone) |
| `debt_repayment` | Avalanche strategy to pay off debt |
| `home_purchase` | Build a property down-payment corpus |
| `retirement` | Maximise long-term compounding via EPF/PPF and equity |
| `education` | Save for higher education or professional certifications |

### Step 4 — Analyse

Click **Analyse My Finances** to receive:

- **Budget Plan** — recommended vs actual spending per category, animated progress bars, and actionable tips
- **Spending Analysis** — percentage of income per category with OK / Over / Under status chips
- **Saving Suggestions** — 4–6 actionable tips mentioning specific rupee amounts
- **Financial Summary** — two-sentence overall health statement

For a step-by-step walkthrough, see [docs/USER_GUIDE.md](./docs/USER_GUIDE.md).

---

## 🤖 AI Modes

### Gemini Mode (Live AI)

When a valid `GEMINI_API_KEY` is configured (via `.env`, the in-app modal, or the request body), the app
calls **Google Gemini 2.0 Flash** with automatic fallback to **Gemini 1.5 Flash**.

### Smart Advisory Engine (Offline Fallback)

When no API key is present or Gemini is unreachable, the app automatically switches to the built-in
**Smart Advisory Engine** — a rule-based planner implementing:

- The **50/30/20 rule**
- Indian household spending benchmarks per category
- Goal-specific allocation strategies (SIP, avalanche debt, RD, PPF, etc.)

### Switching Modes at Runtime

Click the ⚡ **AI Status** button in the header. The key is saved to `localStorage` and, if the server
can write to disk, to `.env` for persistence across restarts.

---

## 🌐 Deployment Options

### 1. GitHub Pages (Static Web App — Free & Instant)
This repository includes a GitHub Actions static workflow (`.github/workflows/static.yml`) that automatically deploys the frontend web app on every push to `main`:
- **Live URL**: [https://kunalkhyade-create.github.io/-New-Personal-Finnace-Advisor-Bot-/](https://kunalkhyade-create.github.io/-New-Personal-Finnace-Advisor-Bot-/)
- Runs 100% in the browser with zero server maintenance.
- Works offline out of the box with the built-in **Smart Advisory Engine**.
- Users can optionally paste their Gemini API key in the UI settings modal to activate live Gemini 2.0 AI insights.

### 2. Render.com (Full-Stack Flask App — Free Cloud Service)
To deploy the Python Flask backend with server-side Gemini API key:
1. Go to [Render.com](https://render.com) and create a free account.
2. Click **New +** → **Web Service** → Connect your GitHub repository:
   `https://github.com/kunalkhyade-create/-New-Personal-Finnace-Advisor-Bot-`
3. Configure the service:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (or automatically read from `Procfile`)
4. Under **Environment Variables**, add:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `SECRET_KEY`: A secure random string
5. Click **Deploy Web Service** to get a permanent live HTTPS URL (e.g., `https://financebot.onrender.com`).

### 3. Public Deployment via Ngrok (Local Tunnel)

Share your locally running app with anyone on the internet using a free Ngrok tunnel.

1. Sign up at <https://ngrok.com> and copy your authtoken.
2. Edit `run_public.py` and paste your token:

   ```python
   TOKEN = "YOUR_NGROK_AUTHTOKEN_HERE"
   ```

3. Run the launcher:

   ```bash
   python run_public.py
   ```

4. Copy the printed public URL and share it.

```
============================================================
  YOUR PUBLIC WEBSITE URL IS LIVE!
  URL: https://xxxx-xx-xx-xxx-xx.ngrok-free.app
============================================================
  Share this URL with anyone to access your Finance Bot.
  Press Ctrl+C to stop.
```

> ⚠️ Free Ngrok URLs change on every restart.

---

## 📡 API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Renders the main single-page UI |
| `POST` | `/analyse` | Runs financial analysis, returns budget and insights |
| `GET` | `/api/key-status` | Returns current AI engine mode |
| `POST` | `/api/key-status` | Sets a new Gemini API key at runtime |
| `GET` | `/health` | Health check — returns app status and mode |

For full request/response schemas and examples, see [docs/API_Documentation.md](./docs/API_Documentation.md).

---

## 📸 Screenshots

> Add screenshots to a `docs/screenshots/` folder and update the paths below.

| Input Form | Analysis Results |
|:---:|:---:|
| *(screenshot pending)* | *(screenshot pending)* |

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `Flask` | 3.0.3 | Web framework and routing |
| `google-generativeai` | 0.8.3 | Google Gemini AI SDK |
| `python-dotenv` | 1.0.1 | `.env` file loader |
| `pyngrok` | 7.2.0 | Ngrok tunnel for public deployment |

```bash
pip install -r requirements.txt
```

---

## 🔒 Security

- API keys loaded from `.env` — never committed to version control
- `.env` is listed in `.gitignore`
- All user input validated server-side (type checking, category whitelist, value bounds)
- Income capped at Rs 1,00,00,000; expense per category capped at Rs 50,00,000
- HTML output escaped in JavaScript to prevent XSS
- Flask `SECRET_KEY` configurable via environment variable

---

## 🧪 Testing

The project does not currently include an automated test suite.
Manual testing can be performed via `curl` or a REST client such as Postman:

```powershell
# Health check (PowerShell)
curl http://127.0.0.1:5000/health

# Test analyse endpoint (Smart Engine — no key needed)
curl -X POST http://127.0.0.1:5000/analyse `
  -H "Content-Type: application/json" `
  -d '{"income":60000,"expenses":{"rent":18000,"food":7000,"dining":3000},"goal":"investment"}'

# Check API key mode
curl http://127.0.0.1:5000/api/key-status
```

> Automated unit and integration tests are planned as a future enhancement.

---

## 🔮 Future Scope

| Enhancement | Description |
|---|---|
| 📅 Monthly Reports | Generate and download PDF/CSV financial reports |
| 🗄️ User Accounts and History | Persistent login with expense history (SQLite/PostgreSQL) |
| 📈 Trend Charts | Interactive spending trend graphs over multiple months |
| 📱 Progressive Web App | Installable PWA with offline support |
| 🤖 Conversational AI | Multi-turn chat interface for follow-up financial questions |
| 🧪 Automated Tests | pytest unit tests for backend functions and API endpoints |
| 🌐 Multi-currency Support | Support for currencies beyond INR |

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup,
coding conventions, and pull request guidelines.

---

## 👤 Author and License

**Author:** Kunal Khyade

**License:** MIT — free to use, modify, and distribute with attribution.

---

<div align="center">
Built with love using Flask and Google Gemini AI
</div>
