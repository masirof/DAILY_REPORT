import os
import pymysql
from pymysql import Connection
from pymysql.cursors import DictCursor
import subprocess
import csv
from io import StringIO
import json
import re
import unicodedata
import pandas as pd
from icecream import ic
from dotenv import load_dotenv
from datetime import datetime, date

# 更新する期間
DATE_RANGE = 100


# .envファイルで環境変数を上書き
load_dotenv()

# TiDBへの接続
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


# gh issue listでissueのbodyまで取得
cmd = f'gh issue list --repo https://github.com/masirof/DAILY_REPORT.git --author github-actions[bot] --json number,title,body --limit {DATE_RANGE}'
process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           shell=True).communicate()[0]).decode('utf-8')

csv_output = StringIO(process)
json_reader = json.load(csv_output)
print(json_reader)


# ❗unicode正規化するとよい
# normalized_json = unicodedata.normalize('NFKC', json_reader['body'])
# ic(normalized_json)
insert_data = []

for json in json_reader:
    # 風呂、本を読む、プログラミング、懸垂回数をパース
    is_bathed_re = re.findall(r'\[(x|X)\].*?風呂', json['body'], re.MULTILINE)
    is_read_book_re = re.findall(r'\[(x|X)\].*?本を読む', json['body'], re.MULTILINE)
    is_programming_re = re.findall(r'\[(x|X)\].*?プログラミング', json['body'], re.MULTILINE)
    pull_up_re = re.findall(r'懸垂.*?`(\d{1,2})`.*?回', json['body'], re.MULTILINE)

    is_bathed = True if is_bathed_re else False
    is_read_book = True if is_bathed_re else False
    is_programming = True if is_programming_re else False

    if pull_up_re:
        pull_up_count = int(pull_up_re[0])
    else:
        pull_up_count = 0

    # if is_bathed or is_read_book or is_programming or pull_up_count:
    insert_data.append((json['title'], is_bathed, is_read_book, is_programming, pull_up_count))

ic(insert_data)



# DB insert&update &全部の値が同じなら更新しない
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        # VALUES(date)がpython側の変数
        # dateがDB側のレコード値
        query = f"""
            INSERT INTO
                daily_logs (date, is_bathed, is_read_book, is_programming, pull_up_count)
                VALUES(%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                is_bathed = IF(is_bathed <> VALUES(is_bathed), VALUES(is_bathed), is_bathed),
                is_read_book = IF(is_read_book <> VALUES(is_read_book), VALUES(is_read_book), is_read_book),
                is_programming = IF(is_programming <> VALUES(is_programming), VALUES(is_programming), is_programming),
                pull_up_count = IF(pull_up_count <> VALUES(pull_up_count), VALUES(pull_up_count), pull_up_count)
        """
        cur.executemany(query, insert_data)

# # 30日分の日付を取得
# with get_connection(autocommit=True) as conn:
#     with conn.cursor() as cur:
#         query = f"""
#             SELECT
#                 date
#             FROM
#                 daily_logs
#             order by date DESC
#             limit {DATE_RANGE}
#         """
#         cur.execute(query)
#         DB_date_list = cur.fetchall()
# DB_date_list = [v['date'] for v in DB_date_list]
# ic(DB_date_list)