import random
import datetime
import GetRealTimeQuote as realtime
import Database as db
import time
from datetime import datetime

def buyOrder(buy_order, account, open_orders, open_positions, lapse, api, order_type, db_conn):
    for buy in buy_order:
        symbol = buy[0]
        buy_qty = buy[1]
        buy_price = float(buy[2])
        max_position_qty = buy[3]
        max_buy_price = buy[4]
        min_buy_price = buy[5]
        buy_sell_cents_buffer = buy[6]
        price_buffer = random.randrange(1, buy_sell_cents_buffer, 1) / 100

        open_order = [o for o in open_orders if o.symbol == f'{symbol}' and o.side == 'buy']
        max_position = [p for p in open_positions if p.symbol == f'{symbol}' and (int(p.qty) + buy_qty) > max_position_qty]
        buying_power = account.buying_power
        buying_cash = account.cash

        # Check to make sure there is NO pending open buy order for the same symbol and the position size of the same symbol had not reached the limit defined in rule.
        if not open_order and not max_position:
            real_time_price, percent_change, day_low = realtime.parsePrice(symbol, lapse)
            order_buy_price = round(real_time_price + price_buffer, 2)

            #Calculate of current price is 5% lower than closing price of previous day and current price is 0.05 higher than day low and current price is less than day low plus 0.12.
            if buy_price == 0:
                order_buy_price = buy_price
                if percent_change < -5.0:
                    if (real_time_price - day_low) > 0.05 and (real_time_price - day_low) < 0.12:
                        order_buy_price = round(real_time_price + price_buffer, 2)

            # Check to make sure there is suffice buying power and cash.
            if (float(buy_qty) * float(order_buy_price)) < float(buying_power) and (float(buy_qty) * float(order_buy_price)) < float(buying_cash):

                # Check to make sure order met all conditions defined in rule.
                if float(order_buy_price) < float(buy_price) and float(order_buy_price) > float(min_buy_price) and float(order_buy_price) < float(max_buy_price):
                    #This is a safety check.
                    if order_buy_price < 80 and buy_qty < 2000:
                        api.submit_order(symbol, buy_qty, 'buy', order_type, 'day', order_buy_price)
                        db.insert_run_log(db_conn, str(datetime.now()),f'Submitted buy orders to API. symbol: {symbol}, price: {order_buy_price}, quantity: {buy_qty}, order type: {order_type}','', '')
                        print(str(datetime.now()) + f': Submitted buy orders to API. symbol: {symbol}, price: {order_buy_price}, quantity: {buy_qty}, order type: {order_type}')
                        # print(f'prev_buy_sell_price: {prev_buy_sell_price}, real_time_price: {real_time_price}, buy_price_increment: {buy_price_increment}, order_buy_price: {order_buy_price}')
                        # print(f'min_buy_price: {min_buy_price}, max_buy_price: {max_buy_price}')
        # db.insert_run_log(db_conn, str(datetime.now()),f'Checked to {order_type} buy {buy_qty} share(s) of {symbol} around {buy_price} per share.','', '')
        print(str(datetime.now()) + f': Checked to {order_type} buy {buy_qty} share(s) of {symbol} around {buy_price} per share.')
        time.sleep(1)



