import bs4
import requests
from bs4 import BeautifulSoup
import datetime
import Database as db
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


symbol = 'BAC'

#url = f'https://www.nasdaq.com/symbol/{symbol}/real-time'
#r = requests.get(url)
#soup = bs4.BeautifulSoup(r.text, features="lxml")
#last_sale_price = ''
#test = soup.find_all('symbol-page-header__pricing-price').text

url = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}'
r = requests.get(url)
#soup = bs4.BeautifulSoup(r.text, features="html.parser")
soup = bs4.BeautifulSoup(r.text, features="lxml")
last_sale_price = soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
prev_close = soup.find_all('table', {'class': 'W(100%)'})[0].text
prev_close = prev_close[14:prev_close.find('Open')]
price_and_percent_change = str(soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text)
percent_change = price_and_percent_change[price_and_percent_change.find('(') + 1:-2]
percent_change = float(percent_change.replace('+', ''))
day_range = soup.find_all('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)'})[0].find_all('td')[9].text
#day_range = soup.find_all('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($c-fuji-grey-c)'})[0].find_all('td')[9].text
day_high = str(day_range)[0:day_range.find('-') - 1]
day_low = str(day_range)[day_range.find('-') + 2:]

print(last_sale_price)
print(prev_close)
print(price_and_percent_change)
print(percent_change)
print(percent_change)
print(day_range)
print(day_high)
print(day_low)

