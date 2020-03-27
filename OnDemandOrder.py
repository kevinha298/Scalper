import alpaca_trade_api as tradeapi
from dateutil import tz
import Database as db
import GetRealTimeQuote
import datetime
import time
from ast import literal_eval
import dateutil.parser
from datetime import datetime
from pytz import timezone
import requests
from bs4 import BeautifulSoup
import bs4


api = tradeapi.REST(
    key_id='PKMGRDNQ2W2URIHDJ4UK',
    secret_key='H1KaFRxgKkxjTFmZdDeTGOu68XkFiZL5EvHugNrT',
    base_url='https://paper-api.alpaca.markets'
)

symbol = 'OXY'
buy_qty = 200
side = 'buy'
order_type = 'limit'
order_span = 'day'
order_buy_price = '10.99'


api.submit_order(symbol, buy_qty, side, order_type, order_span, order_buy_price)
