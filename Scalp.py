import alpaca_trade_api as tradeapi
from dateutil import tz
import Database as db
#import GetRealTimeQuote as realtime
import datetime
import time
from ast import literal_eval
import dateutil.parser
from datetime import datetime
from pytz import timezone
import random
#import SubmitBuyOrder as bo
#import SubmitSellOrder as so
import os
from dotenv import load_dotenv
load_dotenv()

api = tradeapi.REST(
    key_id = os.getenv('ALPACA_ID'),
    secret_key = os.getenv('ALPACA_KEY'),
    base_url = 'https://paper-api.alpaca.markets'
)
print(str(datetime.now()) + ': Established API connection.')

clock = api.get_clock()
now = clock.timestamp

print(f'API clock: {clock}')
print(f'Current clock timestamp: {now}')

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')

db_conn = db.connect()

db.insert_run_log(db_conn, str(datetime.now()), 'Test database connection.', '', '')

