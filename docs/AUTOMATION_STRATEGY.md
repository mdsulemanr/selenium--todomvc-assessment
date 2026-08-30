# Selenium TodoMVC Automation Strategy

## Vision

This project is a compact Selenium Python assessment suite for TodoMVC with an enterprise-style execution layer. The framework should stay app-aware, readable, and easy to audit while supporting local browsers, Selenium Grid, browser/viewport matrices, and pytest-xdist parallelism.

The sibling Playwright project is intentionally independent. Do not share code, generated artifacts, or framework structure between the two repositories unless explicitly requested.

## Locator Strategy

Use the most stable, user-meaningful locator available. Prefer locators that describe app semantics rather than DOM layout.

Locator priority:

1. Unique `data-testid` values.
2. Accessible labels, roles, names, or visible control text.
3. Stable placeholders for form fields.
4. CSS selectors anchored on `data-testid` or clear semantic attributes.
5. Text matching within a stable parent collection.
6. XPath only when Selenium cannot express the relationship cleanly another way.

Avoid:

- Deep CSS chains tied to layout or nesting.
- Index-based selectors for repeated UI.
- XPath that depends on visual structure.
- Class names used only for styling unless they are the behavior under test.

## Synchronization

Use Selenium explicit waits through `WebDriverWait` for app state, navigation state, visibility, clickability, and DOM changes. Do not use fixed sleeps for synchronization.

`ACTION_DELAY` and `--action-delay` exist only for visual observation during debugging or demos. They must not be used to make a flaky test pass. If a test needs delay to pass, improve the explicit wait condition instead.

## Page Object Boundaries

Page objects should model TodoMVC behavior:

- Opening a fresh TodoMVC session.
- Adding todos.
- Completing todos.
- Selecting filters.
- Reading or asserting TodoMVC state.

Tests should describe user workflows and expected outcomes. Page objects should hide Selenium mechanics, but they should not become generic utility containers or orchestrate unrelated test scenarios.

## Test Data and Routes

Keep reusable routes and test data under `test_data/`.

Good defaults:

- Route fragments belong in `test_data/routes.py`.
- Todo labels and scenario data belong in `test_data/todos.py`.
- Tests may use local variables derived from centralized data for readability.

Avoid duplicating route strings or long-lived test labels directly inside tests when they are part of reusable scenarios.

## Debugging Workflow

Normal run:

```powershell
.\.venv\Scripts\python -m pytest
```

Headed run:

```powershell
.\.venv\Scripts\python -m pytest --headed
```

Headed slow-motion run:

```powershell
.\.venv\Scripts\python -m pytest --headed --action-delay=2
```

Browser and viewport profile runs:

```powershell
.\.venv\Scripts\python -m pytest --browser firefox
.\.venv\Scripts\python -m pytest --browser edge --viewport mobile
.\.venv\Scripts\python -m pytest --browser chrome,firefox,edge --viewport desktop,mobile
```

Parallel run:

```powershell
.\.venv\Scripts\python -m pytest -n auto
```

Selenium Grid run:

```powershell
.\scripts\start-grid.ps1
.\.venv\Scripts\python -m pytest -n 3 --remote-url http://localhost:4444 --browser chrome,firefox,edge
.\scripts\stop-grid.ps1
```

Use the pytest-html report for failures:

```text
reports/report.html
```

Failure screenshots are saved in `screenshots/` and attached to the report. These runtime artifacts must stay ignored by git.

## Audit Checklist

Before accepting a framework or test change, verify:

- The test still reflects an actual TodoMVC user behavior.
- Browser setup remains centralized in pytest fixtures.
- Selectors follow the locator priority hierarchy.
- Synchronization uses explicit waits, not fixed sleeps.
- Test data and routes remain centralized when reusable.
- Page objects expose behavior, not low-level test orchestration.
- Cross-browser and Grid runs use the centralized pytest fixture path.
- The default local run remains Chrome desktop for fast local feedback.
- `.env`, `.venv/`, reports, screenshots, caches, and generated artifacts remain untracked.
- `.venv\Scripts\pytest` passes after meaningful changes.

## Anti-Patterns

Avoid adding:

- Generic base-page layers without a clear current need.
- Selenium Grid or browser matrix abstractions outside the centralized pytest fixture path.
- Broad helper libraries that hide simple TodoMVC behavior.
- Assertions that depend on layout rather than behavior or state.
- Slow-motion delays as reliability fixes.
- Changes to the sibling Playwright project.
