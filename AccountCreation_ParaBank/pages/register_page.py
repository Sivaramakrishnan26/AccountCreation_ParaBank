from selenium.webdriver.common.by import By
from .base_page import BasePage


class RegisterPage(BasePage):
    Register_Page = (By.XPATH, "//a[text()='Register']")
    First_Name = (By.XPATH, "//input[@name='customer.firstName']")
    Last_Name = (By.XPATH, "//input[@name='customer.lastName']")
    Street = (By.XPATH, "//input[@name='customer.address.street']")
    City = (By.XPATH, "//input[@name='customer.address.city']")
    State = (By.XPATH, "//input[@name='customer.address.state']")
    ZipCode = (By.XPATH, "//input[@name='customer.address.zipCode']")
    Phone = (By.XPATH, "//input[@name='customer.phoneNumber']")
    SSN = (By.XPATH, "//input[@name='customer.ssn']")
    UserName = (By.XPATH, "//input[@name='customer.username']")
    Password = (By.XPATH, "//input[@name='customer.password']")
    Confirm_Password = (By.XPATH, "//input[@name='repeatedPassword']")
    Register = (By.XPATH, "//input[@value='Register']")
    Error_Message = (By.XPATH, "//span[@class='error']")
    Logout = (By.XPATH, "//a[text()='Log Out']")

    def register(self, first_name, last_name, street, city, state, zipcode, phone, ssn, username, password,confirm_password):
        self.click_element(self.Register_Page)
        self.enter_text(self.First_Name, first_name)
        self.enter_text(self.Last_Name, last_name)
        self.enter_text(self.Street, street)
        self.enter_text(self.City, city)
        self.enter_text(self.State, state)
        self.enter_text(self.ZipCode, zipcode)
        self.enter_text(self.Phone, phone)
        self.enter_text(self.SSN, ssn)
        self.enter_text(self.UserName, username)
        self.enter_text(self.Password, password)
        self.enter_text(self.Confirm_Password, confirm_password)
        self.click_element(self.Register)

        try:
            assert "Your account was created successfully. You are now logged in." in self.driver.page_source
            print("Registered Successfully")
        except AssertionError as e:
            print(f"Error Occurred: {e}")
            error_message = self.find_element(self.Error_Message)
            print(f"Error Message: {error_message.text}")
