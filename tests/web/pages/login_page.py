from selenium.webdriver.common.by import By
from .base_page import PaginaBase


class PaginaLogin(PaginaBase):
    CAMPO_USUARIO = (By.ID, "user-name")
    CAMPO_SENHA = (By.ID, "password")
    BOTAO_LOGIN = (By.ID, "login-button")
    MENSAGEM_ERRO = (By.CSS_SELECTOR, "[data-test='error']")

    URL = "https://www.saucedemo.com/"

    def abrir(self):
        self.driver.get(self.URL)
        return self

    def fazer_login(self, usuario, senha):
        self.digitar_texto(self.CAMPO_USUARIO, usuario)
        self.digitar_texto(self.CAMPO_SENHA, senha)
        self.clicar(self.BOTAO_LOGIN)
        return self

    def obter_mensagem_erro(self):
        return self.obter_texto(self.MENSAGEM_ERRO)
