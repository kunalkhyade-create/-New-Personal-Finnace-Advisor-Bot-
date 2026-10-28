# User Guide — FinanceBot

> **Related docs:** [README](../README.md) | [API Documentation](./API_Documentation.md)

Welcome to **FinanceBot** — your AI-powered personal finance advisor.
This guide walks you through every feature of the app, from first launch to reading your results.

---

## Table of Contents

- [1. First-Time Setup](#1-first-time-setup)
- [2. Opening the App](#2-opening-the-app)
- [3. Understanding the Interface](#3-understanding-the-interface)
- [4. Step-by-Step: Analysing Your Finances](#4-step-by-step-analysing-your-finances)
  - [Step 1 — Enter Your Monthly Income](#step-1--enter-your-monthly-income)
  - [Step 2 — Add Your Expenses](#step-2--add-your-expenses)
  - [Step 3 — Choose a Financial Goal](#step-3--choose-a-financial-goal)
  - [Step 4 — Run the Analysis](#step-4--run-the-analysis)
- [5. Reading Your Results](#5-reading-your-results)
  - [Personalised Budget](#personalised-budget)
  - [Spending Analysis](#spending-analysis)
  - [Saving Suggestions](#saving-suggestions)
  - [Financial Summary](#financial-summary)
- [6. Configuring the AI Engine](#6-configuring-the-ai-engine)
  - [Using the Smart Advisory Engine (Default)](#using-the-smart-advisory-engine-default)
  - [Activating Gemini 2.0 AI](#activating-gemini-20-ai)
  - [Switching Back to Smart Engine](#switching-back-to-smart-engine)
- [7. Sharing the App Publicly (Ngrok)](#7-sharing-the-app-publicly-ngrok)
- [8. Troubleshooting](#8-troubleshooting)

---

## 1. First-Time Setup

Before using the app for the first time, complete the installation steps in the
[README Quick Start](../README.md#-quick-start):

1. Clone the repository.
2. Create and activate a Python virtual environment (`myenv`).
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and (optionally) add your Gemini API key.
5. Start the server: `python app.py`

> The app runs fully without an API key using the built-in Smart Advisory Engine.
> An API key is only needed to use live Google Gemini 2.0 AI responses.

---

## 2. Opening the App

Once the server is running, open your web browser and navigate to:

```
http://127.0.0.1:5000
```

You should see the FinanceBot landing page with the header, hero section, and input form.

---

## 3. Understanding the Interface

| Section | Description |
|---|---|
| **Header** | Shows the FinanceBot brand and an ⚡ AI Status button (top right) |
| **Hero** | Brief description of what FinanceBot does |
| **Your Financial Profile** | The main input form — income, expenses, goal |
| **Analyse Button** | Submits the form and triggers the analysis |
| **Results Section** | Appears below the form after analysis completes |
| **Footer** | Privacy note — confirms no data is stored |

---

## 4. Step-by-Step: Analysing Your Finances

### Step 1 — Enter Your Monthly Income

In the **Monthly Take-Home Income** field, enter your net monthly salary or income in Indian Rupees.

- Example: `75000` for Rs 75,000/month
- Do not include commas or the Rs symbol; enter digits only.
- Minimum: Rs 1 — Maximum: Rs 1,00,00,000

### Step 2 — Add Your Expenses

Fill in the amounts you spend each month for any applicable categories:

| Category | What to include |
|---|---|
| **Rent / Housing** | Rent, mortgage EMI, society maintenance |
| **Groceries and Food** | Grocery shopping, monthly kirana bill |
| **Transport** | Petrol, auto/cab fares, metro pass, vehicle EMI |
| **Dining Out** | Restaurants, food delivery apps (Swiggy, Zomato) |
| **Entertainment** | OTT subscriptions, cinema, gaming |
| **Utilities** | Electricity, water, gas, mobile/broadband bill |
| **Savings** | Amount you transfer to savings or investment accounts |
| **Health and Medical** | Doctor visits, medicines, gym membership |
| **Education** | Course fees, tuition, books, online certifications |
| **Shopping** | Clothing, electronics, household items |
| **Miscellaneous** | Everything else that doesn't fit above |

**Tips:**
- Leave any category blank (or at `0`) if it does not apply to you.
- Enter at least one non-zero expense to proceed.
- Use your actual monthly spending, not an estimate of what you wish you spent.

### Step 3 — Choose a Financial Goal

Select your **primary financial goal** from the dropdown:

| Option | Best for |
|---|---|
| 🛡️ Build Emergency Fund | Anyone who does not have 3–6 months of expenses saved |
| 📈 Start Investing (SIPs) | Those ready to begin a disciplined investment habit |
| ✈️ Save for Vacation | Planning a trip within the next 12 months |
| 💻 Save for a Gadget | Saving for a laptop, smartphone, or other tech purchase |
| 💳 Pay Off Debt | Reducing credit card balances or personal loans |
| 🏠 Home Down Payment | Saving for a property purchase within 2–5 years |
| 🌅 Build Retirement Corpus | Long-term wealth accumulation via compounding |
| 🎓 Education / Certification | Saving for a degree, diploma, or professional course |

### Step 4 — Run the Analysis

Click the **Analyse My Finances** button.

- A loading spinner appears while the analysis runs (typically under 2 seconds).
- The results section scrolls into view automatically once complete.

---

## 5. Reading Your Results

### Personalised Budget

The **Personalised Budget** panel shows each expense category you entered, with:

- **Actual spending** — what you reported
- **Recommended spending** — the recommended maximum for your income level
- **Animated progress bar** — fills to show how much of the recommended budget you have used
- **Status badge:**
  - 🟢 **OK** — spending is within the recommended range
  - 🔴 **OVER** — spending exceeds the recommended limit
  - 🔵 **UNDER** — spending is significantly below the recommended limit (can indicate under-reporting or surplus)
- **Tip** — one actionable suggestion specific to this category

### Spending Analysis

The **Spending Analysis** panel shows compact chips for each category:

- **Category name** and a brief one-sentence insight
- **Percentage of income** — how much of your total income this category consumes
- Colour-coded by status (OK / OVER / UNDER)

### Saving Suggestions

The **Saving Suggestions** panel lists 4–6 concrete, goal-specific tips, each mentioning a specific rupee
amount. For example:

> "Automate a diversified SIP of Rs.15,000 in Nifty 50 and mid-cap index mutual funds on the 1st of every month."

### Financial Summary

The **Summary Banner** at the top of the results provides a two-sentence overall assessment of your
financial health, including your total expense-to-income ratio and a statement about your goal.

The banner also shows an **engine badge**:
- ✨ **Gemini 2.0 AI** — analysis was generated by the live Gemini model
- ⚡ **Smart Advisor** — analysis was generated by the built-in algorithmic engine

---

## 6. Configuring the AI Engine

### Using the Smart Advisory Engine (Default)

No configuration is needed. If no Gemini API key is set, the app automatically uses the built-in
**Smart Advisory Engine**, which applies the 50/30/20 rule and Indian household benchmarks. It works
completely offline and requires no internet connection beyond loading the web page.

### Activating Gemini 2.0 AI

To get live, context-aware AI responses powered by Google Gemini 2.0 Flash:

1. Get a free API key at <https://aistudio.google.com/app/apikey>.
2. Click the ⚡ **AI Status** button in the top-right corner of the app.
3. Paste your key into the **Google Gemini API Key** field.
4. Click **Save and Activate**.

The header badge updates to show ✨ **Gemini 2.0 AI**.

**Persistence options:**
- The key is saved to `localStorage` for the current browser session.
- If the server can write to `.env`, the key is also saved there for persistence across server restarts.

### Switching Back to Smart Engine

1. Click the ⚡ **AI Status** button.
2. Click **Use Smart Engine**.

The key is removed from `localStorage` and the header badge reverts to ⚡ **Smart Advisor**.

---

## 7. Sharing the App Publicly (Ngrok)

To share a live link to your running app with anyone (for a demo or presentation):

1. Sign up for a free account at <https://ngrok.com>.
2. Copy your authtoken from the Ngrok dashboard.
3. Open `run_public.py` and replace `YOUR_NGROK_AUTHTOKEN_HERE` with your token:

   ```python
   TOKEN = "2abc123yourtoken..."
   ```

4. Run:

   ```bash
   python run_public.py
   ```

5. Copy the URL printed in the terminal (e.g., `https://xxxx.ngrok-free.app`) and share it.

Press `Ctrl+C` to stop the tunnel and the server.

> **Note:** Free Ngrok URLs are temporary and change every time you restart.

---

## 8. Troubleshooting

### The page does not load at http://127.0.0.1:5000

- Make sure the Flask server is running: `python app.py`
- Check that your virtual environment is activated: `myenv\Scripts\activate` (Windows)
- Make sure no other process is using port 5000. Try a different port:
  ```bash
  set FLASK_RUN_PORT=5001 && python app.py
  ```

### "Please enter at least one expense amount" error

- At least one expense field must have a value greater than zero before submitting.

### "Please provide a valid positive monthly income" error

- Make sure the income field contains a number greater than zero.
- Do not include currency symbols or commas.

### The analysis uses Smart Engine even though I entered an API key

- Verify the key is valid at <https://aistudio.google.com>.
- Make sure the key does not start with `your_` or contain placeholder text.
- Check the server terminal for a warning message about the Gemini API call.
- Re-enter the key via the ⚡ **AI Status** modal and click **Save and Activate**.

### The Ngrok URL shows a browser security warning

- This is normal for free Ngrok tunnels. Click **Visit Site** to proceed.
- Upgrade to a paid Ngrok plan to use a custom domain with a valid SSL certificate.

### "Network connection error" in the browser

- The Flask server may have stopped. Restart it with `python app.py`.
- Check for Python errors in the terminal.
