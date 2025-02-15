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

# MySQLDBとの接続
# SQLAlchemyはORMで便利に操作できそうだが、SQLのクエリを学習したいため'j'
# PyMySQLを仕様


ic('hi')

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

# issueの入浴をパース
# date - is_bathed を紐付ける
# 最新の日付のみパース
# DBに入っていない過去の日付もパース
# とりまパース
# actions→python
# github scriptでissueのリストを取得
# github rest API
# 日時のリスト　→　テキスト　→　パース?

# 30日分
cmd = 'gh issue list --repo https://github.com/masirof/DAILY_REPORT.git --author github-actions[bot] --limit 30'
# cmd = 'gh issue list --repo https://github.com/masirof/DAILY_REPORT.git --author github-actions[bot]'
process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           shell=True).communicate()[0]).decode('utf-8')
csv_output = StringIO(process)
csv_reader = csv.reader(csv_output, delimiter='\t')
csv_lsit = list(csv_reader)

issue_num_title = [[v[0],v[2]] for v in csv_lsit]
ic(issue_num_title)

# 昨日のissuを番号を取得
latest_issue_num =  issue_num_title[1][0]

# 30日文
# issue_numから
for v in issue_num_title:
    ic(v[0])


latest_issue_num =  63
latest_issue_num =  75
# ic(latest_issue_num)


cmd = f'gh issue view {latest_issue_num} --repo https://github.com/masirof/DAILY_REPORT.git --json title,body'
process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           shell=True).communicate()[0]).decode('utf-8')

csv_output = StringIO(process)
json_reader = json.load(csv_output)
print(json_reader)
print(json_reader['body'])



# ❗unicode正規化するとよい
# normalized_json = unicodedata.normalize('NFKC', json_reader['body'])
# ic(normalized_json)

# 風呂、本を読む、プログラミング、懸垂回数をパース
is_bathed_re = re.findall(r'\[(x|X)\].*?風呂', json_reader['body'], re.MULTILINE)

is_read_book_re = re.findall(r'\[(x|X)\].*?本を読む', json_reader['body'], re.MULTILINE)

is_programming_re = re.findall(r'\[(x|X)\].*?プログラミング', json_reader['body'], re.MULTILINE)

pull_up_re = re.findall(r'懸垂.*?`(\d{1,2})`.*?回', json_reader['body'], re.MULTILINE)

if is_bathed_re:
    is_bathed = True
else:
    is_bathed = False

if is_read_book_re:
    is_read_book = True
else:
    is_read_book = False

if is_programming_re:
    is_programming = True
else:
    is_programming = False

if pull_up_re:
    pull_up_count = pull_up_re[0]
else:
    pull_up_count = 0

insert_data = []


ic(pull_up_count, is_bathed, is_read_book, is_programming)
ic(json_reader['title'])

# ❗dateは一意にしたほうがいいかも
# ❗一ヶ月分

insert_data = [
    ('2000-01-03', True, True, True, 3),
    ('2000-01-04', True, True, True, 3)
]

with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        # cur.execute("INSERT INTO daily_logs (date, is_bathed) VALUES('2000-01-02', TRUE)")
        
        # cur.executemany("INSERT INTO daily_logs (date, is_bathed, is_read_book, is_programming, pull_up_count) VALUES(?, ?, ?, ?, ?)", insert_data)
        
        # cur.executemany("INSERT INTO daily_logs (date, is_bathed, is_read_book, is_programming, pull_up_count) VALUES(%s, %s, %s, %s, %s)", insert_data)
        cur.execute("SELECT * FROM daily_logs;")
        ic(cur.fetchall())

# ❗泣いた
# 同じのを入れると一意じゃなくてエラーが出るぞ
# pymysql.err.IntegrityError: (1062, "Duplicate entry '?' for key '***_logs.unique_date'")