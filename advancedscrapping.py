import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# 1. Set up the Selenium WebDriver
# This code sets up a headless browser (it runs without a graphical user interface)
# so it won't open a window on your screen.
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Ensure your chromedriver is correctly set up, you may need to specify a path
# For example: service = Service('/path/to/your/chromedriver')
driver = webdriver.Chrome(options=options)

# 2. Navigate to the URL
url = "https://www.itcbenchmarking.org/bso-directory"
print("Navigating to the website...")
driver.get(url)

# 3. Wait for the dynamic content (the table) to load
# This is the crucial part for dynamic websites.
# We'll wait until a specific element (the table with a certain class) is present on the page.
print("Waiting for the table to load...")
wait = WebDriverWait(driver, 10)  # Wait for a maximum of 10 seconds
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.p-datatable-wrapper')))

# 4. Get the complete page source after it has fully loaded
page_source = driver.page_source

# 5. Quit the browser session to free up resources
driver.quit()

# 6. Use BeautifulSoup to parse the page source
print("Parsing the HTML content...")
soup = BeautifulSoup(page_source, 'html.parser')

# 7. Find the table containing the directory data
table_div = soup.find('div', class_='p-datatable-wrapper')
table = table_div.find('table')

# 8. Extract headers and rows
print("Extracting data...")
headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
data_rows = []

for row in table.find('tbody').find_all('tr'):
    cells = row.find_all('td')
    row_data = [cell.get_text(strip=True) for cell in cells]
    data_rows.append(row_data)

# 9. Create a pandas DataFrame
df = pd.DataFrame(data_rows, columns=headers)

# 10. Save the DataFrame to a CSV file
# Note: I can't actually run this code and save a file.
# When you run this, a file named 'itc_directory.csv' will be created.
# df.to_csv('itc_directory.csv', index=False)

print("Scraping complete!")
print("\nFirst 5 rows of the scraped data:")
print(df.to_string())