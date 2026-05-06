import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestDebugCI:

    def test_debug_click_methods(self, driver):
        driver.get("https://www.saucedemo.com/")
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains("inventory"))

        print(f"\n=== DEBUG INFO ===")
        print(f"Browser: {driver.capabilities.get('browserName', 'unknown')}")
        print(f"Version: {driver.capabilities.get('browserVersion', 'unknown')}")
        print(f"Platform: {driver.capabilities.get('platformName', 'unknown')}")
        print(f"URL after login: {driver.current_url}")
        print(f"Window size: {driver.get_window_size()}")

        add_btn = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        print(f"\nAdd to cart button - tag: {add_btn.tag_name}, displayed: {add_btn.is_displayed()}, enabled: {add_btn.is_enabled()}")
        add_btn.click()
        time.sleep(1)

        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        print(f"Badge text after add: '{badge.text}'")

        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        print(f"\nCart link - tag: {cart_link.tag_name}, href: {cart_link.get_attribute('href')}")
        print(f"Cart link - displayed: {cart_link.is_displayed()}, enabled: {cart_link.is_enabled()}")
        print(f"Cart link - location: {cart_link.location}, size: {cart_link.size}")

        print(f"\n--- Attempt 1: element.click() ---")
        print(f"URL before: {driver.current_url}")
        cart_link.click()
        time.sleep(2)
        print(f"URL after: {driver.current_url}")

        if "cart" in driver.current_url:
            print("SUCCESS: Native click worked!")
            return

        print("FAILED: Native click did not navigate")

        print(f"\n--- Attempt 2: JS click ---")
        driver.execute_script("arguments[0].click();", cart_link)
        time.sleep(2)
        print(f"URL after JS click: {driver.current_url}")

        if "cart" in driver.current_url:
            print("SUCCESS: JS click worked!")
            return

        print("FAILED: JS click did not navigate")

        print(f"\n--- Attempt 3: JS window.location ---")
        driver.execute_script("window.location.href = arguments[0].href;", cart_link)
        time.sleep(2)
        print(f"URL after location change: {driver.current_url}")

        if "cart" in driver.current_url:
            print("SUCCESS: JS location worked!")
            return

        print("FAILED: JS location did not navigate")

        print(f"\n--- Attempt 4: Direct URL ---")
        driver.get("https://www.saucedemo.com/cart.html")
        time.sleep(2)
        print(f"URL after driver.get: {driver.current_url}")
        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        print(f"Cart items found: {len(items)}")

        assert False, "Debug test - check output above"
