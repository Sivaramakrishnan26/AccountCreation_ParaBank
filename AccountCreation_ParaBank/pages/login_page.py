from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    UserName = (By.NAME, "username")
    Password = (By.NAME, "password")
    LogIn = (By.XPATH, "//input[@value='Log In']")
    Error_Message = (By.CLASS_NAME, "error")

    def login(self, username, password):
        self.enter_text(self.UserName, username)
        self.enter_text(self.Password, password)
        self.click_element(self.LogIn)

        try:
            assert "overview.htm" in self.driver.current_url
            print("Login Successful")
        except AssertionError as e:
            print(f"Error Occurred: {e}")
            error_message = self.find_element(self.Error_Message)
            print(f"Error Message: {error_message.text}")
