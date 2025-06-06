from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import pandas as pd
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://etender.cpwd.gov.in/")
    page.wait_for_selector("#a_TenderswithinOneday3",timeout=6000)  # Ensure the element loads
    page.click("#a_TenderswithinOneday3")
    page.wait_for_load_state("networkidle")
    page.wait_for_selector("select[name='awardedDataTable_length']")
    # Select the option with value "20"
    page.select_option("select[name='awardedDataTable_length']", value="20")
    # Optional: Wait for the table to update (if it's dynamic)
    page.wait_for_timeout(2000)  # Adjust as needed
    
    html_content = page.content()
    browser.close()

soup = BeautifulSoup(html_content, "html.parser")
table = soup.find("table",class_="table table-bordered tablesorter-blue dataTable no-footer")

if not table:
    print("No table found")

# print(table.prettify())
rows = table.find_all("tr")
data=[]
for row in rows[1:]:  # Skip header row
    cols = row.find_all("td")
    print(f"Row has {len(cols)} columns.")
    if len(cols)>=8:
         if len(cols) >= 8:  # Ensure row has enough columns
            data.append({
            "ref_no": cols[1].text.strip() if len(cols) > 1 else "N/A",
            "title": cols[2].text.strip() if len(cols) > 2 else "N/A",
            "tender_value": cols[4].text.strip() if len(cols) > 4 else "N/A",
            "bid_submission_end_date": cols[6].text.strip() if len(cols) > 6 else "N/A",
            "emd": cols[5].text.strip() if len(cols) > 5 else "N/A",
            "bid_open_date": cols[7].text.strip() if len(cols) > 7 else "N/A"
         })
    else:
        print(f"Row has {len(cols)} columns. Skipping.")
df = pd.DataFrame(data)

df.to_csv("tenders_data.csv",index=False)

