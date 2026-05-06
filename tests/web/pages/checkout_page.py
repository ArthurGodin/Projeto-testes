from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    def fill_info(self, first_name, last_name, postal_code):
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)
        self.find(self.CONTINUE_BTN)
        self.driver.find_element(*self.CONTINUE_BTN).click()
        return self

    def get_total(self):
        return self.get_text(self.SUMMARY_TOTAL)

    def finish(self):
        self.find(self.FINISH_BTN)
        self.driver.find_element(*self.FINISH_BTN).click()
        return self

    def get_complete_header(self):
        return self.get_text(self.COMPLETE_HEADER)
