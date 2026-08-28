---
name: selenium-todomvc-assessment
description: Maintain and extend the Selenium Python TodoMVC assessment framework, including pytest fixtures, page objects, explicit-wait Selenium interactions, local HTML reporting, and Chrome-only test execution. Use only for this Selenium TodoMVC project, not for the sibling Playwright implementation.
---

# Selenium TodoMVC Assessment Skill

Use this skill when working in this repository or when the user asks to maintain, review, or extend the Selenium Python TodoMVC assessment framework.

## Project Intent

This project is a Selenium + Python migration of the sibling Playwright TodoMVC assessment. Preserve behavioral parity with the Playwright tests while keeping this repository independent.

Current scope:

- Chrome-only browser execution.
- pytest as the test runner.
- pytest-html for local reports.
- Selenium Manager for Chrome driver resolution.
- TodoMVC hosted at `https://demo.playwright.dev` by default.

## Engineering Rules

- Keep the framework small and app-aware.
- Use pytest fixtures in `conftest.py` for browser lifecycle.
- Use page objects for TodoMVC-specific behavior and assertions.
- Use centralized routes and test data from `test_data/`.
- Read environment values through `config/settings.py`.
- Use Selenium explicit waits; do not add fixed sleeps.
- Prefer stable selectors such as `data-testid`, accessible labels, link text, and placeholders.
- Avoid deep DOM selectors, index-based selectors, visual-layout selectors, and broad generic abstractions.
- Do not add cross-browser, Selenium Grid, CI, or reporting integrations unless the user requests them.
- Do not modify the sibling Playwright repository unless explicitly requested.

## Expected Workflow

Before changing files, inspect the relevant test, page object, fixture, or config file. Keep edits scoped to the requested behavior.

After meaningful changes, run:

```powershell
.venv\Scripts\pytest
```

The default report is generated at:

```text
reports/report.html
```

Failure screenshots are saved in `screenshots/` and attached to the HTML report.

## Acceptance Standards

A completed change should:

- Preserve or improve readability of the pytest specs.
- Keep browser setup centralized in fixtures.
- Avoid duplicated route strings and test data literals.
- Pass the Selenium test suite locally.
- Leave ignored runtime artifacts untracked.
