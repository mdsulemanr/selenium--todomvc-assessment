# Selenium TodoMVC Assessment

A Selenium + Python migration of the Playwright TodoMVC assessment. This project is intentionally separate from the Playwright project so both suites can coexist independently.

## Tech Stack

- Python
- Selenium
- pytest
- pytest-html
- python-dotenv
- Chrome via Selenium Manager

## Structure

```text
selenium-todomvc-assessment/
|-- config/
|   `-- settings.py
|-- pages/
|   `-- todo_page.py
|-- test_data/
|   |-- routes.py
|   `-- todos.py
|-- tests/
|   `-- test_todomvc.py
|-- conftest.py
|-- pytest.ini
|-- requirements.txt
|-- .env
`-- .env.example
```

## Setup

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env
```

## Run Tests

```powershell
.venv\Scripts\pytest
```

The default pytest configuration writes a self-contained HTML report to:

```text
reports/report.html
```

Failure screenshots are saved to `screenshots/` and attached to the pytest-html report.

## Environment

`.env.example` provides the default target:

```dotenv
BASE_URL=https://demo.playwright.dev
HEADLESS=true
```

- `BASE_URL` controls the target domain.
- `HEADLESS=true` runs Chrome headless.
- `HEADLESS=false` opens Chrome visibly for debugging.

## Browser Scope

This v1 implementation is intentionally Chrome-only to match the original Playwright project's Chromium-only setup. Selenium Manager resolves the Chrome driver automatically, so no driver binary is committed.

## Coverage

- Add and complete todos
- Validate item count and remaining counter
- Validate filter behavior for Active, Completed, and All routes
- Validate selected filter state and checkbox completion state

## Troubleshooting

If Chrome does not start, confirm Chrome is installed and up to date:

```powershell
chrome --version
```

If Selenium Manager cannot download or resolve a driver, check proxy/VPN settings and rerun:

```powershell
.venv\Scripts\pytest -v
```

For headed debugging, set this in `.env`:

```dotenv
HEADLESS=false
```

Generated artifacts are ignored by git: `.venv/`, `reports/`, `screenshots/`, `__pycache__/`, and `.pytest_cache/`.
