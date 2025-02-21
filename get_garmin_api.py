import garminconnect
from dotenv import load_dotenv
import os
from icecream import ic
from datetime import datetime, date, timedelta, timezone
import pymysql
from pymysql import Connection
from pymysql.cursors import DictCursor

# .envファイルで環境変数を上書き
load_dotenv()

def get_connection(autocommit: bool = True) -> Connection:
    # actionsのsecretsに登録した環境変数の呼び出し
    TIDB_HOST = os.environ.get("TIDB_HOST")
    TIDB_PORT = int(os.environ.get("TIDB_PORT"))
    TIDB_USER = os.environ.get("TIDB_USER")
    TIDB_PASSWORD = os.environ.get("TIDB_PASSWORD")
    TIDB_DB_NAME = os.environ.get("TIDB_DB_NAME")
    TIDB_CA = os.environ.get("TIDB_CA")

    db_conf = {
        "host": TIDB_HOST,
        "port": TIDB_PORT,
        "user": TIDB_USER,
        "password": TIDB_PASSWORD,
        "database": TIDB_DB_NAME,
        "autocommit": autocommit,
        "cursorclass": DictCursor,
    }

    if TIDB_CA:
        db_conf["ssl_verify_cert"] = True
        db_conf["ssl_verify_identity"] = True
        # db_conf["ssl_ca"] = TIDB_CA
        db_conf["ssl_key_password"] = TIDB_CA

    return pymysql.connect(**db_conf)

# Garminへのログイン
def garmin_login():
    GARMIN_EMAIL = os.environ.get("GARMIN_EMAIL")
    GARMIN_PASS = os.environ.get("GARMIN_PASS")

    garmin = garminconnect.Garmin(GARMIN_EMAIL, GARMIN_PASS)
    garmin.login()
    ic(garmin.display_name)
    return garmin

# garmin_login()

yesterday = date.today() - timedelta(days=1)
yesterday_iso = yesterday.isoformat()

ic(yesterday)
ic(yesterday_iso)

# GMT(ほぼUTC)からJSTに変換
def GMT_to_JST(GMT_time):
    GMT_time_s = GMT_time/1000
    utc_time = datetime.fromtimestamp(GMT_time_s, tz=timezone.utc)

    jst = timezone(timedelta(hours=9))
    jst_time = utc_time.astimezone(jst)
    jst_time = jst_time.replace(tzinfo=None)
    return jst_time

def insert_yesterday():
    sleep = garmin.get_sleep_data(yesterday)
    # ic(sleep['dailySleepDTO'])
    sleep_start_gmt = sleep['dailySleepDTO']['sleepStartTimestampGMT']
    sleep_end_gmt = sleep['dailySleepDTO']['sleepEndTimestampGMT']
    sleep_sec = sleep['dailySleepDTO']['sleepTimeSeconds']
    sleep_hours = sleep_sec/3600

def insert_n_day(n_day:int):
    yesterday = date.today() - timedelta(days=1)
    yesterday_iso = yesterday.isoformat()
    for v in range(n_day):
        ic(yesterday_iso)
        yesterday = yesterday - timedelta(days=1)
        yesterday_iso = yesterday.isoformat()
    # sleep = garmin.get_sleep_data(yesterday)
    # # ic(sleep['dailySleepDTO'])
    # sleep_start_gmt = sleep['dailySleepDTO']['sleepStartTimestampGMT']
    # sleep_end_gmt = sleep['dailySleepDTO']['sleepEndTimestampGMT']
    # sleep_sec = sleep['dailySleepDTO']['sleepTimeSeconds']
    # sleep_hours = sleep_sec/3600


# insert_yesterday()
insert_n_day(10)

ic(sleep['dailySleepDTO']['sleepStartTimestampGMT'])
print("JST:", GMT_to_JST(sleep_start_gmt))
print("JST:", GMT_to_JST(sleep_end_gmt))
ic(sleep_hours)

ic(yesterday)

# DBに入れるデータ整形
insert_data = []



# # DB insert&update &全部の値が同じなら更新しない
# with get_connection(autocommit=True) as conn:
#     with conn.cursor() as cur:
#         # VALUES(date)がpython側の変数
#         # dateがDB側のレコード値
#         query = f"""
#             INSERT INTO
#                 daily_logs (date, is_bathed, is_read_book, is_programming, pull_up_count)
#                 VALUES(%s, %s, %s, %s, %s)
#             ON DUPLICATE KEY UPDATE
#                 is_bathed = IF(is_bathed <> VALUES(is_bathed), VALUES(is_bathed), is_bathed),
#                 is_read_book = IF(is_read_book <> VALUES(is_read_book), VALUES(is_read_book), is_read_book),
#                 is_programming = IF(is_programming <> VALUES(is_programming), VALUES(is_programming), is_programming),
#                 pull_up_count = IF(pull_up_count <> VALUES(pull_up_count), VALUES(pull_up_count), pull_up_count)
#         """
#         cur.executemany(query, insert_data)