import pandas as pd 
import requests
import bs4 
from bs4 import BeautifulSoup


url = "https://cp.spokanecounty.org/SCOUT/propertyinformation/Summary.aspx?PID=35294.0414"
def scrape_appraiser_house_info():
    response = requests.get(url)
    if response.status_code == 200: #populated well
        #create soup object from response object
        soup = BeautifulSoup(response.text, "html.parser")
        #scraping address and parsel
        df = scrape_address_parcel(soup)
        df1 = scrape_neighborhood(soup) #need to join this first 
        df2 = scrape_home_table(soup) # joining after neighborhood is joined
        headers = df1.columns
        print(df1)
        values_to_drop = []
        for val in headers:
            if val != "Neighborhood Name":
                values_to_drop.append(val)
        df3 = pd.DataFrame(df1.drop(values_to_drop, axis=1), columns=["Neighborhood Name"])
        print(df3)
        joined_df = df.join(df3, how='left') 
        print(joined_df)
        
        # for i, index in enumerate(rows):
        #     if i != 0:
        #         df1.drop(index, axis=0, inplace=True)
        # print("After drops")
        # print(df1)

    else: 
        print("response failed")
    df.to_csv("output.csv")
    return joined_df

def scrape_neighborhood(soup):
    table = soup.find("table", attrs={"id": "MainContent_Appraisal_GridView3"})
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
    df = pd.DataFrame(rows, columns=cols_name)
    df = df.set_index("Neighborhood Name")
    return df

def scrape_address_parcel(soup):
    row = []
    cols_name = ["Parcel Number", "Address"]
    span = soup.find("span", attrs={"id": "lblParcel"})
    #find header 
    parcel_number = span.get_text()
    address_span = soup.find("span", attrs={"id" : "lblSiteAddress"})
    address_number = address_span.get_text()
    address_and_number = [parcel_number,address_number]
    row.append(address_and_number)
    df = pd.DataFrame(row, columns=cols_name)
    df = df.set_index("Parcel Number")
    return df  

def scrape_home_table(soup):
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
    df = pd.DataFrame(rows, columns=cols_name)
    df = df.set_index("Tax Year")
    return df

if __name__ == "__main__":
    df = scrape_appraiser_house_info()
    print(df)