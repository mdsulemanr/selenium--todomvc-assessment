from pathlib import Path

import pytest
from pytest_html import extras
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.settings import ACTION_DELAY, HEADLESS
from pages.todo_page import TodoPage


@pytest.fixture
def driver(request):
    headless = False if request.config.getoption("headed") else HEADLESS

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,720")

    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


@pytest.fixture
def todo_page(driver, request):
    action_delay = request.config.getoption("action_delay")
    if action_delay is None:
        action_delay = ACTION_DELAY

    return TodoPage(driver, action_delay=action_delay)


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run Chrome visibly instead of using the configured headless mode.",
    )
    parser.addoption(
        "--action-delay",
        type=float,
        default=None,
        help="Seconds to pause after visible page actions for observation.",
    )


def pytest_html_report_title(report):
    report.title = "Selenium TodoMVC Assessment Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    screenshot_dir = Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    screenshot_path = screenshot_dir / f"{item.name}.png"
    browser.save_screenshot(str(screenshot_path))

    report.extras = getattr(report, "extras", [])
    report.extras.append(extras.image(str(screenshot_path)))
