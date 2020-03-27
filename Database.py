import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def connect():
    conn = mysql.connector.connect(
        host = os.getenv('DB_SERVER'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME')
    )
    return conn

def insert_filled_order(db_conn, value):
    insert = "INSERT INTO filled_order_stage (asset_class, asset_id, canceled_at, client_order_id, created_at, expired_at, failed_at, filled_at, filled_avg_price, " \
             "filled_qty, id, limit_price, order_type, qty, side, status, stop_price, submitted_at, symbol, time_in_force, type, updated_at, filled_at_east_std_time)"
    add_filled_order = f'{insert} values {value}'
    cursor = db_conn.cursor()
    cursor.execute(add_filled_order)
    db_conn.commit()


def update():
    pass

def truncate(db_conn, table):
    cursor = db_conn.cursor()
    cursor.execute(f'TRUNCATE TABLE {table}')
    db_conn.commit()


def call_store_procedure(db_conn, name):
    cursor = db_conn.cursor()
    cursor.callproc(name)
    db_conn.commit()

def order_rule(db_conn, side):
    if side == 'buy':
        exe_stm = 'SELECT * FROM queue_buy'
    elif side == 'sell':
        exe_stm = 'SELECT * FROM queue_sell'
    cursor = db_conn.cursor()
    cursor.execute(exe_stm)
    return cursor.fetchall()


def insert_run_log(db_conn, run_time, run_message, run_error, run_notes):
    insert = "INSERT INTO run_log (run_time, run_message, run_error, run_notes)"
    insert_log = f"{insert} values ('{run_time}', '{run_message}', '{run_error}', '{run_notes}')"
    # print(insert_log)
    cursor = db_conn.cursor()
    cursor.execute(insert_log)
    db_conn.commit()

def execute_query(db_conn, exe_stm):
    cursor = db_conn.cursor()
    cursor.execute(exe_stm)
    return cursor.fetchall()

