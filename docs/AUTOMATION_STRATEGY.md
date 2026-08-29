# Selenium TodoMVC Automation Strategy

## Vision

This project is a compact Selenium Python assessment suite for TodoMVC. The framework should stay app-aware, readable, and easy to audit. Every addition should improve confidence in TodoMVC behavior without turning the project into a generic automation framework.

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
.venv\Scripts\pytest
```

Headed run:

```powershell
.venv\Scripts\pytest --headed
```

Headed slow-motion run:

```powershell
.venv\Scripts\pytest --headed --action-delay=2
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
- Chrome-only scope is preserved unless cross-browser support is explicitly requested.
- `.env`, `.venv/`, reports, screenshots, caches, and generated artifacts remain untracked.
- `.venv\Scripts\pytest` passes after meaningful changes.

## Anti-Patterns

Avoid adding:

- Generic base-page layers without a clear current need.
- Selenium Grid, browser matrices, or CI wiring without a user request.
- Broad helper libraries that hide simple TodoMVC behavior.
- Assertions that depend on layout rather than behavior or state.
- Slow-motion delays as reliability fixes.
- Changes to the sibling Playwright project.
