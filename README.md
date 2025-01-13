# DAILY_REPORT
日報をIssuesに書きます。

## 予定:
- 入浴履歴ダッシュボード
- Github Pagesでサイト化


# 入浴履歴ダッシュボードどうしよ
- Grafana DBにクエリを投げてデータをグラフとして可視化するツール
- Prometheus サーバーからリソース情報を取得して監視する。リミットを決められアラートを出せる

Grafana cloudの無料版はメトリクスが2週間みたい(2週間分1Grafana側キャッシュでデータを保持できる)
なので、長期的にデータを持ちたいときは外部DBが必要になる。
GrafanaCloud - DB - GithubActions - データ対象
みたいなデータの流れになると思う。

DB: PlanetScale or TiDB Serverless
PlanetScale無料版が2024/4月に終わるっぽい
TiDBServerlessはNewSQLらしい
NewSQLは RDBMS と NoSQLをいいとこ取りしてるらしい
DBのクラウドサービスをDBaaSというらしい

SaaS的な文脈でのストレージとデータベースって違うんですね...(GoogleDriveとDBみたいな...)

- TiDB:
Serverlessは「みんなで仲良くつかおう」に対して、Dedicatedは「専有で使おう」になります。AWS以外でGCPが選択できる。Node、CPU、RAMのチューニングができるというのが魅力ですね。料金は少しお高くなります。データは完全に利用者しか見えなくなりPingCAP様でも一切見えなくなる
https://zenn.dev/icck/articles/5bc716bbe18a3a

参考:
睡眠
ヘルスケア

# TiDB Serverless入門
- https://docs.pingcap.com/ja/tidb/stable/basic-sql-operations
- https://zenn.dev/icck/articles/5bc716bbe18a3a
- https://qiita.com/urachooooooo/items/8a5a0c9ed4bab551231a

- Dedicated 専有でAWS等のクラウドを使える(セキュリティ高)
- Serverless みんなでAWSのプールを共有する

- DB Table 作成 クラスタ内のSQL Editor
たぶんMySQLで書く?
- SQL Editor内の左矢印(Expand)を押すとSchemeが見れる

- Diagnosis → SQL Statement でクエリの実行速度を見れる

- 右上の設定歯車 → show syste database schema を押すとschema一覧にTiDB自体のシステム系スキーマが表示される

- **TiDB Editorでは各クエリごとに区分けされているので、実行をしたときにファイル内の全コードを実行しているわけではない　クエリとして解釈できるコードブロックごとに実行する　そのため複数行に複数クエリを記入することが可能 (ちゃんと文末を;で区切ること)**


- **全実行する倍は、ctrl+Aで全選択してから実行を行う**


## SQL自体の関数のカテゴリ
- DDL (データ定義言語): データベース、テーブル、ビュー、インデックスなどのデータベース オブジェクトを定義するために使用されます。
- DML (データ操作言語): アプリケーション関連のレコードを操作するために使用されます。
- DQL (データ クエリ言語): 条件付きフィルタリング後にレコードをクエリするために使用されます。
- DCL (データ制御言語): アクセス権限とセキュリティ レベルを定義するために使用されます。

一般的な DDL 機能は、オブジェクト (テーブルやインデックスなど) の作成、変更、削除です。対応するコマンドはCREATE 、 ALTER 、 DROPです。

## SQL

- 構成  
DB > Table

- DB指定
```
use [DB名]
```

- DB確認
```
SHOW DATABASES
```

- INFORMATION_SCHEMA
- PERFORMANCE_SCHEMA
- mysql
上以外が作成したDB

- テーブル確認
```
use test;
SHOW TABLES

or 

show TABLES from test
```

- daily用DB作成
```
CREATE DATABASE `daily`;


-- zerofillは非推奨になった
use daily;
CREATE TABLE
  `bath` (
    `id` int(8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `date` date NOT NULL,
    `is_bathed` BOOLEAN NOT NULL
  );

DROP TABLE bath;

INSERT INTO
  `bath` (date, is_bathed)
VALUES
  ('2000-01-01', TRUE);

SELECT
  *
FROM
  `bath`;
```


# Actions
Actionsでボタンを押したらpythonが動く
PythonでDBにデータをinsert
ライブラリはpymysqlを使用

issueからテキスト(markdown)を取得
パース
markdownをパース?
insert

[pythonからdbに接続](https://zenn.dev/icck/articles/c4344f75460b53)
[codespacesからpythonを実行](https://docs.github.com/ja/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces#step-1-open-the-project-in-a-codespace)

[actionsからgithub secret呼び出し、pythonで使用](https://qiita.com/Wallaby19/items/7a9f2e514cd2e10d8b42)