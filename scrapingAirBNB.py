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

    # Initialize previous page source variable
    prev_page_source = None

    for page in range(num_pages):
        # Calculate the offset for the current page
        items_offset = page * 20

        # Get the URL for the current page
        current_url = get_next_page_url(url, items_offset)

        # Navigate to the current page
        driver.get(current_url)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pquyp1l')))
        
        # Wait for all prices to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pquyp1l')))
        
        # Wait for all titles to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 't1jojoys')))

        # Get the current page source
        current_page_source = driver.page_source

        # If the current page source is the same as the previous one, break the loop
        if current_page_source == prev_page_source:
            print("Reached end of results. Stopping scraping.")
            break

        # Update the previous page source
        prev_page_source = current_page_source

        # Print page number
        print(f"Scraping page {page + 1}")

        prices = driver.find_elements(By.CLASS_NAME, 'pquyp1l')
        titles = driver.find_elements(By.CLASS_NAME, 't1jojoys')

        print(f"Number of prices found on page {page + 1}: {len(prices)}")  # Print the number of prices found

        page_data = []
        for title, price in zip(titles, prices):
            title_text = title.text.strip() if title else None
            price_value = price.text.strip() if price else None
            print(f"Title: {title_text}, Price: {price_value}")  # Print title and price details

            page_data.append({
                'Title': title_text,
                'Price': price_value
            })

        all_prices.extend(page_data)

        # Wait briefly before scraping the next page
        time.sleep(2)

    driver.quit()

    return all_prices

def main():
    url = 'https://www.airbnb.com.br/s/Paran%C3%A1--Brasil/homes'
    num_pages = 25  # Number of pages to scrape
    prices = scrape_prices(url, num_pages)

    # Create a DataFrame from the scraped data
    df = pd.DataFrame(prices)

    # Export DataFrame to an Excel file
    df.to_excel('airbnb_prices_paraná.xlsx', index=False)
    print("Prices exported to 'airbnb_prices_paraná.xlsx'")

if __name__ == "__main__":
    main()
