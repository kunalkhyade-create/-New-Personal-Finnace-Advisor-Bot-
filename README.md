# 💰 Personal Finance Advisor Bot

An AI-powered personal finance advisor built with **Flask** and **Google Gemini 2.0 Flash**. Enter your monthly income and expenses, set a financial goal, and receive a personalised budget plan, spending analysis, and saving suggestions — instantly.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Budget Generator** | Personalised monthly budget based on income and expense data |
| **Spending Analyser** | Category-by-category analysis with status indicators (over / on-track / under) |
| **Saving Suggestions** | 4–6 specific, rupee-quantified saving recommendations |
| **Financial Summary** | AI-written two-sentence health overview |
| **Public Deployment** | One-command Ngrok tunnel for sharing the app publicly |

---

## 🗂️ Project Structure

```
new personal finance advisor bot/
├── app.py                  # Flask backend + Gemini AI integration
├── run_public.py           # Ngrok public deployment launcher
├── requirements.txt        # Python dependencies
├── .env.example            # Template for environment variables
├── .gitignore
├── templates/
│   └── index.html          # Single-page UI
└── static/
    ├── css/
    │   └── style.css       # Dark glassmorphism design system
    └── js/
        └── main.js         # Async form handling + dynamic rendering
```

---

## 🚀 Quick Start

### 1. Clone / Open the project

```powershell
cd "new personal finance advisor bot"
```

### 2. Create & activate a virtual environment

```powershell
python -m venv myenv
myenv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Add your Gemini API Key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Get your key** → [https://aistudio.google.com](https://aistudio.google.com) → Get API Key → Create API Key

### 5. Run locally

```powershell
python app.py
```

Open your browser at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🌍 Public Deployment (Ngrok)

### 1. Sign up at [ngrok.com](https://ngrok.com) and copy your authtoken

### 2. Edit `run_public.py` — replace the placeholder:

```python
TOKEN = "YOUR_NGROK_AUTHTOKEN_HERE"
```

### 3. Run the public launcher:

```powershell
python run_public.py
```

The terminal will print your live public URL:

```
============================================================
  YOUR PUBLIC WEBSITE URL IS LIVE!
  URL: https://xxxx-xx-xx-xxx-xx.ngrok-free.app
============================================================
```

> **Note:** Free Ngrok URLs change every restart. Upgrade for a fixed domain.

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Google Gemini API key |
| `SECRET_KEY` | Optional | Flask session secret (auto-generated if absent) |

---

## 🏗️ Architecture

```
Browser (HTML / CSS / JS)
        │  fetch POST /analyse (JSON)
        ▼
Flask Backend (app.py)
  ├── validate_input()
  ├── build_prompt()  ←── CATEGORY_TIPS + GOAL_DESCRIPTIONS
  ├── model.generate_content()  ──► Gemini 2.0 Flash
  └── extract_json()
        │  JSON response
        ▼
Frontend renders budget / analysis / suggestions
```

---

## 📦 Dependencies

```
Flask==3.0.3
google-generativeai==0.8.3
python-dotenv==1.0.1
pyngrok==7.2.0
```

---

## 🔒 Security

- API key loaded from `.env` — never committed to version control
- `.env` is listed in `.gitignore`
- All user input is validated server-side before being sent to the AI
- HTML output is escaped in JavaScript to prevent XSS

---

## 📄 License

MIT — free to use and modify.
