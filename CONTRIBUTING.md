# Contributing to FinanceBot

Thank you for your interest in contributing! This guide explains how to set up your development
environment, follow project conventions, and submit your changes.

> **Related docs:** [README](./README.md) | [Architecture](./docs/architecture.md)

---

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Conventions](#coding-conventions)
  - [Python (Backend)](#python-backend)
  - [JavaScript (Frontend)](#javascript-frontend)
  - [HTML / CSS](#html--css)
- [Running Locally](#running-locally)
- [Branch Strategy](#branch-strategy)
- [Commit Messages](#commit-messages)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Reporting Bugs](#reporting-bugs)
- [Security](#security)

---

## Development Setup

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/personal-finance-advisor-bot.git
cd personal-finance-advisor-bot
```

### 2. Create a virtual environment

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

### 4. Configure environment

```bash
copy .env.example .env   # Windows
cp .env.example .env     # macOS / Linux
```

Edit `.env` and add your `GEMINI_API_KEY` (optional) and a strong `SECRET_KEY`.

### 5. Run the development server

```bash
python app.py
```

Open <http://127.0.0.1:5000> to confirm the app loads correctly.

---

## Project Structure

```
app.py                  # All Flask routes and backend logic
run_public.py           # Ngrok public launcher (do not modify for features)
requirements.txt        # Python dependencies — update if you add packages
templates/index.html    # Single Jinja2 template — all HTML lives here
static/css/style.css    # Design system — CSS custom properties and components
static/js/main.js       # All frontend JS — form handling and result rendering
docs/                   # Documentation files
```

---

## Coding Conventions

### Python (Backend)

- Follow **PEP 8** style guidelines.
- Use `snake_case` for variables, functions, and module-level constants.
- Use `UPPER_SNAKE_CASE` for true constants (e.g., `MAX_INCOME`, `VALID_GOALS`).
- Add docstrings to all new functions following the existing format:
  ```python
  def my_function(arg):
      """One-sentence summary of what this function does."""
  ```
- Do not use bare `except:`; always catch specific exceptions.
- Keep route handler functions thin — extract logic into helper functions.
- Log significant events using `logger.info()` and warnings using `logger.warning()`.

### JavaScript (Frontend)

- Use `"use strict";` (already present at the top of `main.js`).
- Use `const` by default; use `let` only when the variable must be reassigned.
- Use `camelCase` for variable and function names.
- Always escape dynamic content using `escapeHtml()` before inserting into the DOM.
- Use `async/await` with `try/catch` for all `fetch()` calls.
- Do not use any external JS frameworks or libraries — the project is intentionally vanilla.

### HTML / CSS

- HTML must remain valid and semantic.
- Use the existing CSS custom properties defined in `:root` — do not add new hardcoded colour values.
- Follow the BEM-inspired naming already used (e.g., `budget-item`, `budget-item__header`).
- Add new styles to `style.css`; keep them grouped logically with a comment header.

---

## Running Locally

```powershell
# Normal run
python app.py

# With hot-reload (Flask debug mode)
$env:FLASK_DEBUG = "1"; python app.py

# Health check
curl http://127.0.0.1:5000/health

# Quick API test
curl -X POST http://127.0.0.1:5000/analyse `
  -H "Content-Type: application/json" `
  -d '{"income":60000,"expenses":{"rent":15000,"food":6000},"goal":"investment"}'
```

---

## Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, production-ready code |
| `feature/<name>` | New features (e.g., `feature/pdf-export`) |
| `fix/<name>` | Bug fixes (e.g., `fix/json-parse-error`) |
| `docs/<name>` | Documentation-only changes (e.g., `docs/api-reference`) |
| `refactor/<name>` | Code restructuring without behaviour changes |

- Always branch off `main`.
- Never commit directly to `main`.

---

## Commit Messages

Follow the **Conventional Commits** format:

```
<type>(<scope>): <short description>

[optional body]
[optional footer]
```

**Types:**

| Type | When to use |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes only |
| `style` | Formatting, whitespace — no logic change |
| `refactor` | Code restructuring — no new feature, no bug fix |
| `test` | Adding or updating tests |
| `chore` | Build process or tooling changes |

**Examples:**

```
feat(backend): add support for multi-currency income inputs
fix(frontend): correct progress bar width clamping for 0% actual
docs(api): add response examples for /health endpoint
```

---

## Pull Request Guidelines

1. **One feature or fix per PR** — keep changes focused.
2. **Update documentation** — if you change an endpoint, update `docs/API_Documentation.md`.
3. **Test manually** — run the app locally and test the affected flow before opening a PR.
4. **Write a clear PR description:**
   - What does this PR do?
   - Why is this change needed?
   - How was it tested?
5. **Do not commit:**
   - `.env` files
   - Virtual environment folders (`myenv/`, `venv/`, `env/`)
   - `__pycache__/`, `*.pyc`
   - Database files containing personal data
   - Generated credentials or secrets

---

## Reporting Bugs

Open a GitHub Issue with the following information:

1. **Description** — what went wrong?
2. **Steps to reproduce** — exactly how to trigger the bug.
3. **Expected behaviour** — what should have happened?
4. **Actual behaviour** — what actually happened?
5. **Environment** — OS, Python version, browser.
6. **Logs** — paste relevant terminal output or browser console errors.

---

## Security

- Never include real API keys, passwords, or personal data in commits or issues.
- If you discover a security vulnerability, please report it privately rather than opening a public issue.
