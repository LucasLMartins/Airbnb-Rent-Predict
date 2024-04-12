import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_prices(url):
    options = Options()
    # Remove headless option to run Chrome in regular mode
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # Wait for the prices to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pquyp1l')))

    prices = driver.find_elements(By.CLASS_NAME, 'pquyp1l')
    print(f"Number of prices found: {len(prices)}")  # Print the number of prices found

    price_data = []
    for price in prices:
        price_value = price.text.strip() if price else None

        print(f"Price: {price_value}")  # Print price details

        price_data.append({
            'Price': price_value
        })

    driver.quit()

    return price_data

def main():
    url = 'https://www.airbnb.com.br/s/Curitiba--Paran%C3%A1--Brasil/homes'
    prices = scrape_prices(url)

    # Create a DataFrame from the scraped data
    df = pd.DataFrame(prices)

    # Export DataFrame to an Excel file
    df.to_excel('airbnb_prices.xlsx', index=False)
    print("Prices exported to 'airbnb_prices.xlsx'")

if __name__ == "__main__":
    main()
