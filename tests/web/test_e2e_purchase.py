import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .pages.login_page import LoginPage
from .pages.inventory_page import InventoryPage

pytestmark = pytest.mark.web


class TestCompletePurchase:

    def test_full_purchase_flow(self, driver):
        driver.get("https://www.saucedemo.com/")
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        assert driver.find_element(By.CLASS_NAME, "title").text == "Products"

        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        time.sleep(0.5)
        assert driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "1"

        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        wait.until(EC.url_contains("cart"))

        item = driver.find_element(By.CLASS_NAME, "inventory_item_name")
        assert item.text == "Sauce Labs Backpack"

        driver.find_element(By.ID, "checkout").click()
        wait.until(EC.url_contains("checkout-step-one"))

        driver.find_element(By.ID, "first-name").send_keys("Arthur")
        driver.find_element(By.ID, "last-name").send_keys("Godinho")
        driver.find_element(By.ID, "postal-code").send_keys("64000")
        driver.find_element(By.ID, "continue").click()
        wait.until(EC.url_contains("checkout-step-two"))

        total = driver.find_element(By.CLASS_NAME, "summary_total_label").text
        assert "Total:" in total

        driver.find_element(By.ID, "finish").click()
        wait.until(EC.url_contains("checkout-complete"))

        header = driver.find_element(By.CLASS_NAME, "complete-header").text
        assert header == "Thank you for your order!"


class TestLogin:

    def test_successful_login(self, driver):
        LoginPage(driver).open().login("standard_user", "secret_sauce")
        assert InventoryPage(driver).get_title() == "Products"

    def test_locked_user(self, driver):
        page = LoginPage(driver).open()
        page.login("locked_out_user", "secret_sauce")
        assert "locked out" in page.get_error_message().lower()

    def test_invalid_credentials(self, driver):
        page = LoginPage(driver).open()
        page.login("invalid_user", "wrong_pass")
        assert "Username and password do not match" in page.get_error_message()
