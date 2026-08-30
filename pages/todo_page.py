import logging
from html import escape
from time import monotonic

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from test_data.routes import ROUTES

try:
    import allure
except ImportError:
    allure = None

logger = logging.getLogger(__name__)


def report_step(title):
    if allure is None:
        return lambda func: func

    return allure.step(title)


class TodoPage:
    def __init__(self, driver: WebDriver, action_delay: float = 0):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
        self.action_delay = action_delay

    @property
    def new_todo_input(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What needs to be done?"]'))
        )

    @property
    def todo_items(self):
        return self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="todo-item"]')

    @property
    def todo_count(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="todo-count"]')))

    def _matching_todo_item(self, item_text: str):
        items = self.todo_items
        logger.debug("Searching %d todo rows for matching title", len(items))
        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, '[data-testid="todo-title"]')
            except NoSuchElementException:
                continue

            if title.text.strip() == item_text:
                return item

        return False

    @report_step("Open a fresh TodoMVC session")
    def open_fresh_todomvc(self):
        url = f"{BASE_URL}{ROUTES['all']}"
        logger.info("Opening fresh TodoMVC session")
        logger.debug("Navigating to %s", url)
        self.driver.get(url)
        self.driver.execute_script("localStorage.clear();")
        self.driver.refresh()
        self.wait.until(EC.url_to_be(url))
        self.new_todo_input
        self.pause_for_observation()

    def pause_for_observation(self):
        if self.action_delay <= 0:
            return

        logger.debug("Pausing %.2f seconds for observation", self.action_delay)
        deadline = monotonic() + self.action_delay
        try:
            WebDriverWait(self.driver, self.action_delay + 0.5, poll_frequency=0.1).until(
                lambda _: monotonic() >= deadline
            )
        except TimeoutException:
            return

    def todo_item(self, item_text: str):
        return self.wait.until(lambda _: self._matching_todo_item(item_text))

    def visible_todo_item(self, item_text: str):
        def matching_visible_item(_):
            item = self._matching_todo_item(item_text)
            if item and item.is_displayed():
                return item
            return False

        return self.wait.until(matching_visible_item)

    def todo_toggle(self, item_text: str):
        item = self.todo_item(item_text)
        return item.find_element(By.CSS_SELECTOR, 'input[aria-label="Toggle Todo"]')

    def filter_link(self, name: str):
        return self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, name)))

    @report_step("Add todo: {item_text}")
    def add_todo(self, item_text: str):
        logger.info("Adding todo item")
        logger.debug("Todo text: %s", item_text)
        input_box = self.new_todo_input
        input_box.clear()
        input_box.send_keys(item_text)
        self.pause_for_observation()
        input_box.send_keys(Keys.ENTER)
        self.wait.until(lambda _: self.new_todo_input.get_attribute("value") == "")
        self.visible_todo_item(item_text)
        self.pause_for_observation()

    @report_step("Complete todo: {item_text}")
    def toggle_todo(self, item_text: str):
        logger.info("Completing todo item")
        logger.debug("Todo text: %s", item_text)
        toggle = self.todo_toggle(item_text)
        if not toggle.is_selected():
            toggle.click()
        self.wait.until(lambda _: self.todo_toggle(item_text).is_selected())
        self.pause_for_observation()

    @report_step("Select filter: {name}")
    def select_filter(self, name: str):
        logger.info("Selecting %s filter", name)
        self.filter_link(name).click()
        self.pause_for_observation()

    @report_step("Assert remaining todo counter is {count}")
    def assert_items_left(self, count: int):
        noun = "item left" if count == 1 else "items left"
        expected = f"{count} {noun}"
        logger.debug("Expecting todo count text: %s", expected)
        self.wait.until(lambda _: self.todo_count.text == expected)

    @report_step("Assert visible todo item count is {count}")
    def assert_total_items(self, count: int):
        logger.debug("Expecting total visible todo rows: %d", count)
        self.wait.until(lambda _: len(self.todo_items) == count)

    @report_step("Assert selected filter is {name}")
    def assert_selected_filter(self, name: str, route: str):
        logger.debug("Expecting %s filter route: %s", name, route)
        self.wait.until(EC.url_to_be(f"{BASE_URL}{route}"))
        classes = self.filter_link(name).get_attribute("class") or ""
        assert "selected" in classes.split(), f"Expected {escape(name)} filter to be selected, got classes: {classes}"

    @report_step("Assert todo is completed: {item_text}")
    def assert_item_completed(self, item_text: str):
        classes = self.todo_item(item_text).get_attribute("class") or ""
        assert "completed" in classes.split(), f"Expected todo '{item_text}' to be completed, got classes: {classes}"

    @report_step("Assert todo is active: {item_text}")
    def assert_item_not_completed(self, item_text: str):
        classes = self.todo_item(item_text).get_attribute("class") or ""
        assert "completed" not in classes.split(), f"Expected todo '{item_text}' to be active, got classes: {classes}"

    @report_step("Assert todo checkbox state for {item_text}")
    def assert_toggle_checked(self, item_text: str, checked: bool = True):
        assert self.todo_toggle(item_text).is_selected() is checked

    @report_step("Assert todo is not visible: {item_text}")
    def assert_item_not_present(self, item_text: str):
        self.wait.until(lambda _: self._matching_todo_item(item_text) is False)
