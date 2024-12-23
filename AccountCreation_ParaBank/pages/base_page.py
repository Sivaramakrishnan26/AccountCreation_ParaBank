from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def find_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def click_element(self, locator, timeout=10):
        element = self.find_element_clickable(locator, timeout)
        element.click()

    def enter_text(self, locator, text, timeout=10):
        element = self.find_element(locator, timeout)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACK_SPACE)
        element.send_keys(text)

    def find_elements(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def get_current_url(self):
        return self.driver.current_url()
