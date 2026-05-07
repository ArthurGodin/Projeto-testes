import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .pages.login_page import LoginPage
from .pages.inventory_page import InventoryPage

pytestmark = pytest.mark.web


def _js_click(driver, css_selector, next_locator, timeout=20):
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, css_selector)
    ))
    driver.execute_script(f"""
        var el = document.querySelector('{css_selector}');
        el.dispatchEvent(new MouseEvent('click', {{bubbles: true, cancelable: true}}));
    """)
    wait.until(EC.presence_of_element_located(next_locator))


class TestCompletePurchase:

    @pytest.mark.flaky(reruns=3)
    def test_full_purchase_flow(self, driver):
        driver.get("https://www.saucedemo.com/")
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait = WebDriverWait(driver, 20)
        wait.until(EC.url_contains("inventory"))

        _js_click(driver, "#add-to-cart-sauce-labs-backpack", (By.CLASS_NAME, "shopping_cart_badge"))

        _js_click(driver, ".shopping_cart_link", (By.CLASS_NAME, "cart_item"))
        assert driver.find_element(By.CLASS_NAME, "inventory_item_name").text == "Sauce Labs Backpack"

        _js_click(driver, "#checkout", (By.ID, "first-name"))

        driver.find_element(By.ID, "first-name").send_keys("Arthur")
        driver.find_element(By.ID, "last-name").send_keys("Godinho")
        driver.find_element(By.ID, "postal-code").send_keys("64000")

        _js_click(driver, "#continue", (By.CLASS_NAME, "summary_total_label"))

        total = driver.find_element(By.CLASS_NAME, "summary_total_label").text
        assert "Total:" in total

        _js_click(driver, "#finish", (By.CLASS_NAME, "complete-header"))
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
