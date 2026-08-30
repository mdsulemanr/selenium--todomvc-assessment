# Selenium Execution Guide

This guide explains the commands used to run the Selenium TodoMVC suite locally, in headed mode, with browser/viewport parameterization, with pytest-xdist parallelism, and with Selenium Grid.

## Baseline Commands

Use the virtualenv Python module form on Windows:

```powershell
.\.venv\Scripts\python -m pytest
```

This runs the default profile:

```text
browser: chrome
viewport: desktop
execution: local WebDriver
parallelism: off
```

Run only smoke tests:

```powershell
.\.venv\Scripts\python -m pytest -m smoke
```

Run only regression tests:

```powershell
.\.venv\Scripts\python -m pytest -m regression
```

Show framework logs in the terminal:

```powershell
.\.venv\Scripts\python -m pytest --log-cli-level=INFO
```

## Headed Mode

Use headed mode when you want to see the browser:

```powershell
.\.venv\Scripts\python -m pytest --headed
```

Use action delay only for demos/debugging:

```powershell
.\.venv\Scripts\python -m pytest --headed --action-delay=1
```

Run headed with a mobile viewport:

```powershell
.\.venv\Scripts\python -m pytest --headed --viewport mobile
```

## Parameterization

Parameterization means pytest creates multiple test cases from the same test code.

Run one browser:

```powershell
.\.venv\Scripts\python -m pytest --browser chrome
.\.venv\Scripts\python -m pytest --browser firefox
.\.venv\Scripts\python -m pytest --browser edge
```

Run multiple browsers:

```powershell
.\.venv\Scripts\python -m pytest --browser chrome,firefox,edge
```

With two tests, that creates six test cases:

```text
test_add_and_complete_todos[chrome-desktop]
test_add_and_complete_todos[firefox-desktop]
test_add_and_complete_todos[edge-desktop]
test_filter_behaviour_is_correct[chrome-desktop]
test_filter_behaviour_is_correct[firefox-desktop]
test_filter_behaviour_is_correct[edge-desktop]
```

Run viewport profiles:

```powershell
.\.venv\Scripts\python -m pytest --viewport desktop
.\.venv\Scripts\python -m pytest --viewport mobile
```

Run a browser and viewport matrix:

```powershell
.\.venv\Scripts\python -m pytest --browser chrome,firefox,edge --viewport desktop,mobile
```

Check the matrix without opening browsers:

```powershell
.\.venv\Scripts\python -m pytest --collect-only -q --browser chrome,firefox,edge --viewport desktop,mobile
```

Without `-n`, parameterized cases run sequentially.

## Parallelism With pytest-xdist

pytest-xdist runs multiple pytest workers at the same time. Each worker owns its own WebDriver session.

Run two workers:

```powershell
.\.venv\Scripts\python -m pytest -n 2
```

Let pytest-xdist choose the worker count:

```powershell
.\.venv\Scripts\python -m pytest -n auto
```

Run a browser matrix in parallel:

```powershell
.\.venv\Scripts\python -m pytest -n 3 --browser chrome,firefox,edge
```

Example behavior:

```text
worker 1 -> Chrome session -> test case A
worker 2 -> Chrome session -> test case B
worker 3 -> Firefox session -> test case C
```

The exact assignment is handled by pytest-xdist. The important rule is that each parallel test gets its own browser session.

## Selenium Grid

Selenium Grid is used when browser sessions should run remotely instead of directly on the local machine.

Local execution:

```text
pytest -> webdriver.Chrome/Firefox/Edge -> local browser
```

Grid execution:

```text
pytest -> webdriver.Remote -> Selenium Grid -> browser node
```

Start the local Docker Compose Grid:

```powershell
.\scripts\start-grid.ps1
```

Run one browser through Grid:

```powershell
.\.venv\Scripts\python -m pytest --remote-url http://localhost:4444 --browser chrome
```

Run a browser matrix through Grid in parallel:

```powershell
.\.venv\Scripts\python -m pytest -n 3 --remote-url http://localhost:4444 --browser chrome,firefox,edge
```

Stop the Grid:

```powershell
.\scripts\stop-grid.ps1
```

## Reporting

The project keeps `pytest-html` as the default lightweight report:

```text
reports/report.html
```

Use Allure when you need richer evidence for review, demos, or CI artifacts:

```powershell
.\.venv\Scripts\python -m pytest --alluredir reports/allure-results
```

