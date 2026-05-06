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
        assert inventory.get_cart_count() == "1"

        inventory.go_to_cart()
        inventory.wait_for_url("cart")

        cart = CartPage(driver)
        assert "Sauce Labs Backpack" in cart.get_item_names()

        cart.checkout()
        cart.wait_for_url("checkout-step-one")

        checkout = CheckoutPage(driver)
        checkout.fill_info("Arthur", "Godinho", "64000")
        checkout.wait_for_url("checkout-step-two")
        assert "Total:" in checkout.get_total()

        checkout.finish()
        checkout.wait_for_url("checkout-complete")
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
