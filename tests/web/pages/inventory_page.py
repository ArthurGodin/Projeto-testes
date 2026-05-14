from selenium.webdriver.common.by import By
from .base_page import PaginaBase


class PaginaInventario(PaginaBase):
    TITULO = (By.CLASS_NAME, "title")
    ADICIONAR_MOCHILA = (By.ID, "add-to-cart-sauce-labs-backpack")
    BADGE_CARRINHO = (By.CLASS_NAME, "shopping_cart_badge")

    def obter_titulo(self):
        return self.obter_texto(self.TITULO)

    def adicionar_mochila_ao_carrinho(self):
        self.clicar(self.ADICIONAR_MOCHILA)
        return self

    def obter_quantidade_carrinho(self):
        return self.obter_texto(self.BADGE_CARRINHO)

    def ir_para_carrinho(self):
        self.driver.get("https://www.saucedemo.com/cart.html")
        return self
