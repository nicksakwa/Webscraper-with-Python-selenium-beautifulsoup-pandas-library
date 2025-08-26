import requests
import pandas as pd
from bs4 import BeautifulSoup

# 1. Setting the URL of the website to scrape
url = "https://www.scrapethissite.com/pages/forms/?per_page=100"

# ...existing code...
# 2. Sending an HTTP GET request to the URL (add User-Agent and check status)
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
response.raise_for_status()

# 3. Parsing the HTML content of the website with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# 4. Finding the table with the CSS class 'table' and checking if it exists
hockey_table = soup.find('table', class_='table')

# Check if the table was found before proceeding
if hockey_table:
    # 5. Extracting all column headers (th elements) from the table
    headers = [header.get_text(strip=True) for header in hockey_table.find_all('th')]
    
    # 6. Creating an empty list to store the data rows
    data_rows = []
    
    # 7. Looping through each table row (tr element) and extracting the data
    tbody = hockey_table.find('tbody') or hockey_table
    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        if not cells:
            continue
        row_data = [cell.get_text(strip=True) for cell in cells]
        data_rows.append(row_data)
        
    # 8. Creating a pandas DataFrame with the extracted data and headers
    df = pd.DataFrame(data_rows, columns=headers)
    
    # 9. Printing the first 5 rows of the DataFrame
    print("Scraping successful! Here is the data:")
    print(df.to_string())
    
    # You can uncomment the line below to save the data to a CSV file
    # df.to_csv('hockey_teams_data.csv', index=False)

else:
    print("Error: The table with class 'table' could not be found on the page.")
    print("Please check the URL or the class name of the table you're trying to scrape.")
# ...existing code...