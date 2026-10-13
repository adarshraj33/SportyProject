"""Fixtures for the desktop Chrome browser session."""

from __future__ import annotations

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tests.utils.settings import Settings


@pytest.fixture
def driver(settings: Settings):
    """Start one desktop-sized Chrome session for a UI test."""
    options = Options()
    options.add_argument("--window-size=1440,1000")
    if settings.headless:
        options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)
    yield browser
    browser.quit()
