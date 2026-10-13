"""Small base class shared by page objects."""

from __future__ import annotations

from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout: int = 12) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def click(self, locator) -> None:
        self.wait.until(conditions.element_to_be_clickable(locator)).click()

    def fill(self, locator, value: str) -> None:
        field = self.wait.until(conditions.visibility_of_element_located(locator))
        field.clear()
        field.send_keys(value)

    def text(self, locator) -> str:
        return self.wait.until(conditions.visibility_of_element_located(locator)).text
