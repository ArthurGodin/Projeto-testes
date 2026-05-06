from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    URL = "https://www.saucedemo.com/"

    def open(self):
        self.driver.get(self.URL)
        return self

    def login(self, username, password):
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        return self

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)
