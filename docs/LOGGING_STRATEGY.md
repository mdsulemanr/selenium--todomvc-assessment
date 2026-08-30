# Selenium Logging Strategy

## Purpose

Logging helps explain what the automation did before a failure. It supports debugging, bug investigation, CI triage, and audit review, but it does not replace assertions, screenshots, or pytest-html reports.

Good logs should answer:

- Which test flow was running?
- What major user action was attempted?
- Which environment and route were used?
- What evidence exists when the test failed?

## Logging Principles

Use Python's standard `logging` module. Prefer one module-level logger per file:

```python
import logging

logger = logging.getLogger(__name__)
```

Use logs for meaningful workflow boundaries, not every Selenium call. Keep logs readable, deterministic, and safe to share.

Avoid:

- `print()` in framework or test code.
- Logging secrets, tokens, credentials, `.env` contents, or sensitive test data.
- Using logs as assertions.
- Adding fixed sleeps to make logs easier to read.
- Logging noisy implementation details that do not help triage.

## Recommended Levels

- `DEBUG`: locator details, resolved URLs, low-level page-object diagnostics.
- `INFO`: major user actions such as opening TodoMVC, adding a todo, completing a todo, or selecting a filter.
- `WARNING`: unexpected but handled behavior.
- `ERROR`: setup, teardown, or framework-level failures that need attention.

Tests should stay readable. Page objects and fixtures are the best places for most diagnostic logs because they already own browser setup and user actions.

Useful examples:

- `INFO`: `Starting test: tests/test_todomvc.py::test_add_and_complete_todos; markers=regression, smoke`
- `INFO`: `Selecting Active filter`
- `DEBUG`: `Searching 3 todo rows for matching title`
- `ERROR`: `Failure URL: https://demo.playwright.dev/todomvc/#/active`

## Pytest Usage

Prefer pytest's built-in logging controls for local debugging:

```powershell
.venv\Scripts\pytest --log-cli-level=INFO
.venv\Scripts\pytest --log-file=reports/test.log --log-file-level=DEBUG
```

Recommended future defaults, if persistent log files are needed:

```ini
log_file = reports/test.log
log_file_level = INFO
log_file_format = %(asctime)s %(levelname)s %(name)s %(message)s
log_file_date_format = %Y-%m-%d %H:%M:%S
```

Keep CLI logging off by default unless actively debugging, so normal test output remains concise.

## Failure Investigation

When a local or CI test fails, inspect evidence in this order:

1. `reports/test.log` for test flow, runtime configuration, browser version, and failure URL.
2. `reports/report.html` for pytest-html failure details.
3. `screenshots/` for the browser state at failure.
4. GitHub Actions job logs for environment setup or dependency failures.

Use DEBUG logs when the failure appears related to matching elements, routes, counts, or test data. Keep INFO logs limited to the timeline a reviewer needs to understand the run quickly.

## CI and Artifacts

In GitHub Actions, logs already appear in the job output. If the framework writes `reports/test.log`, upload it with the existing report artifacts.

CI logging rules:

- Keep CI headless.
- Keep log files under `reports/`.
- Upload logs, HTML reports, and screenshots as artifacts.
- Never commit generated logs.
- Do not add email distribution unless recipients, retention, and secrets are explicitly defined.

## Audit Checklist

Before accepting logging changes, verify:

- Logs explain user-facing automation steps or useful failure context.
- Log level choices are intentional.
- No secrets or sensitive values are logged.
- No `print()` statements are introduced.
- Logs are generated under ignored runtime folders.
- CI artifact upload includes logs only when they exist.
- Assertions remain explicit and independent from log text.
