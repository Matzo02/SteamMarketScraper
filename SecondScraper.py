from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import csv
import pandas as pd

# after examining the source page, choose which data we want to extract.
header = ['Item', 'Price', 'Date_time']

# create a new csv file and write in the header row.
with open('Invoker_data.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)


def check_price():
    URL = "https://steamcommunity.com/market/search?q=Dark+Artistry"#Steam has a tendancy to not display items with filters sometimes, So make sure the page is readable.

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    item = soup2.find_all("span", {"class": "market_listing_item_name"})
    price = soup2.find_all("span", {"class": "normal_price", "data-currency": "1"})
    #check steams naming trends through console to add more columns if you want.
    for x, i in enumerate(item):
        item[x] = i.get_text().strip()

    for x, i in enumerate(price):
        price[x] = i.get_text().strip()

    data = []

    for n in range(len(item)):
        entry = [item[n], price[n], now]
        data.append(entry)

    with open('Invoker_data.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


# retrieve data
check_price()

df = pd.read_csv(r'Invoker_data.csv')
df.sort_values(by=['Item', 'Date_time'])
df

# inspect our csv file
while(True):
    check_price()
    time.sleep(86400)#change time depending on your preference

