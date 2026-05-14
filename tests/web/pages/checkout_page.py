from selenium.webdriver.common.by import By
from .base_page import PaginaBase


class PaginaCheckout(PaginaBase):
    CAMPO_NOME = (By.ID, "first-name")
    CAMPO_SOBRENOME = (By.ID, "last-name")
    CAMPO_CEP = (By.ID, "postal-code")
    BOTAO_CONTINUAR = (By.ID, "continue")
    BOTAO_FINALIZAR = (By.ID, "finish")
    CABECALHO_COMPLETO = (By.CLASS_NAME, "complete-header")
    TOTAL_RESUMO = (By.CLASS_NAME, "summary_total_label")

    def preencher_informacoes(self, nome, sobrenome, cep):
        self.digitar_texto(self.CAMPO_NOME, nome)
        self.digitar_texto(self.CAMPO_SOBRENOME, sobrenome)
        self.digitar_texto(self.CAMPO_CEP, cep)
        self.clicar(self.BOTAO_CONTINUAR)
        return self

    def obter_total(self):
        return self.obter_texto(self.TOTAL_RESUMO)

    def finalizar(self):
        self.clicar(self.BOTAO_FINALIZAR)
        return self

    def obter_cabecalho_completo(self):
        return self.obter_texto(self.CABECALHO_COMPLETO)
