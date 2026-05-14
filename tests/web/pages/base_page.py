from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PaginaBase:
    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, 20)

    def encontrar(self, localizador):
        return self.espera.until(EC.presence_of_element_located(localizador))

    def clicar(self, localizador):
        self.encontrar(localizador)
        self.driver.find_element(*localizador).click()

    def digitar_texto(self, localizador, texto):
        elemento = self.encontrar(localizador)
        elemento.clear()
        elemento.send_keys(texto)

    def obter_texto(self, localizador):
        return self.encontrar(localizador).text
