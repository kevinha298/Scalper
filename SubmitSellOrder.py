import random
import datetime
import GetRealTimeQuote as realtime
import Database as db
import time
from datetime import datetime

def sellOrder(sell_order, account, open_orders, open_positions, lapse, api, order_type, db_conn):
    sell_order_list = list()
    for sell in sell_order:
        symbol = sell[0]
        sell_qty = sell[1]
        sell_price = float(sell[2])
        buy_sell_cents_buffer = sell[3]
        price_buffer = random.randrange(1, buy_sell_cents_buffer, 1) / 100

        open_order = [o for o in open_orders if o.symbol == f'{symbol}' and o.side == 'sell']
        if not open_order:
            real_time_price, percent_change, day_low = realtime.parsePrice(symbol, lapse)
            order_sell_price = round(real_time_price - price_buffer, 2)
            if float(order_sell_price) > sell_price:
                api.submit_order(symbol, sell_qty, 'sell', order_type, 'day', order_sell_price)
                db.insert_run_log(db_conn, str(datetime.now()), f'Submitted sell orders to API. symbol: {symbol}, price: {order_sell_price}, quantity: {sell_qty}, order type: {order_type}','', '')
                print(str(datetime.now()) + f': Submitted sell orders to API. symbol: {symbol}, price: {order_sell_price}, quantity: {sell_qty}, order type: {order_type}')
        # db.insert_run_log(db_conn, str(datetime.now()), f'Checked to {order_type} sell {sell_qty} share(s) of {symbol} at around {sell_price} per share.','', '')
        print(str(datetime.now()) + f': Checked to {order_type} sell {sell_qty} share(s) of {symbol} at around {sell_price} per share.')
        time.sleep(1)
    # return sell_order_list

