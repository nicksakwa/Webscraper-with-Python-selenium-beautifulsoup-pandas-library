import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.scrapethissite.com/pages/forms/?per_page=100"

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

hockey_table = soup.find('table', class_='table')


if hockey_table:
    headers = [header.get_text(strip=True) for header in hockey_table.find_all('th')]
    
    data_rows = []
    tbody = hockey_table.find('tbody') or hockey_table
    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        if not cells:
            continue
        row_data = [cell.get_text(strip=True) for cell in cells]
        data_rows.append(row_data)
        
    df = pd.DataFrame(data_rows, columns=headers)
    
    print("Scraping successful! Here is the data:")
    print(df.to_string())

else:
    print("Error: The table with class 'table' could not be found on the page.")
    print("Please check the URL or the class name of the table you're trying to scrape.")