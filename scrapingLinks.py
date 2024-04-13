import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode

def get_next_page_url(url, items_offset):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['items_offset'] = items_offset
    updated_query = urlencode(query_params, doseq=True)
    return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{updated_query}"

def scrape_prices(url, num_pages):
    options = Options()
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    all_prices = []
    all_links = []

    prev_page_source = None

    for page in range(num_pages):
        items_offset = page * 20
        current_url = get_next_page_url(url, items_offset)

        driver.get(current_url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pquyp1l')))
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pquyp1l')))
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 't1jojoys')))
        # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="site-content"]/div/div[2]/div/div/div/div/div[1]/div[1]/div/div[2]/div/meta[3]')))

        current_page_source = driver.page_source

        if current_page_source == prev_page_source:
            print("Reached end of results. Stopping scraping.")
            break

        prev_page_source = current_page_source

        print(f"Scraping page {page + 1}")

        # prices = driver.find_elements(By.CLASS_NAME, 'pquyp1l')
        # titles = driver.find_elements(By.CLASS_NAME, 't1jojoys')
        links = driver.find_elements(By.XPATH, '//*[@id="site-content"]/div/div[2]/div/div/div/div/div[1]/div')

        # print(f"Number of prices found on page {page + 1}: {len(prices)}")

        # page_data = []
        page_links = []
        i = 1
        for link in zip(links):
            urlink = '//*[@id="site-content"]/div/div[2]/div/div/div/div/div[1]/div[{}]/div/div[2]/div/meta[3]'.format(i)
            linkurl = driver.find_element(By.XPATH, urlink)
            
            link_value = linkurl.get_attribute("content") if link else None

            page_links.append({ 'Link': link_value})
            i = i + 1

        # all_prices.extend(page_data)
        all_links.extend(page_links)

        time.sleep(1)

    driver.quit()

    return all_links

def main():
    url = 'https://www.airbnb.com.br/s/Curitiba-~-PR/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-05-01&monthly_length=3&monthly_end_date=2024-08-01&price_filter_input_type=0&channel=EXPLORE&query=Curitiba%20-%20PR&place_id=ChIJ3bPNUVPj3JQRCejLuqVrL20&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click'
    num_pages = 2
    links = scrape_prices(url, num_pages)

    df = pd.DataFrame(links)
    df.to_excel('airbnb_links.xlsx', index=False)
    print("Prices exported to 'airbnb_links.xlsx'")

if __name__ == "__main__":
    main()
