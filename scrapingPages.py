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
df_links = pd.read_excel('airbnb_links5.xlsx', usecols=['Link'])

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
    'banheiros': [],
}

amenitiesData = {
    'Elevador': [],
    'Cozinha': [],
    'Microondas': [],
    'Fogão': [],
    'Mesadejantar': [],
    'Wi-Fi': [],
    'Ar-condicionado': [],
    'TV': [],
    'Secadordecabelo': [],
    'Xampu': [],
    'Condicionador': [],
    'Saboneteparaocorpo': [],
    'Águaquente': [],
    'MáquinadeLavar': [],
    'Secadora': [],
    'Café': [],
    'Fechadurainteligente': [],
    'Refrigerador': [],
    'Permitidoanimais': [],
    'Permitidofumar': [],
    'Banheira': [],
    'Produtosdelimpeza': [],
    'Básico': [],
    'Cabides': [],
    'Roupadecama': [],
    'Cinema': [],
    'Lareirainterna': [],
    'Espaçodetrabalhoexclusivo': [],
    'Itensbásicosdecozinha': [],
    'Louçasetalheres': [],
    'Frigobar': [],
    'Lavalouças': [],
    'Cafeteira': [],
    'Torradeira': [],
    'Entradaprivada': [],
    'Áreadejantarexterna': [],
    'Churrasqueira': [],
    'Estacionamentoincluído': [],
    'Jacuzziprivativa': [],
    'Vistaparaojardim': [],
}

# Função para extrair dados de uma URL
def extrair_dados(url):
    parsedUrl = 'https://' + url
    driver.get(parsedUrl)

    # Esperando elementos carregarem
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div/div[1]/span/h1')))
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[1]/h2')))

    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[4]/div/div/div/div[1]/h3')))
    except:
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[2]')))
        except:
            print(f"Localização not found for URL: {parsedUrl}. Skipping...")
            return

    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[4]')))
    except:
        print(f"Hospedes, quartos, camas or banheiros not found for URL: {parsedUrl}. Skipping...")
        return

    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[1]')))
    except:
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[2]')))
        except:
            print(f"Valor not found for URL: {parsedUrl}. Skipping...")
            return

    # Setandos os elementos no array
    data['url'].append(parsedUrl)
    data['titulo'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[1]/div[1]/div/div/div/div/div/section/div/div[1]/span/h1').text)
    data['tipo'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[1]/h2').text)

    try:
        data['localizacao'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[4]/div/div/div/div[1]/h3').text)
    except:
        try:
            data['localizacao'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[5]/div/div/div/div[2]/section/div[2]').text)
        except:
            data['localizacao'].append("N/A")

    try:
        data['valor'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[1]').text)
    except:
        try:
            data['valor'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[2]').text)
        except:
            data['valor'].append("N/A")
        
    data['hospedes'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[1]').text)

    try:
        data['quartos'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[2]').text)
    except:
        data['quartos'].append("N/A")

    try:
        data['camas'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[3]').text)
    except:
        data['camas'].append("N/A")

    try:
        data['banheiros'].append(driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[4]').text)
    except:
        data['banheiros'].append("N/A")

    try:
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]'))).click()
    except:
        0

    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[5]/div/div[2]/section/div[3]/button'))).click()
    except:
        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[6]/div/div[2]/section/div[3]/button'))).click()
        except:
            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[7]/div/div[2]/section/div[3]/button'))).click()
            except:
                try:
                    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[8]/div/div[2]/section/div[3]/button'))).click()
                except:
                    print("Comodidades not found")

    WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[3]/div/div/div/section/div[2]/div')))
    amenities_div = driver.find_elements(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[3]/div/div/div/section/div[2]/div')
    amenitiesList = []
    a = 1
    for type in zip(amenities_div):
        b = 1
        amenities = driver.find_elements(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[3]/div/div/div/section/div[2]/div[{}]/ul/li'.format(a))
        for type_amenity in zip(amenities):
            amenity = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[3]/div/div/div/section/div[2]/div[{}]/ul/li[{}]/div[1]/div/div[2]/div'.format(a,b))
            amenitiesList.append(amenity.text)
            b = b + 1
        a = a + 1
    amenitiesFiltered = [elemento for elemento in amenitiesList if 'Indisponível' not in elemento]
    for i in range(len(amenitiesFiltered)):
        amenitiesFiltered[i] = amenitiesFiltered[i].replace(" ", "")
    
    for item in amenitiesData:
        if item in amenitiesFiltered:
            amenitiesData[item].append(1)
        else:
            amenitiesData[item].append(0)

    data.update(amenitiesData)

# Extraindo os dados
t0 = time.time()
l = 1
for link in df_links['Link']:
    print(f"Scraping link {l}")
    try:
        extrair_dados(link)
    except Exception as e:
        print(f"An error occurred for URL: {link}. Skipping...")
        print(e)
    l = l + 1

# Convertendo os dados para DataFrame
df = pd.DataFrame(data)

# Salvando os dados em um novo arquivo
df.to_excel('airbnb_dados5.xlsx', index=False)
print(f'Duração do scraping: {time.time() - t0} segundos')
