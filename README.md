# Selenium TodoMVC Assessment

A Selenium + Python migration of the Playwright TodoMVC assessment. This project is intentionally separate from the Playwright project so both suites can coexist independently.

## Tech Stack

- Python
- Selenium
- pytest
- pytest-html
- pytest-xdist
- allure-pytest
- python-dotenv
- Chrome, Firefox, and Edge via Selenium Manager
- Selenium Grid through Docker Compose

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
.\.venv\Scripts\python -m pytest
```

The default pytest configuration writes a self-contained HTML report to:

```text
reports/report.html
```

Runtime logs are written to:

```text
reports/test.log
```

Failure screenshots are saved to `screenshots/` and attached to the pytest-html report.

Allure reporting is also supported for richer local/CI evidence:

```powershell
.\.venv\Scripts\python -m pytest --alluredir reports/allure-results
.\scripts\run-allure.ps1
```

## Environment

`.env.example` provides the default target:

```dotenv
BASE_URL=https://demo.playwright.dev
HEADLESS=true
ACTION_DELAY=0
```

- `BASE_URL` controls the target domain.
- `HEADLESS=true` runs Chrome headless by default.
- `HEADLESS=false` opens Chrome visibly when set in `.env`.
- `ACTION_DELAY=1.5` slows visible page actions when set in `.env`.

For ad hoc debugging, prefer pytest CLI flags:

```powershell
.\.venv\Scripts\python -m pytest --headed
```

For a headed slow-motion run:

```powershell
.\.venv\Scripts\python -m pytest --headed --action-delay=2
```

To show framework logs in the terminal while debugging:

```powershell
.\.venv\Scripts\python -m pytest --log-cli-level=INFO
```

## Command Reference

Use the virtualenv Python module form for consistent Windows execution:

```powershell
.\.venv\Scripts\python -m pytest
```

Run visibly:

```powershell
.\.venv\Scripts\python -m pytest --headed
.\.venv\Scripts\python -m pytest --headed --action-delay=1
.\.venv\Scripts\python -m pytest --headed --viewport mobile
```

Run one browser or viewport profile:

```powershell
.\.venv\Scripts\python -m pytest --browser chrome
.\.venv\Scripts\python -m pytest --browser firefox
.\.venv\Scripts\python -m pytest --browser edge
.\.venv\Scripts\python -m pytest --viewport mobile
```

Run a parameterized matrix. This collects each test once for every browser/viewport combination:

```powershell
.\.venv\Scripts\python -m pytest --browser chrome,firefox,edge
.\.venv\Scripts\python -m pytest --browser chrome,firefox,edge --viewport desktop,mobile
```

Run in parallel with pytest-xdist. `-n 2` starts two pytest workers, so two test cases can own separate browser sessions at the same time:

```powershell
.\.venv\Scripts\python -m pytest -n 2
.\.venv\Scripts\python -m pytest -n auto
.\.venv\Scripts\python -m pytest -n 3 --browser chrome,firefox,edge
```

Check collection without opening browsers:

```powershell
.\.venv\Scripts\python -m pytest --collect-only -q
.\.venv\Scripts\python -m pytest --collect-only -q --browser chrome,firefox,edge --viewport desktop,mobile
```

Concept mapping:

- `--browser` and `--viewport` control parameterization: what combinations should run.
- `-n 2`, `-n 3`, or `-n auto` controls parallelism: how many pytest workers run at once.
- `--remote-url` controls Grid execution: where browser sessions are created.
- Docker is only required for local Selenium Grid, not for normal local browser runs.

Selenium Manager resolves local browser drivers automatically, so no driver binary is committed.

Learning sequence:

```powershell
.\.venv\Scripts\python -m pytest --headed
.\.venv\Scripts\python -m pytest --headed --viewport mobile
.\.venv\Scripts\python -m pytest --browser chrome,firefox,edge --collect-only -q
.\.venv\Scripts\python -m pytest --browser chrome,firefox,edge
.\.venv\Scripts\python -m pytest -n 2
.\.venv\Scripts\python -m pytest -n 3 --browser chrome,firefox,edge
```

Parameterization means pytest creates multiple test cases from the same test code. For example, `--browser chrome,firefox,edge` runs each test once for Chrome, once for Firefox, and once for Edge. Without `-n`, those cases run sequentially.

Parallelism means pytest-xdist starts multiple workers. Each worker gets its own WebDriver session, so `-n 2` can run two browser sessions at the same time.

## Selenium Grid

Start the local Docker Compose Grid:

```powershell
.\scripts\start-grid.ps1
```

Run tests remotely through Grid:

```powershell
.\.venv\Scripts\python -m pytest --remote-url http://localhost:4444 --browser chrome
.\.venv\Scripts\python -m pytest -n 3 --remote-url http://localhost:4444 --browser chrome,firefox,edge
```

Stop the Grid:

```powershell
.\scripts\stop-grid.ps1
```

The Grid uses Selenium Docker images for Chrome, Firefox, and Edge nodes. Set `SELENIUM_IMAGE_TAG` before starting the Grid if a pinned image tag is required.

If Docker is not installed or `docker --version` fails, skip Grid commands and use local browser or local parallel commands until Docker Desktop is available.

## Browser Notes

Local browser runs require the selected browser to be installed on the machine. Check availability with:

```powershell
chrome --version
firefox --version
msedge --version
```

If Edge is not installed, not on PATH, or installed in a non-standard location, local `--browser edge` may fail or hang during startup. Grid-based Edge can still work because the Docker node image contains the browser.

Safari is not included in this Windows-focused project because Safari WebDriver requires Apple's `safaridriver` and is intended for Safari on macOS. Internet Explorer is not included because standalone IE is no longer a normal enterprise browser target; Selenium's IE support is now mainly for Edge IE Compatibility Mode and needs special Windows configuration.

## Script Shortcuts

PowerShell wrappers are provided for common runs:

```powershell
.\scripts\run-local.ps1
.\scripts\run-local.ps1 -Browser firefox -Viewport mobile
.\scripts\run-parallel.ps1 -Workers auto -Browser chrome,firefox,edge
.\scripts\run-grid.ps1 -Workers 3 -Browser chrome,firefox,edge
.\scripts\run-allure.ps1 -Workers 2 -Browser chrome,firefox
.\scripts\open-allure-report.ps1
```

These scripts invoke pytest through the virtualenv Python interpreter and keep the same options available for ad hoc runs.

## Automation Strategy

Project automation practices, locator priority, debugging workflow, and audit checklist are documented in [docs/AUTOMATION_STRATEGY.md](docs/AUTOMATION_STRATEGY.md).

Git/GitHub workflow, future CI job strategy, environment handling, and artifact practices are documented in [docs/CI_CD_STRATEGY.md](docs/CI_CD_STRATEGY.md).

Logging principles for local debugging, CI triage, and audit evidence are documented in [docs/LOGGING_STRATEGY.md](docs/LOGGING_STRATEGY.md).

Detailed execution commands for headed mode, parameterization, xdist parallelism, Selenium Grid, Docker, and browser support are documented in [docs/EXECUTION_GUIDE.md](docs/EXECUTION_GUIDE.md).

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
