# -*- coding: utf-8 -*-
import time
import sys
import subprocess
import pandas as pd
import re
import openpyxl
from utils import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, \
    ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.alert import Alert


def definir_planilha(driver):
        # https://www.gov.br/transferegov/pt-br/sistemas/acesso-livre
        # https://discricionarias.transferegov.sistema.gov.br/voluntarias/proposta/ConsultarProposta/ConsultarProposta.do 
        driver.get("https://www.gov.br/transferegov/pt-br/sistemas/acesso-livre")
        # driver.find_element(By.XPATH, '//*[@id="login_form"]/div[5]/a').click()
        div = driver.find_element(By.ID, 'main').find_element(By.ID, 'content').find_element(By.ID, 'content-core').\
            find_element(By.ID, 'parent-fieldname-text')
        paragraphs = div.find_elements(By.TAG_NAME, 'p')
        driver.get(paragraphs[4].find_element(By.CSS_SELECTOR, 'span > a').get_attribute('href'))

        df = pd.read_excel('C:\\Users\\gabri\\Desktop\\Trampo\\Tarefa\\propostas.xlsx', engine="openpyxl")
        dados = []
        colunas = ["Nº Proposta", "CNPJ", "Valor Global ", "Total"]
        driver.find_element(By.XPATH, '//*[@id="consultarUfAcessoLivre"]').click()
        driver.find_element(By.XPATH, '//*[@id="consultarUfAcessoLivre"]/option[10]').click()

        driver.find_element(By.XPATH, '/html/body/div[3]/div[12]/div[3]/div/div/form/table/tbody/tr[2]/td[2]/select[2]').click()
        driver.find_element(By.XPATH, '//*[@id="consultarMunicipioAcessoLivre"]/option[152]').click()

        driver.find_element(By.XPATH, '//*[@id="consultarAno"]').send_keys('2024')
        driver.find_element(By.XPATH, '//*[@id="form_submit"]').click()

        table = driver.find_element(By.XPATH, '//*[@id="tbodyrow"]')
        rows = table.find_elements(By.TAG_NAME, "tr")
        total = 0
        for i in range(1, len(rows) + 1):
            link_xpath = f'//*[@id="tbodyrow"]/tr[{i}]/td[1]/div/a'
            v = driver.find_element(By.XPATH, f'//*[@id="tbodyrow"]/tr[{i}]/td[2]/div/a').text
            if "Em" in v:
                 pass
            else:
                 continue
            link_element = driver.find_element(By.XPATH, link_xpath)
            link_element.click()
            time.sleep(5)
            def adicionar_valor(xpath):
                try:
                    return driver.find_element(By.XPATH, xpath).text
                except NoSuchElementException:
                    return None
            N_Orgao = adicionar_valor('//*[@id="tr-alterarNumeroInterno"]/td[2]')
            N_Processo = adicionar_valor('//*[@id="tr-alterarNumeroProcesso"]/td[2]')
            valor_str = adicionar_valor('//*[@id="tr-alterarPercentualMinimoContrapartida"]/td/b')
            valor_str_limpo = valor_str.replace('R$', '').replace('.', '').replace(',', '.')
            valor = float(valor_str_limpo)
            total += valor
            dados += [[N_Orgao, N_Processo, valor_str,"" ]]
            df = pd.DataFrame(dados, columns=colunas)
            df.to_excel("Morrinhos_cnpj.xlsx", index=False)
            driver.back()
        resultado = f"R$ {total}"
        dados += [['', 'Montante Total: ', resultado,'']]
        df = pd.DataFrame(dados, columns=colunas)
        df.to_excel("Morrinhos_cnpj.xlsx", index=False)   

        # driver.close()

def main():
    inicio = time.time()
    driver = setup_drive()
    wait = WebDriverWait(driver, 15)
    definir_planilha(driver)

    driver.close()

    fim = time.time()
    tempo_total = (fim - inicio) / 60

    print(f"Tempo de execução: {tempo_total:.2f} minutos")


if __name__ == '__main__':
    main()