Run Allure with parallel execution:

```powershell
.\.venv\Scripts\python -m pytest -n 2 --alluredir reports/allure-results
```

Run Allure with browser parameterization:

```powershell
.\.venv\Scripts\python -m pytest --browser chrome,firefox,edge --alluredir reports/allure-results
```

Use the helper script:

```powershell
.\scripts\run-allure.ps1
.\scripts\run-allure.ps1 -Workers 2 -Browser chrome,firefox
```

The pytest Allure adapter writes raw results to:

```text
reports/allure-results
```

If the Allure CLI is installed, generate and open the HTML report:

```powershell
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

or:

```powershell
.\scripts\open-allure-report.ps1
```

Reporting choices:

- `pytest-html`: simple report, low maintenance, already built into the default run.
- `Allure`: richer report with screenshots, environment metadata, steps, labels, and CI-friendly artifacts.
- `ReportPortal`: centralized live reporting dashboard for larger teams, but requires a running service and credentials.

## Docker Guidance

Docker is not mandatory for every live automation project.

Use Docker/Grid when the project needs:

- repeatable browser infrastructure across machines
- parallel cross-browser execution without installing every browser locally
- CI browser nodes that behave like local Grid nodes
- scalable test capacity beyond one local machine

Skip Docker/Grid when:

- the suite is small
- local Chrome/Firefox coverage is enough
- the team or CI environment cannot run Docker reliably
- Grid setup would add more maintenance than value

For this project, Docker is useful because the suite is intended to demonstrate enterprise-style Selenium scalability. It is not required for normal local runs.

Check Docker availability:

```powershell
docker --version
docker compose version
```

Current Docker Desktop for Windows requires a supported Windows version and container backend. For the normal WSL 2 backend, verify:

```powershell
winver
wsl --version
```

Expected baseline for current Docker Desktop:

```text
Windows 10 Pro/Enterprise/Education 22H2 build 19045 or newer
or Windows 11 Pro/Enterprise/Education 23H2 build 22631 or newer
WSL 2.1.5 or newer
hardware virtualization enabled
```

If those commands fail, install Docker Desktop or continue using local runs:

```powershell
.\.venv\Scripts\python -m pytest
.\.venv\Scripts\python -m pytest -n 2
.\.venv\Scripts\python -m pytest --browser chrome,firefox
```

If the OS is older than Docker's supported baseline, update Windows first, enable/install WSL 2, restart the machine, then install Docker Desktop.

## Browser Support Notes

Chrome, Firefox, and Edge are the supported local/browser-matrix targets in this Windows project.

Check local browsers:

```powershell
chrome --version
firefox --version
msedge --version
```

If Edge opens manually but `msedge --version` fails, Edge may not be on PATH or may be installed under `Microsoft\EdgeCore`. The framework includes a Windows fallback for that install layout.

Safari requires Apple's `safaridriver` and is a macOS/Safari target, so it is not included in this Windows-focused framework.

Internet Explorer is not included. Standalone IE is no longer a normal enterprise automation target; Selenium's IE path is mainly for Edge IE Compatibility Mode and needs special Windows configuration.

## Script Shortcuts

Local run:

```powershell
.\scripts\run-local.ps1
.\scripts\run-local.ps1 -Browser firefox -Viewport mobile
```

Parallel local run:

```powershell
.\scripts\run-parallel.ps1 -Workers 2
.\scripts\run-parallel.ps1 -Workers auto -Browser chrome,firefox,edge
```

Grid run:

```powershell
.\scripts\start-grid.ps1
.\scripts\run-grid.ps1 -Workers 3 -Browser chrome,firefox,edge
.\scripts\stop-grid.ps1
```

## Recommended Learning Order

Run these in order:

```powershell
.\.venv\Scripts\python -m pytest --headed
.\.venv\Scripts\python -m pytest --headed --viewport mobile
.\.venv\Scripts\python -m pytest --browser chrome,firefox,edge --collect-only -q
.\.venv\Scripts\python -m pytest --browser chrome,firefox,edge
.\.venv\Scripts\python -m pytest -n 2
.\.venv\Scripts\python -m pytest -n 3 --browser chrome,firefox,edge
```

After Docker is installed:

```powershell
.\scripts\start-grid.ps1
.\scripts\run-grid.ps1 -Workers 3 -Browser chrome,firefox,edge
.\scripts\stop-grid.ps1
```
