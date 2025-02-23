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

yesterday = date.today() - timedelta(days=1)
yesterday_iso = yesterday.isoformat()
today_iso = date.today().isoformat()

# ic(yesterday)
# ic(yesterday_iso)

# # DBにはUTCで保存すること!!
# # GMT(ほぼUTC)からJSTに変換
# def GMT_to_JST(GMT_time):
#     GMT_time_s = GMT_time/1000
#     utc_time = datetime.fromtimestamp(GMT_time_s, tz=timezone.utc)

#     jst = timezone(timedelta(hours=9))
#     jst_time = utc_time.astimezone(jst)
#     jst_time = jst_time.replace(tzinfo=None)
#     return jst_time

def GMT_to_UTC(GMT_time):
    GMT_time_s = GMT_time/1000
    utc_time = datetime.fromtimestamp(GMT_time_s, tz=timezone.utc)
    return utc_time

def insert_yesterday():
    insert_data = []
    sleep = garmin.get_sleep_data(yesterday_iso)
    # ic(sleep['dailySleepDTO'])
    sleep_start_gmt = sleep['dailySleepDTO']['sleepStartTimestampGMT']
    sleep_end_gmt = sleep['dailySleepDTO']['sleepEndTimestampGMT']
    sleep_sec = sleep['dailySleepDTO']['sleepTimeSeconds']
    
    if sleep_start_gmt:
        sleep_start_utc = GMT_to_UTC(sleep_start_gmt)
    if sleep_end_gmt:
        sleep_end_utc = GMT_to_UTC(sleep_end_gmt)
    if sleep_sec:
        sleep_hours = sleep_sec/3600

    if sleep_start_gmt or sleep_end_gmt or sleep_sec:
        insert_data.append([yesterday_iso, sleep_start_utc, sleep_end_utc, sleep_hours])
    return insert_data

def insert_n_day(n_day:int, yesterday, yesterday_iso):
    insert_data = []
    for v in range(n_day):
        # ic(yesterday_iso)
        sleep = garmin.get_sleep_data(yesterday_iso)
        sleep_start_gmt = sleep['dailySleepDTO']['sleepStartTimestampGMT']
        sleep_end_gmt = sleep['dailySleepDTO']['sleepEndTimestampGMT']
        sleep_sec = sleep['dailySleepDTO']['sleepTimeSeconds']
        
        # sleep_start_utc = sleep_start_gmt if sleep_start_gmt else None
        # sleep_end_utc = sleep_end_gmt if sleep_end_gmt else None
        # sleep_hours = sleep_sec/3600 if sleep_sec else None
        if sleep_start_gmt:
            sleep_start_utc = GMT_to_UTC(sleep_start_gmt)
        if sleep_end_gmt:
            sleep_end_utc = GMT_to_UTC(sleep_end_gmt)
        if sleep_sec:
            sleep_hours = sleep_sec/3600
        
        if sleep_start_gmt or sleep_end_gmt or sleep_sec:
            insert_data.append([yesterday_iso, sleep_start_utc, sleep_end_utc, sleep_hours])
        
        yesterday = yesterday - timedelta(days=1)
        yesterday_iso = yesterday.isoformat()
        # sleep()
    return insert_data
    # sleep = garmin.get_sleep_data(yesterday)
    # # ic(sleep['dailySleepDTO'])
    # sleep_start_gmt = sleep['dailySleepDTO']['sleepStartTimestampGMT']
    # sleep_end_gmt = sleep['dailySleepDTO']['sleepEndTimestampGMT']
    # sleep_sec = sleep['dailySleepDTO']['sleepTimeSeconds']
    # sleep_hours = sleep_sec/3600


garmin = garmin_login()

# 昨日をDBに入れる
# insert_data = insert_yesterday()
# ic(insert_data)

# n_day分DBに入れる
insert_data = insert_n_day(15, yesterday, yesterday_iso)
ic(insert_data)

# ic(sleep['dailySleepDTO']['sleepStartTimestampGMT'])
# print("JST:", GMT_to_utc(sleep_start_gmt))
# print("JST:", GMT_to_utc(sleep_end_gmt))
# ic(sleep_hours)

# ic(yesterday)


# DB insert&update &全部の値が同じなら更新しない
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        # VALUES(date)がpython側の変数
        # dateがDB側のレコード値
        query = f"""
            INSERT INTO
                garmin (date, sleep_start_utc, sleep_end_utc, sleep_hours)
                VALUES(%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                sleep_start_utc = IF(sleep_start_utc <> VALUES(sleep_start_utc), VALUES(sleep_start_utc), sleep_start_utc),
                sleep_end_utc = IF(sleep_end_utc <> VALUES(sleep_end_utc), VALUES(sleep_end_utc), sleep_end_utc),
                sleep_hours = IF(sleep_hours <> VALUES(sleep_hours), VALUES(sleep_hours), sleep_hours)
        """
        cur.executemany(query, insert_data)
