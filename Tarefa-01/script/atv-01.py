# -- coding: utf-8 --
import time
import sys
import subprocess
import pandas as pd
import re
from utils import *
import openpyxl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, \
    ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.alert import Alert


def definir_planilha(driver):
        driver.get("https://www.gov.br/transferegov/pt-br/sistemas/acesso-livre")
        driver.find_element(By.XPATH, '//*[@id="login_form"]/div[5]/a').click()
        div = driver.find_element(By.ID, 'main').find_element(By.ID, 'content').find_element(By.ID, 'content-core').\
            find_element(By.ID, 'parent-fieldname-text')
        paragraphs = div.find_elements(By.TAG_NAME, 'p')
        driver.get(paragraphs[4].find_element(By.CSS_SELECTOR, 'span > a').get_attribute('href'))

        df = pd.read_excel('C:\\Users\\gabri\\Desktop\\Trampo\\Tarefa\\propostas.xlsx', engine="openpyxl")
        dados = []
        colunas = ["Nº Proposta", "CNPJ", "Município"]
        for ind, linha in df.iterrows():
            driver.get("https://discricionarias.transferegov.sistema.gov.br/voluntarias/proposta/ConsultarProposta/ConsultarProposta.do ")
            proposta = linha.iloc[0]
            cnpj, cidade = pegar_cnpj(driver, proposta)
            dados += [[proposta, cnpj, cidade]]

        df = pd.DataFrame(dados, columns=colunas)
        df.to_excel("propostas_cnpj.xlsx", index=False)
        driver.close()

        
def pegar_cnpj(driver, proposta):
    def adicionar_valor(xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text
        except NoSuchElementException:
            return None
        
    lista_dados = []
    driver.find_element(By.XPATH, '//*[@id="consultarNumeroProposta"]').clear()
    driver.find_element(By.XPATH, '//*[@id="consultarNumeroProposta"]').send_keys(proposta)
    driver.find_element(By.XPATH, '//*[@id="form_submit"]').click()

    cidade = adicionar_valor('//*[@id="tbodyrow"]/tr/td[4]/div/a')
    cnpj = adicionar_valor('//*[@id="tbodyrow"]/tr/td[6]/div/a')

    return cnpj, cidade


def main():
    inicio = time.time()
    # PADRONIZANDO DRIVER DO CHROME
    driver = setup_drive()

    # TEMPO DO WAIT
    wait = WebDriverWait(driver, 15)

    # REALIZAR CONSULTAS
    definir_planilha(driver)

    fim = time.time()
    tempo_total = (fim - inicio) / 60

    print(f"Tempo de execução: {tempo_total:.2f} minutos")


if __name__ == '_main_':
    main()
