import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode

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

    # Esperando elementos carregarem
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div/div[1]/span/h1')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[1]/h2')))
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[4]/div/div/div/div[1]/h3')))
    except:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[2]')))

    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[4]')))
    except:
        return

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[1]')))
    
    # acompanhando os elementos no console
    # print(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div/div[1]/span/h1').text)
    # print(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[1]/h2').text)
    # try:
    #     print(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[4]/div/div/div/div[1]/h3').text)
    # except:
    #     print(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[2]').text)

    # try:
    #     print(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[1]').text)
    # except:
    #     print(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[2]').text)
    # print(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[1]').text)
    # print(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[2]').text)
    # print(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[3]').text)
    # print(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[4]').text)

    # Setandos os elementos no array
    data['url'].append(parsedUrl)
    data['titulo'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div/div[1]/span/h1').text)
    data['tipo'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[1]/h2').text)
    try:
        data['localizacao'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[4]/div/div/div/div[1]/h3').text)
    except:
        data['localizacao'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[2]').text)

    try:
        data['valor'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[1]').text)
    except:
        data['valor'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[2]').text)
    data['hospedes'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[1]').text)
    data['quartos'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[2]').text)
    data['camas'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[3]').text)
    data['banheiros'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[4]').text)

# Iterando sobre os links e extraindo os dados
t0 = time.time()
for link in df_links['Link']:
    extrair_dados(link)
    # time.sleep(2)

# Fechando o WebDriver
driver.quit()
print(time.time() - t0)

# Convertendo os dados para DataFrame
df = pd.DataFrame(data)

# Salvando os dados em um novo arquivo Excel
df.to_excel('airbnb_dados.xlsx', index=False)
