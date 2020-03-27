import bs4
import requests
from bs4 import BeautifulSoup
import datetime
import Database as db
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def parsePrice(symbol, lapse):
    iex_api_key = os.getenv('IEX_API_KEY')
    last_sale_price = 1000  # default last sale price
    if lapse % 2 == 0:
        url = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}'
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text, features="lxml")
        try:
            last_sale_price = soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
            prev_close = soup.find_all('table', {'class': 'W(100%)'})[0].text
            prev_close = prev_close[14:prev_close.find('Open')]
            price_and_percent_change = str(soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find_all('span')[1].text)
            percent_change = price_and_percent_change[price_and_percent_change.find('(') + 1:-2]
            percent_change = float(percent_change.replace('+', ''))
            #day_range = soup.find_all('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($c-fuji-grey-c)'})[0].find_all('td')[9].text
            day_range = soup.find_all('div', {'class': 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)'})[0].find_all('td')[9].text
            day_low = str(day_range)[0:day_range.find('-') - 1]
            day_high = str(day_range)[day_range.find('-') + 2:]
        except Exception as error:
            db_conn = db.connect()
            db.insert_run_log(db_conn, str(datetime.now()), f'Encountered an exception when trying to retrieve price for {symbol} from Yahoo.', error, soup)
        print(f'Yahoo: symbol = {symbol},  price = {last_sale_price}')
    elif lapse % 2 == 10:
        url = f'https://www.nasdaq.com/symbol/{symbol}/real-time'
        url_quote = f'https://www.nasdaq.com/symbol/{symbol}'
        r = requests.get(url)
        r_quote = requests.get(url_quote)
        soup = bs4.BeautifulSoup(r.text, features="lxml")
        soup_quote = bs4.BeautifulSoup(r_quote.text, features="lxml")
        last_sale_price = ''
        try:
            last_sale_price = soup.find_all('div', {'class': 'qwidget-dollar', 'id': 'qwidget_lastsale'})[0].text
            last_sale_price = float(last_sale_price[1:])
            percent_change = soup.find_all('div', {'class': 'qwidget-percent', 'id': 'qwidget_percent'})[0].text
            percent_change = float(percent_change[:-1])
            day_high_low = soup_quote.find_all('div', {'class': 'table-table fontS14px'})[0].find_all('div', {'class': 'table-row'})[1].find_all('div', {'class': 'table-cell'})[1].text
            day_high_low = str(day_high_low)[day_high_low.find('$'):]
            day_high = float(day_high_low[day_high_low.find('$') + 2:day_high_low.find('/') - 1])
            day_low = float(day_high_low[day_high_low.find('/') + 3:day_high_low.find('/') + 15])
            prev_close = soup_quote.find_all('div', {'class': 'table-table fontS14px'})[0].find_all('div', {'class': 'table-row'})[4].find_all('div', {'class': 'table-cell'})[1].text
            prev_close = str(prev_close)[prev_close.find('$'):]
            prev_close = float(prev_close[prev_close.find('$') + 2:prev_close.find('.') + 5])
            if last_sale_price < prev_close:
                percent_change *= -1
        except Exception as error:
            db_conn = db.connect()
            db.insert_run_log(db_conn, str(datetime.now()),f'Encountered an exception when trying to retrieve price for {symbol} from Nasdaq.',error, soup)
        print(f'Nasdaq: symbol = {symbol},  price = {last_sale_price}')
    elif lapse % 2 == 1:
        url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={iex_api_key}'
        try:
            r = requests.get(url)
            r_json = r.json()
            last_sale_price = r_json['latestPrice']
            percent_change = float(r_json['changePercent'] * 100)
            day_low = r_json['low'] if r_json['low'] == 'None' else last_sale_price
        except Exception as error:
            db_conn = db.connect()
            db.insert_run_log(db_conn, str(datetime.now()), f'Encountered an exception when trying to retrieve price for {symbol} from IEX.', error, url)
        print(f'IEX: symbol = {symbol},  price = {last_sale_price}')

        # url = f'https://cloud.iexapis.com/stable/tops?token={iex_api_key}&symbols={symbol}'
        # try:
        #     r = requests.get(url)
        #     r_json = r.json()
        #     r_list = r_json[0]
        #     last_sale_price = r_list['lastSalePrice']
        # except Exception as error:
        #     db_conn = db.connect()
        #     db.insert_run_log(db_conn, str(datetime.now()), f'Encountered an exception when trying to retrieve price for {symbol} from IEX.', error, url)
        # print(f'IEX: {last_sale_price}')
    return float(last_sale_price), float(percent_change), float(day_low)




