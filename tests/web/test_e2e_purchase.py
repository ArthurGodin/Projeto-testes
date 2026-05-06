import time
import pytest
from .pages.login_page import LoginPage
from .pages.inventory_page import InventoryPage
from .pages.cart_page import CartPage
from .pages.checkout_page import CheckoutPage

pytestmark = pytest.mark.web


class TestCompletePurchase:

    def test_full_purchase_flow(self, driver):
        LoginPage(driver).open().login("standard_user", "secret_sauce")

        inventory = InventoryPage(driver)
        assert inventory.get_title() == "Products"

        inventory.add_backpack_to_cart()
        inventory.add_bike_light_to_cart()
        assert inventory.get_cart_count() == "2"

        inventory.go_to_cart()
        time.sleep(1)

        cart = CartPage(driver)
        items = cart.get_item_names()
        assert "Sauce Labs Backpack" in items
        assert "Sauce Labs Bike Light" in items

        cart.checkout()
        time.sleep(1)

        checkout = CheckoutPage(driver)
        checkout.fill_info("Arthur", "Godinho", "64000")
        assert "Total:" in checkout.get_total()

        checkout.finish()
        assert checkout.get_complete_header() == "Thank you for your order!"


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
