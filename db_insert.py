import os
import pymysql
from pymysql import Connection
from pymysql.cursors import DictCursor
import subprocess
import csv
from io import StringIO
import json

# MySQLDBとの接続
# SQLAlchemyはORMで便利に操作できそうだが、SQLのクエリを学習したいため'j'
# PyMySQLを仕様


print('hi')

def get_connection(autocommit: bool = True) -> Connection:
    # actionsのsecretsに登録した環境変数の呼び出し
    TIDB_HOST = os.environ.get("TIDB_HOST")
    TIDB_PORT = int(os.environ.get("TIDB_PORT"))
    TIDB_USER = os.environ.get("TIDB_USER")
    TIDB_PASSWORD = os.environ.get("TIDB_PASSWORD")
    TIDB_DB_NAME = os.environ.get("TIDB_DB_NAME")
    TIDB_CA_PATH = os.environ.get("TIDB_CA_PATH")

    db_conf = {
        "host": TIDB_HOST,
        "port": TIDB_PORT,
        "user": TIDB_USER,
        "password": TIDB_PASSWORD,
        "database": TIDB_DB_NAME,
        "autocommit": autocommit,
        "cursorclass": DictCursor,
    }

    if TIDB_CA_PATH:
        db_conf["ssl_verify_cert"] = True
        db_conf["ssl_verify_identity"] = True
        db_conf["ssl_ca"] = TIDB_CA_PATH

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


# cmd = 'gh issue list --repo https://github.com/masirof/DAILY_REPORT.git --author github-actions[bot] --limit 30'
# process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
#                            shell=True).communicate()[0]).decode('utf-8')
# csv_output = StringIO(process)
# csv_reader = csv.reader(csv_output, delimiter='\t')
# csv_lsit = list(csv_reader)

# issue_num_title = [[v[0],v[2]] for v in csv_lsit]
# print(issue_num_title[0:10])

# # 昨日のissuを番号を取得
# issue_num =  issue_num_title[1][0]
issue_num =  74
# print(issue_num)


cmd = f'gh issue view {issue_num} --repo https://github.com/masirof/DAILY_REPORT.git --json title,body'
process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           shell=True).communicate()[0]).decode('utf-8')
csv_output = StringIO(process)
# csv_reader = csv.reader(csv_output, delimiter=' ')
json_reader = json.load(csv_output)
# csv_reader = csv.reader(csv_output)
# csv_lsit = list(csv_reader)
print(json_reader)
print(json_reader['body'])



# get issue body(return:json)
# run: gh issue view --repo https://github.com/masirof/DAILY_REPORT.git --author github-actions[bot] --json title,body

# with get_connection(autocommit=True) as conn:
#     with conn.cursor() as cur:
#         # cur.execute("SELECT * FROM bath;")
#         # cur.execute("INSERT INTO bath (date, is_bathed) VALUES('2000-01-02', TRUE)")
#         # print(cur.fetchall())