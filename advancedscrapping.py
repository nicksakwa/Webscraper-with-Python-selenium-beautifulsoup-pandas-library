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
import traceback
# ...existing code...

# 1. Helper to start a Chrome driver with options and return the page_source or raise
def fetch_page_source(url, headless=True, timeout=30):
    options = webdriver.ChromeOptions()
    if headless:
        # try headless first (faster). If it fails below we retry non-headless.
        options.add_argument("--headless=new")
    # add some stability options and a realistic user-agent
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36")
    # create driver (assumes chromedriver is on PATH)
    driver = webdriver.Chrome(options=options)
    page_source = None
    try:
        driver.get(url)
        wait = WebDriverWait(driver, timeout, poll_frequency=0.5)
        # prefer waiting for actual rows, fallback to wrapper
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-datatable-wrapper table tbody tr")))
        except TimeoutException:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-datatable-wrapper")))
        page_source = driver.page_source
        return page_source
    finally:
        try:
            driver.quit()
        except Exception:
            pass

# 2. Try headless, then fall back to headed if needed, always save debug HTML on failure
url = "https://www.itcbenchmarking.org/bso-directory"
print("Navigating to the website...")
page_source = None
try:
    try:
        page_source = fetch_page_source(url, headless=True, timeout=30)
    except TimeoutException:
        # headless timed out, retry with headed browser for debugging/richer rendering
        print("Headless run timed out — retrying with headed browser (visible).")
        page_source = fetch_page_source(url, headless=False, timeout=45)
except WebDriverException as e:
    # Save whatever we have and raise a clearer error
    page_source = page_source or ""
    with open("advancedscrapping_debug_page.html", "w", encoding="utf-8") as f:
        f.write(page_source)
    raise RuntimeError(f"WebDriver error while loading page: {e}\nSaved debug HTML to advancedscrapping_debug_page.html") from e
except TimeoutException:
    # Save debug HTML and raise
    with open("advancedscrapping_debug_page.html", "w", encoding="utf-8") as f:
        f.write(page_source or "")
    raise RuntimeError("Timed out waiting for the table to load. Saved page to advancedscrapping_debug_page.html.")
except Exception:
    # ensure debug HTML saved for unknown failures
    with open("advancedscrapping_debug_page.html", "w", encoding="utf-8") as f:
        f.write(page_source or "")
    raise

# 3. Use BeautifulSoup to parse the page source
print("Parsing the HTML content...")
soup = BeautifulSoup(page_source or "", 'html.parser')

# ...existing code...
table_div = soup.find('div', class_='p-datatable-wrapper')
if table_div is None:
    # Save debug HTML (if not already saved) and raise
    with open("advancedscrapping_debug_page.html", "w", encoding="utf-8") as f:
        f.write(page_source or "")
    raise RuntimeError("Could not find the 'div.p-datatable-wrapper' element in the page HTML. Saved debug HTML.")

table = table_div.find('table')
if table is None:
    with open("advancedscrapping_debug_page.html", "w", encoding="utf-8") as f:
        f.write(page_source or "")
    raise RuntimeError("Could not find a <table> inside the 'div.p-datatable-wrapper' element. Saved debug HTML.")

# ...existing code...
# 8. Extract headers and rows
print("Extracting data...")
thead = table.find('thead')
headers = [th.get_text(strip=True) for th in thead.find_all('th')] if thead else []

data_rows = []
tbody = table.find('tbody') or table

for row in tbody.find_all('tr'):
    cells = row.find_all('td')
    if not cells:
        continue
    if headers:
        row_dict = {headers[i]: (cells[i].get_text(strip=True) if i < len(cells) else "") for i in range(len(headers))}
        data_rows.append(row_dict)
    else:
        row_data = [cell.get_text(strip=True) for cell in cells]
        data_rows.append(row_data)

# ...existing code...