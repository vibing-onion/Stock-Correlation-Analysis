from bs4 import BeautifulSoup
import requests

import helpers
from helpers import general

import sys
external_file = [
    "helpers"
]
for f in external_file:
    sys.path.append(f)

def load_avail_short():
    url = "https://www.hkex.com.hk/Services/Trading/Securities/Securities-Lists/Designated-Securities-Eligible-for-Short-Selling?sc_lang=zh-HK"
    page = requests.get(url)
    soap = BeautifulSoup(page.text, "html.parser")

    latest_row = soap.find_all("td", class_ = "ms-rteTableOddCol-2")[0]
    latest_date = latest_row.find_all("span")[0].text.replace('/','')

    latest_date = latest_date[-4:] + latest_date[2:4] + latest_date[0:2]

    available_short = "https://www.hkex.com.hk/chi/market/sec_tradinfo/ds" + latest_date + "_c.htm"

    url = available_short
    page = requests.get(url)
    soap = BeautifulSoup(page.text, "html.parser")

    soap = soap.find_all("table")[0].find_all("tr")[1:]
    soap = [data.find_all("td")[1].text.replace('\n', '') for data in soap]
    soap = [data + ".HK" for data in soap]
    
    helpers.general.export_json("temp_file/avail_short.json", soap)

load_avail_short()