from html import escape
from time import monotonic

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from test_data.routes import ROUTES


def xpath_literal(value: str) -> str:
    if '"' not in value:
        return f'"{value}"'
    if "'" not in value:
        return f"'{value}'"
    parts = value.split('"')
    return "concat(" + ', "\\\"", '.join(f'"{part}"' for part in parts) + ")"


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

    def open_fresh_todomvc(self):
        self.driver.get(f"{BASE_URL}{ROUTES['all']}")
        self.driver.execute_script("localStorage.clear();")
        self.driver.refresh()
        self.wait.until(EC.url_to_be(f"{BASE_URL}{ROUTES['all']}"))
        self.new_todo_input
        self.pause_for_observation()

    def pause_for_observation(self):
        if self.action_delay <= 0:
            return

        deadline = monotonic() + self.action_delay
        try:
            WebDriverWait(self.driver, self.action_delay + 0.5, poll_frequency=0.1).until(
                lambda _: monotonic() >= deadline
            )
        except TimeoutException:
            return

    def todo_item(self, item_text: str):
        text = xpath_literal(item_text)
        locator = (
            By.XPATH,
            "//*[@data-testid='todo-item'][.//*[@data-testid='todo-title' "
            f"and normalize-space()={text}]]",
        )
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible_todo_item(self, item_text: str):
        text = xpath_literal(item_text)
        locator = (
            By.XPATH,
            "//*[@data-testid='todo-item'][.//*[@data-testid='todo-title' "
            f"and normalize-space()={text}]]",
        )
        return self.wait.until(EC.visibility_of_element_located(locator))

    def todo_toggle(self, item_text: str):
        item = self.todo_item(item_text)
        return item.find_element(By.CSS_SELECTOR, 'input[aria-label="Toggle Todo"]')

    def filter_link(self, name: str):
        return self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, name)))

    def add_todo(self, item_text: str):
        input_box = self.new_todo_input
        input_box.clear()
        input_box.send_keys(item_text)
        self.pause_for_observation()
        input_box.send_keys(Keys.ENTER)
        self.wait.until(lambda _: self.new_todo_input.get_attribute("value") == "")
        self.visible_todo_item(item_text)
        self.pause_for_observation()

    def toggle_todo(self, item_text: str):
        toggle = self.todo_toggle(item_text)
        if not toggle.is_selected():
            toggle.click()
        self.wait.until(lambda _: self.todo_toggle(item_text).is_selected())
        self.pause_for_observation()

    def select_filter(self, name: str):
        self.filter_link(name).click()
        self.pause_for_observation()

    def assert_items_left(self, count: int):
        noun = "item left" if count == 1 else "items left"
        expected = f"{count} {noun}"
        self.wait.until(lambda _: self.todo_count.text == expected)

    def assert_total_items(self, count: int):
        self.wait.until(lambda _: len(self.todo_items) == count)

    def assert_selected_filter(self, name: str, route: str):
        self.wait.until(EC.url_to_be(f"{BASE_URL}{route}"))
        classes = self.filter_link(name).get_attribute("class") or ""
        assert "selected" in classes.split(), f"Expected {escape(name)} filter to be selected, got classes: {classes}"

    def assert_item_completed(self, item_text: str):
        classes = self.todo_item(item_text).get_attribute("class") or ""
        assert "completed" in classes.split(), f"Expected todo '{item_text}' to be completed, got classes: {classes}"

    def assert_item_not_completed(self, item_text: str):
        classes = self.todo_item(item_text).get_attribute("class") or ""
        assert "completed" not in classes.split(), f"Expected todo '{item_text}' to be active, got classes: {classes}"

    def assert_toggle_checked(self, item_text: str, checked: bool = True):
        assert self.todo_toggle(item_text).is_selected() is checked

    def assert_item_not_present(self, item_text: str):
        text = xpath_literal(item_text)
        locator = (
            By.XPATH,
            "//*[@data-testid='todo-item'][.//*[@data-testid='todo-title' "
            f"and normalize-space()={text}]]",
        )
        self.wait.until(lambda _: len(self.driver.find_elements(*locator)) == 0)
