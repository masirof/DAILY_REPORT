import os
import pymysql
from pymysql import Connection
from pymysql.cursors import DictCursor

# MySQLDBとの接続
# SQLAlchemyはORMで便利に操作できそうだが、SQLのクエリを学習したいため
# PyMySQLを仕様

# actionsのsecretsに登録した環境変数の呼び出し
TIDB_HOST = os.environ.get("TIDB_HOST")
TIDB_PORT = int(os.environ.get("TIDB_PORT"))
TIDB_USER = os.environ.get("TIDB_USER")
TIDB_PASSWORD = os.environ.get("TIDB_PASSWORD")
TIDB_DB_NAME = os.environ.get("TIDB_DB_NAME")
TIDB_CA_PATH = os.environ.get("TIDB_CA_PATH")

print('hi')


def get_connection(autocommit: bool = True) -> Connection:
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

with get_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM bath;")
        print(cur.fetchall())