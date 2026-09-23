import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    """Open Chrome for a test and close it afterwards."""

    browser = webdriver.Chrome()

    try:
        browser.maximize_window()
        yield browser

    finally:
        browser.quit()