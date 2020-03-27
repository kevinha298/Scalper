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

url = f'https://www.nasdaq.com/symbol/{symbol}/real-time'
url = f'https://www.nasdaq.com/market-activity/stocks/{symbol}/real-time'
r = requests.get(url)
soup = bs4.BeautifulSoup(r.text, features="lxml")
test1 = soup.find_all('div', {'class': 'header-ads'})
test2 = soup.find_all('main', {'class': 'page__main', 'role': 'main'})[0].find_all('div', {'class': 'page__content'})[0].find_all('div', {'class': 'quote-subdetail__header-container'})[0].find_all('span', {'class': 'symbol-page-header__pricing-last-price'})[1]
test3 = soup.find_all('main', {'class': 'page__main', 'role': 'main'})[0].find_all('div', {'class': 'page__content'})[0].find_all('div', {'class': 'quote-subdetail__header-container'})[0].find_all('div', {'class': 'symbol-page-header__pricing-changes'})



#print(test1)
print(test2)
print(test3)

#last_sale_price = soup.find_all('div',{'class':'symbol-page-header__pricing-details symbol-page-header__pricing-details--current symbol-page-header__pricing-details--increase'})[0].text
#last_sale_price = soup.find('div')
#last_sale_price = soup.find_all(class_= "symbol-page-header__pricing-details symbol-page-header__pricing-details--current symbol-page-header__pricing-details--increase")
#test = last_sale_price.find('symbol-page-header__pricing-details symbol-page-header__pricing-details--current symbol-page-header__pricing-details--increase')
#print(last_sale_price)

""" print(last_sale_price)
print(soup.find_all('div')) """


