import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

# Inicialização do WebDriver
options = Options()
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

# Carregando o arquivo Excel
df_links = pd.read_excel('airbnb_links.xlsx', usecols=['Link'])

# Inicializando listas para armazenar os dados
data = {
    'url': [],
    'titulo': [],
    'tipo': [],
    'localizacao': [],
    'valor': [],
    'hospedes': [],
    'quartos': [],
    'camas': [],
    'banheiros': []
}

# Função para extrair dados de uma URL
def extrair_dados(url):
    parsedUrl = 'https://' + url
    driver.get(parsedUrl)
    time.sleep(1)

    # Esperando elementos carregarem
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div/div[1]/span/h1')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[1]/h2')))

    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[4]/div/div/div/div[1]/h3')))
    except:
        print(f"Localização not found for URL: {parsedUrl}. Skipping...")
        return

    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[4]')))
    except:
        print(f"Banheiros not found for URL: {parsedUrl}. Skipping...")
        return

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[1]')))
    
    # Setandos os elementos no array
    data['url'].append(parsedUrl)
    data['titulo'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div/div[1]/span/h1').text)
    data['tipo'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[1]/h2').text)
    
    try:
        data['localizacao'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[4]/div/div/div/div[1]/h3').text)
    except:
        print(f"Localização not found for URL: {parsedUrl}. Skipping...")
        data['localizacao'].append("N/A")

    try:
        data['valor'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[1]').text)
    except:
        data['valor'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[2]').text)
    
    data['hospedes'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[1]').text)
    data['quartos'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[2]').text)
    data['camas'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[3]').text)
    
    try:
        data['banheiros'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[4]').text)
    except:
        print(f"Banheiros not found for URL: {parsedUrl}. Skipping...")
        data['banheiros'].append("N/A")

# Iterando sobre os links e extraindo os dados
t0 = time.time()
for link in df_links['Link']:
    try:
        extrair_dados(link)
    except Exception as e:
        print(f"An error occurred for URL: {link}. Skipping...")
        print(e)

# Convertendo os dados para DataFrame
df = pd.DataFrame(data)

# Salvando os dados em um novo arquivo Excel
df.to_excel('airbnb_dados.xlsx', index=False)
print(time.time() - t0)
