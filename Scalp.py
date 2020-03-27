import alpaca_trade_api as tradeapi
from dateutil import tz
import Database as db
import GetRealTimeQuote as realtime
import datetime
import time
from ast import literal_eval
import dateutil.parser
from datetime import datetime
from pytz import timezone
import random
import SubmitBuyOrder as bo
import SubmitSellOrder as so
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

def app_run_cond():
    app_config = db.execute_query(db_conn, "SELECT * FROM app_config WHERE config_name = 'is_app_active'")
    run_app = False
    clock = api.get_clock()
    for config in app_config:
        run_app = True if config[0] == 'is_app_active' and int(config[1]) == 1 and datetime.today().weekday() < 6 and clock.is_open else False
    return run_app

order_keys = ['asset_class', 'asset_id', 'canceled_at', 'client_order_id', 'created_at', 'expired_at', 'failed_at', 'filled_at', 'filled_avg_price', 'filled_qty', 'id', 'limit_price', 'order_type', 'qty', 'side', 'status', 'stop_price', 'submitted_at', 'symbol', 'time_in_force', 'type', 'updated_at']
lapse = 0
while app_run_cond():
    lapse += 1
    print(f'Run #: {lapse}')

    for j in range(1,3):
        # Get a list of filled orders.  To improve speed we want to only get recently filled orders today.
        orders = [o for o in api.list_orders(status='closed') if o.status == 'filled']
        insert_values = ''
        for order in orders:
            order = str(order)[str(order).find('(')+1:-1]
            order = order.replace("Order({   '","{'")
            order = literal_eval(order)
            filled_at = str(order['filled_at'])[:10] +' ' + str(order['filled_at'])[11:19]
            filled_at = datetime.strptime(filled_at, '%Y-%m-%d %H:%M:%S')
            filled_at = filled_at.replace(tzinfo=from_zone)
            filled_at_east_std_time = str(filled_at.astimezone(to_zone))[:-6]
            order_values = ''
            for keys,values in order.items():
                if keys in order_keys:
                    order_values += f"'{values}',"
            order_values = f"{order_values}'{filled_at_east_std_time}'"
            insert_values += f"({order_values}),"
        # db.insert_run_log(db_conn, str(datetime.now()), 'Retrieved all recent orders data from API.', NULL, NULL)
        print(str(datetime.now()) + ': Retrieved all recent orders data from API.')

        # update filled orders into back-end database.
        insert_values = insert_values[:-1]
        db.truncate(db_conn, 'filled_order_stage')
        # db.insert_run_log(db_conn, str(datetime.now()), 'Truncated stage table in database.', NULL, NULL)
        print(str(datetime.now()) + ': Truncated stage table in database.')

        db.insert_filled_order(db_conn, insert_values)
        # db.insert_run_log(db_conn, str(datetime.now()), 'Updated stage table in database with recent order data from API.', NULL, NULL)
        print(str(datetime.now()) + ': Updated stage table in database with recent order data from API.')

        db.call_store_procedure(db_conn, 'add_new_filled_order')
        # db.insert_run_log(db_conn, str(datetime.now()), 'Updated recent order data from stage table to order table.', NULL, NULL)
        print(str(datetime.now()) + ': Updated recent order data from stage table to order table.')


        db.call_store_procedure(db_conn, 'add_transaction_buy')
        # db.insert_run_log(db_conn, str(datetime.now()), 'Updated recent order into buy transaction table.', NULL, NULL)
        print(str(datetime.now()) + ': Updated recent order into buy transaction table.')

        db.call_store_procedure(db_conn, 'add_transaction_sell')
        # db.insert_run_log(db_conn, str(datetime.now()), 'Updated recent order into sell transaction table.', NULL, NULL)
        print(str(datetime.now()) + ': Updated recent order into sell transaction table.')

        db.call_store_procedure(db_conn, 'update_transaction')
        # db.insert_run_log(db_conn, str(datetime.now()), 'Calculated and synchronized buy and sell transactions and updated open positions.', NULL, NULL)
        print(str(datetime.now()) + ': Calculated and synchronized buy and sell transactions and updated open positions.')

        db.call_store_procedure(db_conn, 'update_queue_sell')
        # db.insert_run_log(db_conn, str(datetime.now()), 'Updated database queue for future sell orders to submit to API.', NULL, NULL)
        print(str(datetime.now()) + ': Updated database queue for future sell orders to submit to API.')

        db.call_store_procedure(db_conn, 'update_queue_buy')
        # db.insert_run_log(db_conn, str(datetime.now()), 'Updated database queue for future buy orders to submit to API.', NULL, NULL)
        print(str(datetime.now()) + ': Updated database queue for future buy orders to submit to API.')

        time.sleep(6)

    sell_order = db.order_rule(db_conn,'sell')
    buy_order = db.order_rule(db_conn,'buy')
    # db.insert_run_log(db_conn, str(datetime.now()), 'Retrieved rules for buy and sell orders from database.', NULL, NULL)
    print(str(datetime.now()) + ': Retrieved rules for buy and sell orders from database.')

    open_orders = api.list_orders(status='open')
    open_positions = api.list_positions()
    account = api.get_account()
    order_type = 'limit'
    # db.insert_run_log(db_conn, str(datetime.now()), 'Retrieved current open orders and open positions from API.', NULL, NULL)
    print(str(datetime.now()) + ': Retrieved current open orders and open positions from API.')

    so.sellOrder(sell_order, account, open_orders, open_positions, lapse, api, order_type, db_conn)

    bo.buyOrder(buy_order, account, open_orders, open_positions, lapse, api, order_type, db_conn)

db_conn.close()




