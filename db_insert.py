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
from datetime import datetime
from datetime import date

DATE_RANGE = 30


# .envファイルで環境変数を上書き
load_dotenv()

# SQLAlchemyはORMで便利に操作できそうだが、SQLのクエリを学習したいため
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

# issueの入浴をパース
# date - is_bathed を紐付ける
# 最新の日付のみパース
# DBに入っていない過去の日付もパース
# とりまパース
# actions→python
# github scriptでissueのリストを取得
# github rest API
# 日時のリスト　→　テキスト　→　パース?


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


# gh issue listでbodyまで取得できた
cmd = f'gh issue list --repo https://github.com/masirof/DAILY_REPORT.git --author github-actions[bot] --json number,title,body --limit {DATE_RANGE}'
process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           shell=True).communicate()[0]).decode('utf-8')

csv_output = StringIO(process)
json_reader = json.load(csv_output)
print(json_reader)


# ❗unicode正規化するとよい
# normalized_json = unicodedata.normalize('NFKC', json_reader['body'])
# ic(normalized_json)

# 風呂、本を読む、プログラミング、懸垂回数をパース
is_bathed_re = re.findall(r'\[(x|X)\].*?風呂', json_reader['body'], re.MULTILINE)
is_read_book_re = re.findall(r'\[(x|X)\].*?本を読む', json_reader['body'], re.MULTILINE)
is_programming_re = re.findall(r'\[(x|X)\].*?プログラミング', json_reader['body'], re.MULTILINE)
pull_up_re = re.findall(r'懸垂.*?`(\d{1,2})`.*?回', json_reader['body'], re.MULTILINE)

is_bathed = True if is_bathed_re else False
is_read_book = True if is_bathed_re else False
is_programming = True if is_programming_re else False

if pull_up_re:
    pull_up_count = pull_up_re[0]
else:
    pull_up_count = 0

insert_data = []


ic(pull_up_count, is_bathed, is_read_book, is_programming)
ic(json_reader['title'])


insert_data = [
    ('2000-01-03', True, True, True, 3),
    ('2000-01-04', True, True, True, 3)
]


# ❗upsert
# ❗onduplicate key update.
# ❗全部の値が同じなら更新しない


# DB insert&update
with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        # VALUES(date)がpython側の変数
        # dateがDB側のレコード値
        query = f"""
            INSERT INTO
                daily_logs (date, is_bathed, is_read_book, is_programming, pull_up_count)
                VALUES(%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                date = IF(date <> VALUES(date), VALUES(date), date)
                is_bathed = IF(is_bathed <> VALUES(is_bathed), VALUES(is_bathed), is_bathed)
                is_read_book = IF(is_read_book <> VALUES(is_read_book), VALUES(is_read_book), is_read_book)
                is_programming = IF(is_programming <> VALUES(is_programming), VALUES(is_programming), is_programming)
                pull_up_count = IF(pull_up_count <> VALUES(pull_up_count), VALUES(pull_up_count), pull_up_count)
        """
        cur.executemany(query, insert_data)
        DB_date_list = cur.fetchall()
DB_date_list = [v['date'] for v in DB_date_list]
ic(DB_date_list)






# # 30日分のissue_noとtitleを取得
# cmd = f'gh issue list --repo https://github.com/masirof/DAILY_REPORT.git --author github-actions[bot] --limit {DATE_RANGE}'
# # cmd = 'gh issue list --repo https://github.com/masirof/DAILY_REPORT.git --author github-actions[bot]'
# process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
#                            shell=True).communicate()[0]).decode('utf-8')
# csv_output = StringIO(process)
# csv_reader = csv.reader(csv_output, delimiter='\t')
# csv_lsit = list(csv_reader)

# gh_issueno_title = [[v[0], datetime.strptime(v[2], '%Y-%m-%d').date()] for v in csv_lsit]
# ic(gh_issueno_title)

# # 昨日のissuを番号を取得
# latest_issue_no =  gh_issueno_title[1][0]

# 差分処理
diff_issueno_title = [item for item in gh_issueno_title if item[1] not in DB_date_list]
ic(diff_issueno_title)

latest_issue_no =  63
latest_issue_no =  75
# ic(latest_issue_no)


cmd = f'gh issue view {latest_issue_no} --repo https://github.com/masirof/DAILY_REPORT.git --json title,body'
process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           shell=True).communicate()[0]).decode('utf-8')

csv_output = StringIO(process)
json_reader = json.load(csv_output)
print(json_reader)
print(json_reader['body'])




# with get_connection(autocommit=True) as conn:
#     with conn.cursor() as cur:
#         # cur.execute("INSERT INTO daily_logs (date, is_bathed) VALUES('2000-01-02', TRUE)")

#         # cur.executemany("INSERT INTO daily_logs (date, is_bathed, is_read_book, is_programming, pull_up_count) VALUES(%s, %s, %s, %s, %s)", insert_data)
#         cur.execute("SELECT * FROM daily_logs;")
#         ic(cur.fetchall())

# ❗泣いた
# 同じのを入れると一意じゃなくてエラーが出るぞ
# pymysql.err.IntegrityError: (1062, "Duplicate entry '?' for key '***_logs.unique_date'")