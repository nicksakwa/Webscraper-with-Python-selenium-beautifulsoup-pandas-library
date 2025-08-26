import requests
from bs4 import BeautifulSoup
import pandas as pd

url="https://www.scrapethissite.com/pages/forms/?per_page=100"

response= requests.get(url)
soup= BeautifulSoup(response.text, 'html.parser')
hockey_table=soup.find('table', class_='table')
if hockey_table:
    headers=[header.get_text(strip=True) for header in hockey_table.find_all('th')]
    data_rows= []
    for row in hockey_table.find_all('tr'):
        cells= row.find_all('td')
        row_data=[cell.get_text(strip=True) for cell in cells]
        data_rows.append(row_data)
    df=pd.DataFrame(data_rows, columns=headers)

    print("Scraping data successful! Here is the data:")
    print(df.to_string())
    df.to_csv("hockey_data.csv", index=False)
    print("Data saved to hockey_data.csv")
else:
    print("Error: Hockey table not found.")
    print("Please check the website structure or the class names used in the scraper.")