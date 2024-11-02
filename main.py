import pandas as pd 
import requests
import bs4 
from bs4 import BeautifulSoup


url = "https://cp.spokanecounty.org/SCOUT/propertyinformation/Summary.aspx?PID=35084.2405"
def scrape_appraiser_house_info():
    response = requests.get(url)
    if response.status_code == 200: #populated well
        #create soup object from response object
        soup = BeautifulSoup(response.text, "html.parser")
        #find the housing price data 
        table = soup.find("table", attrs={"id": "MainContent_AssessedValue_GridView4"})
        #find header 
        thead = table.find("thead")
        #grab the column names 
        ths = thead.find_all("th")
        cols_name = [th.get_text() for th in ths]
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")
        rows = []
        for tr in trs:
            row = []
            tds = tr.find_all("td")
            for td in tds:
                row.append(td.get_text())
            rows.append(row)
        print(rows)
    else: 
        print("response failed")

if __name__ == "__main__":
    scrape_zillow_house_info()