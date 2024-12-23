import pytest
from selenium import webdriver
import time
import os

SCREENSHOT_DIRECTORY = "Screenshots"


@pytest.fixture(scope="function")
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://parabank.parasoft.com/parabank/index.htm")
    request.cls.driver = driver
    yield driver
    driver.quit()


def pytest_runtest_makereport(item, call):
    if call.when == 'call' and call.excinfo is not None:
        if not os.path.exists(SCREENSHOT_DIRECTORY):
            os.makedirs(SCREENSHOT_DIRECTORY)
        driver = item.funcargs['setup']
        if driver:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = os.path.join(SCREENSHOT_DIRECTORY, f"Screenshot-{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            print("Screenshot Saved Successfully")
        else:
            print("Driver instance not found")
