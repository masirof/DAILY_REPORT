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
```

