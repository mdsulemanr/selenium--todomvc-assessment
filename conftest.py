import logging
import os
import platform
import re
import sys
from pathlib import Path

import pytest
from pytest_html import extras
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.settings import ACTION_DELAY, BASE_URL, DEFAULT_TIMEOUT, HEADLESS
from pages.todo_page import TodoPage

try:
    import allure
except ImportError:
    allure = None


logger = logging.getLogger(__name__)

SUPPORTED_BROWSERS = ("chrome", "firefox", "edge")
VIEWPORTS = {
    "desktop": (1280, 720),
    "mobile": (390, 844),
}


def _csv_option(value, allowed_values, option_name):
    selected = [item.strip().lower() for item in value.split(",") if item.strip()]
    if not selected:
        raise pytest.UsageError(f"{option_name} requires at least one value.")

    invalid = sorted(set(selected) - set(allowed_values))
    if invalid:
        allowed = ", ".join(allowed_values)
        raise pytest.UsageError(f"Unsupported {option_name} value(s): {', '.join(invalid)}. Use: {allowed}")

    return selected


def _edge_binary_location():
    candidates = []
    for root in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")):
        if not root:
            continue
        root_path = Path(root)
        candidates.append(root_path / "Microsoft" / "Edge" / "Application" / "msedge.exe")
        edge_core = root_path / "Microsoft" / "EdgeCore"
        if edge_core.exists():
            candidates.extend(sorted(edge_core.glob("*/msedge.exe"), reverse=True))

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)

    return None


def _browser_options(browser_name, headless, viewport_name):
    width, height = VIEWPORTS[viewport_name]

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={width},{height}")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        return options

    if browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        return options

    options = EdgeOptions()
    edge_binary = _edge_binary_location()
    if edge_binary:
        options.binary_location = edge_binary
    if headless:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    return options


def _start_browser(browser_name, options, remote_url):
    if remote_url:
        return webdriver.Remote(command_executor=remote_url, options=options)

    if browser_name == "chrome":
        return webdriver.Chrome(options=options)

    if browser_name == "firefox":
        return webdriver.Firefox(options=options)

    return webdriver.Edge(options=options)


def _safe_artifact_name(nodeid):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid).strip("_")


def _allure_results_dir(config):
    return getattr(config.option, "allure_report_dir", None)


def _write_allure_environment(config):
    allure_dir = _allure_results_dir(config)
    if not allure_dir:
        return

    results_dir = Path(allure_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    remote_url = config.getoption("remote_url")
    environment = {
        "Base URL": BASE_URL,
        "Browser Option": config.getoption("browser"),
        "Viewport Option": config.getoption("viewport"),
        "Execution Mode": "Selenium Grid" if remote_url else "Local WebDriver",
        "Remote URL": remote_url or "not configured",
        "Headless": str(False if config.getoption("headed") else HEADLESS),
        "Python": sys.version.split()[0],
        "Platform": platform.platform(),
    }
    lines = [f"{key}={value}" for key, value in environment.items()]
    (results_dir / "environment.properties").write_text("\n".join(lines), encoding="utf-8")


@pytest.fixture
def driver(request, browser_name, viewport_name):
    headless = False if request.config.getoption("headed") else HEADLESS
    action_delay = request.config.getoption("action_delay")
    remote_url = request.config.getoption("remote_url")
    if action_delay is None:
        action_delay = ACTION_DELAY

    options = _browser_options(browser_name, headless, viewport_name)
    width, height = VIEWPORTS[viewport_name]

    logger.info(
        "Starting %s browser; viewport=%s; remote=%s; headless=%s; action_delay=%.2f",
        browser_name,
        viewport_name,
        bool(remote_url),
        headless,
        action_delay,
    )
    logger.debug("Target base URL: %s", BASE_URL)
    browser = _start_browser(browser_name, options, remote_url)
    browser.set_page_load_timeout(DEFAULT_TIMEOUT)
    browser.set_script_timeout(DEFAULT_TIMEOUT)
    browser.set_window_size(width, height)
    capabilities = browser.capabilities
    logger.info(
        "Started browser session; browser=%s; version=%s",
        capabilities.get("browserName"),
        capabilities.get("browserVersion"),
    )
    try:
        yield browser
    finally:
        logger.info("Closing %s browser", browser_name)
        browser.quit()


@pytest.fixture
def todo_page(driver, request):
    action_delay = request.config.getoption("action_delay")
    if action_delay is None:
        action_delay = ACTION_DELAY

    return TodoPage(driver, action_delay=action_delay)


@pytest.fixture
def browser_name(request):
    return request.param


@pytest.fixture
def viewport_name(request):
    return request.param


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browsers visibly instead of using the configured headless mode.",
    )
    parser.addoption(
        "--action-delay",
        type=float,
        default=None,
        help="Seconds to pause after visible page actions for observation.",
    )
    parser.addoption(
        "--browser",
        default="chrome",
        help="Comma-separated browser list: chrome, firefox, edge. Default: chrome.",
    )
    parser.addoption(
        "--viewport",
        default="desktop",
        help="Comma-separated viewport list: desktop, mobile. Default: desktop.",
    )
    parser.addoption(
        "--remote-url",
        default=None,
        help="Selenium Grid URL, for example http://localhost:4444. Omit for local browsers.",
    )


def pytest_generate_tests(metafunc):
    if "browser_name" in metafunc.fixturenames:
        browsers = _csv_option(metafunc.config.getoption("browser"), SUPPORTED_BROWSERS, "--browser")
        metafunc.parametrize("browser_name", browsers, indirect=True)

    if "viewport_name" in metafunc.fixturenames:
        viewports = _csv_option(metafunc.config.getoption("viewport"), VIEWPORTS.keys(), "--viewport")
        metafunc.parametrize("viewport_name", viewports, indirect=True)


def pytest_html_report_title(report):
    report.title = "Selenium TodoMVC Assessment Report"


def pytest_configure(config):
    _write_allure_environment(config)


def pytest_runtest_setup(item):
    markers = sorted(marker.name for marker in item.iter_markers())
    marker_text = ", ".join(markers) if markers else "none"
    logger.info("Starting test: %s; markers=%s", item.nodeid, marker_text)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        logger.info("Finished test: %s; outcome=%s", item.nodeid, report.outcome)

    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    logger.error("Test failed: %s", item.nodeid)
    logger.error("Failure URL: %s", browser.current_url)

    screenshot_png = browser.get_screenshot_as_png()
    screenshot_dir = Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    screenshot_path = screenshot_dir / f"{_safe_artifact_name(item.nodeid)}.png"
    screenshot_path.write_bytes(screenshot_png)
    logger.info("Saved failure screenshot: %s", screenshot_path)

    report.extras = getattr(report, "extras", [])
    report.extras.append(extras.image(str(screenshot_path)))

    if allure is not None and _allure_results_dir(item.config):
        allure.attach(
            screenshot_png,
            name="failure screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
