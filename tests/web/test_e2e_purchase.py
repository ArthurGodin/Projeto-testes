import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .pages.login_page import LoginPage
from .pages.inventory_page import InventoryPage

pytestmark = pytest.mark.web


def _reliable_click(driver, by, value, expected_url_fragment, timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            el = driver.find_element(by, value)
            el.click()
        except Exception:
            pass
        try:
            WebDriverWait(driver, 2).until(EC.url_contains(expected_url_fragment))
            return
        except Exception:
            pass
    raise TimeoutError(
        f"Click on ({by}, {value}) did not navigate to '{expected_url_fragment}'. "
        f"Current URL: {driver.current_url}. "
        f"Page source snippet: {driver.page_source[:500]}"
    )


class TestCompletePurchase:

    def test_full_purchase_flow(self, driver):
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait = WebDriverWait(driver, 20)
        wait.until(EC.url_contains("inventory"))

        wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1"))

        _reliable_click(driver, By.CLASS_NAME, "shopping_cart_link", "cart")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

        assert driver.find_element(By.CLASS_NAME, "inventory_item_name").text == "Sauce Labs Backpack"

        _reliable_click(driver, By.ID, "checkout", "checkout-step-one")
        wait.until(EC.presence_of_element_located((By.ID, "first-name")))

        driver.find_element(By.ID, "first-name").send_keys("Arthur")
        driver.find_element(By.ID, "last-name").send_keys("Godinho")
        driver.find_element(By.ID, "postal-code").send_keys("64000")

        _reliable_click(driver, By.ID, "continue", "checkout-step-two")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))

        total = driver.find_element(By.CLASS_NAME, "summary_total_label").text
        assert "Total:" in total

        _reliable_click(driver, By.ID, "finish", "checkout-complete")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))

        assert driver.find_element(By.CLASS_NAME, "complete-header").text == "Thank you for your order!"


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
