from selenium.webdriver.common.by import By
from .base_page import PaginaBase


class PaginaCarrinho(PaginaBase):
    BOTAO_CHECKOUT = (By.ID, "checkout")
    ITENS_CARRINHO = (By.CLASS_NAME, "cart_item")
    NOME_ITEM = (By.CLASS_NAME, "inventory_item_name")

    def obter_itens_carrinho(self):
        return self.driver.find_elements(*self.ITENS_CARRINHO)

    def obter_nomes_itens(self):
        elementos = self.driver.find_elements(*self.NOME_ITEM)
        return [el.text for el in elementos]

    def finalizar_compra(self):
        self.clicar(self.BOTAO_CHECKOUT)
        return self
