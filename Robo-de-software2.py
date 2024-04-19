from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from pymongo import MongoClient

def config_driver():
    servico = Service(ChromeDriverManager().install())
    options = ChromeOptions()
    options.add_argument('--headless')

    navegador = webdriver.Chrome(service=servico, options=options)
    navegador.implicitly_wait(5)
    return navegador

def config_data():
    data_atual = datetime.now()
    data_seis_meses_atras = data_atual - timedelta(days=30*6)
    data_formatada = data_seis_meses_atras.strftime('%d/%m/%Y')

    return data_formatada

def get_links(navegador):
    navegador.get("https://unica.com.br/noticias/")
    
    campo_data = navegador.find_element(By.ID, 'from')  
    campo_data.clear()
    campo_data.send_keys(config_data())

    # Coleta dos links 
    lista = navegador.find_element(By.CLASS_NAME, 'lista')
    anchors = lista.find_elements(By.TAG_NAME, 'a')
    valid_links = []

    for anchor in anchors:
        href = anchor.get_attribute('href')
        if 'noticias' in href and href not in valid_links:
            valid_links.append(href)

    return valid_links

def web_scrape(navegador, urls):
    data_matrix = []

    for url in urls:
        navegador.get(url)
   
        soup = BeautifulSoup(navegador.page_source, 'html.parser')

        title = soup.title.text.strip() if soup.title else 'No title'

        paragraphs = [p.get_text() for p in soup.find_all('p')]
        content = '\n'.join(paragraphs)

        data_matrix.append({'url': url, 'title': title, 'content': content})

    return data_matrix

def save_to_mongodb(data_matrix):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['']
    noticias_collection = db[''] 
    
    noticias_collection.insert_many(data_matrix) 

if __name__ == "__main__":
    try:
        navegador = config_driver()
        links = get_links(navegador)
        print(links)
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        data_matrix = web_scrape(navegador, links)

        for row in data_matrix:
            print(row)
        
        save_to_mongodb(data_matrix)
        print("Dados salvos no MongoDB com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
    finally:
        if 'navegador' in locals():
            navegador.quit()
