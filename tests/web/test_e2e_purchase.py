import os
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .pages.login_page import PaginaLogin
from .pages.inventory_page import PaginaInventario

pytestmark = pytest.mark.web

LENTO = not os.environ.get("CI")
ATRASO = 1.5 if LENTO else 0


def _destacar(driver, seletor_css):
    if not LENTO:
        return
    driver.execute_script(f"""
        var el = document.querySelector('{seletor_css}');
        if (el) {{
            el.style.outline = '3px solid red';
            el.style.outlineOffset = '2px';
        }}
    """)
    time.sleep(ATRASO)


def _clique_js(driver, seletor_css, proximo_localizador, timeout=20):
    espera = WebDriverWait(driver, timeout)
    espera.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, seletor_css)
    ))
    _destacar(driver, seletor_css)

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            elemento = driver.find_element(By.CSS_SELECTOR, seletor_css)
            elemento.click()
        except Exception:
            pass
        try:
            driver.execute_script(f"""
                var el = document.querySelector('{seletor_css}');
                if (el) el.dispatchEvent(new MouseEvent('click', {{bubbles: true, cancelable: true}}));
            """)
        except Exception:
            pass
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located(proximo_localizador))
            if LENTO:
                time.sleep(0.5)
            return
        except Exception:
            pass
    raise TimeoutError(f"Falha ao navegar após clicar em {seletor_css}")


class TestCompraCompleta:

    @pytest.mark.flaky(reruns=3)
    def test_fluxo_compra_completo(self, driver):
        driver.get("https://www.saucedemo.com/")
        if LENTO:
            time.sleep(ATRASO)

        _destacar(driver, "#user-name")
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        _destacar(driver, "#password")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        _destacar(driver, "#login-button")
        driver.find_element(By.ID, "login-button").click()

        espera = WebDriverWait(driver, 20)
        espera.until(EC.url_contains("inventory"))
        if LENTO:
            time.sleep(ATRASO)

        _clique_js(driver, "#add-to-cart-sauce-labs-backpack", (By.CLASS_NAME, "shopping_cart_badge"))

        _clique_js(driver, ".shopping_cart_link", (By.CLASS_NAME, "cart_item"))
        assert driver.find_element(By.CLASS_NAME, "inventory_item_name").text == "Sauce Labs Backpack"
        if LENTO:
            time.sleep(ATRASO)

        _clique_js(driver, "#checkout", (By.ID, "first-name"))

        _destacar(driver, "#first-name")
        driver.find_element(By.ID, "first-name").send_keys("Arthur")
        _destacar(driver, "#last-name")
        driver.find_element(By.ID, "last-name").send_keys("Godinho")
        _destacar(driver, "#postal-code")
        campo_cep = driver.find_element(By.ID, "postal-code")
        campo_cep.send_keys("64000")
        campo_cep.send_keys(Keys.ENTER)
        espera.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))

        total = driver.find_element(By.CLASS_NAME, "summary_total_label").text
        assert "Total:" in total
        if LENTO:
            time.sleep(ATRASO)

        _clique_js(driver, "#finish", (By.CLASS_NAME, "complete-header"))
        assert driver.find_element(By.CLASS_NAME, "complete-header").text == "Thank you for your order!"
        if LENTO:
            time.sleep(2)


class TestLogin:

    def test_login_sucesso(self, driver):
        PaginaLogin(driver).abrir().fazer_login("standard_user", "secret_sauce")
        assert PaginaInventario(driver).obter_titulo() == "Products"

    def test_usuario_bloqueado(self, driver):
        pagina = PaginaLogin(driver).abrir()
        pagina.fazer_login("locked_out_user", "secret_sauce")
        assert "locked out" in pagina.obter_mensagem_erro().lower()

    def test_credenciais_invalidas(self, driver):
        pagina = PaginaLogin(driver).abrir()
        pagina.fazer_login("invalid_user", "wrong_pass")
        assert "Username and password do not match" in pagina.obter_mensagem_erro()
