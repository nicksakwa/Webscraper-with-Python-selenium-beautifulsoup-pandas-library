# 1. Importing the necessary libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup

# 2. Setting the URL of the website to scrape
url = "https://www.scrapethissite.com/pages/forms/?per_page=10"

# 3. Sending an HTTP GET request to the URL
response = requests.get(url)

# 4. Parsing the HTML content of the website with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# 5. Finding the table with the CSS class 'table'
hockey_table = soup.find('table', class_='table')

# 6. Extracting all column headers (th elements) from the table
table_headers = [header.get_text(strip=True) for header in hockey_table.find_all('th')]

# 7. Creating an empty list to store the data rows
data_rows = []

# 8. Looping through each table row (tr element) and extracting the data
for row in hockey_table.find('tbody').find_all('tr'):
    cells = row.find_all('td')
    row_data = [cell.get_text(strip=True) for cell in cells]
    data_rows.append(row_data)

# 9. Creating a pandas DataFrame with the extracted data and headers
df = pd.DataFrame(data_rows, columns=table_headers)

# 10. Saving the DataFrame to a CSV file
# Note: I can't actually run this code and save a file, but this is the correct command
# df.to_csv('hockey_teams_data.csv', index=False)

# Optional: Print the first few rows of the DataFrame to confirm it works
print(df.head())