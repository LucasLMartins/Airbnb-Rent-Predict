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
    # Remove headless option to run Chrome in regular mode
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    all_prices = []

    for page in range(num_pages):
        driver.get(url)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pquyp1l')))
        
        # Wait for all prices to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pquyp1l')))

        prices = driver.find_elements(By.CLASS_NAME, 'pquyp1l')
        print(f"Number of prices found on page {page + 1}: {len(prices)}")  # Print the number of prices found

        page_prices = []
        for price in prices:
            price_value = price.text.strip() if price else None
            print(f"Price: {price_value}")  # Print price details

            page_prices.append({
                'Price': price_value
            })

        all_prices.extend(page_prices)

        # Update the URL to navigate to the next page
        items_offset = (page + 1) * 20  # Incremental offset for each page
        next_url = get_next_page_url(url, items_offset)
        driver.get(next_url)

        # Wait briefly before scraping the next page
        time.sleep(2)

    driver.quit()

    return all_prices

def main():
    url = 'https://www.airbnb.com.br/s/Curitiba--Paran%C3%A1--Brasil/homes'
    num_pages = 25  # Number of pages to scrape
    prices = scrape_prices(url, num_pages)

    # Create a DataFrame from the scraped data
    df = pd.DataFrame(prices)

    # Export DataFrame to an Excel file
    df.to_excel('airbnb_prices.xlsx', index=False)
    print("Prices exported to 'airbnb_prices.xlsx'")

if __name__ == "__main__":
    main()
