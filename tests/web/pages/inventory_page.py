from selenium.webdriver.common.by import By
from .base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def get_title(self):
        return self.get_text(self.TITLE)

    def add_backpack_to_cart(self):
        self.click(self.ADD_BACKPACK)
        return self

    def get_cart_count(self):
        return self.get_text(self.CART_BADGE)

    def go_to_cart(self):
        self.driver.get("https://www.saucedemo.com/cart.html")
        return self
