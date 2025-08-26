# ...existing code...
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import time
# ...existing code...

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
wait = WebDriverWait(driver, 20, poll_frequency=0.5)  # increased timeout and polling

try:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.p-datatable-wrapper')))
except TimeoutException:
    driver.quit()
    raise RuntimeError("Timed out waiting for the table to load. The page may have changed or network is slow.")

# 4. Get the complete page source after it has fully loaded
page_source = driver.page_source

# 5. Quit the browser session to free up resources
driver.quit()

# 6. Use BeautifulSoup to parse the page source
print("Parsing the HTML content...")
soup = BeautifulSoup(page_source, 'html.parser')

# 7. Find the table containing the directory data
table_div = soup.find('div', class_='p-datatable-wrapper')
if table_div is None:
    raise RuntimeError("Could not find the 'div.p-datatable-wrapper' element in the page HTML.")

table = table_div.find('table')
if table is None:
    raise RuntimeError("Could not find a <table> inside the 'div.p-datatable-wrapper' element.")

# 8. Extract headers and rows
print("Extracting data...")
thead = table.find('thead')
if thead is None:
    raise RuntimeError("Table does not contain a thead element; table structure may have changed.")
headers = [th.get_text(strip=True) for th in thead.find_all('th')]

data_rows = []
tbody = table.find('tbody') or table

for row in tbody.find_all('tr'):
    cells = row.find_all('td')
    if not cells:
        continue
    # Build a dict mapping headers to cell values (handles missing/padded cells)
    if headers:
        row_dict = {headers[i]: (cells[i].get_text(strip=True) if i < len(cells) else "") for i in range(len(headers))}
        data_rows.append(row_dict)
    else:
        # fallback to list if no headers were found
        row_data = [cell.get_text(strip=True) for cell in cells]
        data_rows.append(row_data)

# 9. Create a pandas DataFrame
if data_rows and isinstance(data_rows[0], dict):
    df = pd.DataFrame(data_rows)
else:
    df = pd.DataFrame(data_rows, columns=headers if headers else None)

# ...existing code...
print("Scraping complete!")
print("\nFirst 5 rows of the scraped data:")
print(df.to_string())
# ...existing code...