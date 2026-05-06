from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):
    CHECKOUT_BTN = (By.ID, "checkout")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def get_cart_items(self):
        return self.driver.find_elements(*self.CART_ITEMS)

    def get_item_names(self):
        elements = self.driver.find_elements(*self.ITEM_NAME)
        return [el.text for el in elements]

    def checkout(self):
        self.click(self.CHECKOUT_BTN)
        return self
