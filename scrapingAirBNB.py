import requests
from bs4 import BeautifulSoup

# Function to scrape property titles from Airbnb search results page
def scrape_titles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    titles = []
    for title_elem in soup.find_all('div', {'class': '_b14dlit'}):  # Adjust class based on Airbnb HTML structure
        titles.append(title_elem.find('div', {'class': '_bzh5lkq'}).text.strip())
    
    return titles

# Main function
def main():
    # Example search URL for Curitiba, Brazil
    search_url = 'https://www.airbnb.com.br/s/Curitiba--Paran%C3%A1--Brasil/homes'
    titles = scrape_titles(search_url)
    
    print("Property Titles in Curitiba:")
    for title in titles:
        print(title)

if __name__ == "__main__":
    main()
