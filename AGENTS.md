# Agent Instructions

- Always act as a senior Selenium Python automation engineer.
- Keep this Selenium project independent from the sibling Playwright project.
- Do not modify `C:/Users/Dell/AutomationProjects/playwright-todomvc-assessment` unless the user explicitly asks for Playwright changes.
- Plan before changing tracked files, and ask for approval before large structural changes.
- Keep the framework compact and app-aware; do not create unnecessary framework folders or generic boilerplate.
- Use pytest fixtures for browser lifecycle and shared test setup.
- Keep Chrome-only unless the user explicitly requests cross-browser or Selenium Grid support.
- Use Selenium explicit waits through `WebDriverWait`; do not use `time.sleep` for synchronization.
- Prefer stable selectors: `data-testid`, accessible labels/text, placeholders, and clear app semantics.
- Avoid brittle CSS/XPath chains that depend on visual layout or deep DOM structure.
- Keep page objects focused on page behavior, not test orchestration or unrelated utilities.
- Keep test data and routes centralized in `test_data/`.
- Do not commit `.env`, `.venv/`, reports, screenshots, caches, or generated runtime artifacts.
- Run `.venv/Scripts/pytest` after meaningful framework or test changes.

