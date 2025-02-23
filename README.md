# DAILY_REPORT

日報をIssuesに書きます。

# SRE
## SLI(Service Level Indicator) 指標
- 爆睡率= $睡眠できた日数\over全日数$
  - 8時間睡眠とする
- 早寝率= $早寝できた日数\over全日数$
  - 23時までの入眠とする
- 早起き率= $早起きできた日数\over全日数$
  - 7時までの起床とする
- 入浴率= $入浴できた日数\over全日数$

## SLO(Service Level Objective) 目標値
- 爆睡率>=80%
  - 1週間に6日は達成したい
- 早寝率>=70%
  - 1週間に5日は達成したい
- 早起き率>=70%
  - 1週間に5日は達成したい
- 入浴率>=90%
  - 30日中27日は達成したい

## SLA（Service Level Agreement）外部との契約
- 爆睡率>=80% 未達
  - ペナルティ 入浴を行い、寝る1時間前のデジタルデバイスを禁止します。(読書は可)
- 早寝率>=70% 未達
  - ペナルティ 30分早めの行動に変更
- 早起き率>=70% 未達
  - ペナルティ10,000lux以上の照光機、自動昇降ベッドの導入
- 入浴率>=90% 未達
  - ペナルティ 帰宅中に泥をかぶる or 水たまりちゃぷちゃぷを行い帰宅後に入浴を行います。

## エラーバジェット
- 爆睡率>=80%
  - 月6回まで未達ok
- 早寝率>=70%
  - 月9日まで未達OK
- 早起き率>=70%
  - 月9日まで未達OK
- 入浴率>=90%
  - 月3日まで未達OK

- 一つでも指標のSLOを下回った場合、反省・対策を行います。
- 

## 各指標の考察
- お風呂に入る→眠くなる→早寝率が上がる
- 早寝率が上がる→爆睡率が上がる
- 風呂に入るまでの時間で爆睡率が変化するのでは?

## 運用
- ダッシュボードで監視を行います。
- 有給休暇を取得し、コードレッドの発令

使用可能数 / 全期間
# 計画
- Garmin 睡眠時間
- ゲームデータ
- 

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

- 構成DB > Table
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

bathテーブルをdaily_logsテーブルに変更

```
ALTER TABLE bath RENAME TO daily_logs;
```

- カラム情報表示

```
SELECT 
    COLUMN_NAME, 
    COLUMN_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT, 
    CHARACTER_SET_NAME, 
    COLLATION_NAME, 
    COLUMN_KEY, 
    EXTRA 
FROM information_schema.COLUMNS 
WHERE TABLE_NAME = 'daily_logs';
```

- dateカラムにunique属性追加

```
ALTER TABLE daily_logs 
ADD CONSTRAINT unique_date UNIQUE (date);
```

- カラム追加

```
ALTER TABLE daily_logs 
ADD COLUMN is_read_book BOOLEAN NOT NULL DEFAULT 0;
```

- テーブル作成
```
use daily;
CREATE TABLE
  `garmin` (
    `id` int(8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `date` date NOT NULL UNIQUE,
    `sleep_start_jst` DATETIME,
    `sleep_end_jst` DATETIME,
    `sleep_hours` DECIMAL(4,2) UNSIGNED
  );
```

- column typeがdateにstrを入れるとdate型に変換してくれる

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

# python

github codespaceで頑張ってたけど、ghコマンドをcodespaceに入れる方法がわからず、ローカルでpython環境を作成する

```
sudo apt update'j
sudo apt install python3.12 -y
python3 --version
sudo apt install python3-pip

# uv(linux)
wget -qO- https://astral.sh/uv/install.sh | sh
# curl -LsSf https://astral.sh/uv/install.sh | sh

# uv(windows)
winget install --id astral-sh.uv

# github cli(windows)
winget install --id GitHub.cli

uv init --python 3.12
# uv sync
uv venv


source ./.venv/bin/activate
uv add hoge

```

uv pip compile pyproject.toml > requirements.txt

# grafana
- ユーザーアイコン→profile→Preferences→timezone をasia/tokyoに変更しJSTを扱えるようにする

# Github Actionのpem
- Repository secretsに入れるときは普通に.pemをコピペすればよい

# garmin
Garminは無料でAPIを公開していないぞ！

- Garmin Health API
  - 全データ取得可能かつ無料ですが，企業向けのため利用不可

サードパーティ
- GarminDB https://github.com/tcgoetz/GarminDB
- garminconnect https://github.com/cyberjunky/python-garminconnect
- 手法としてはgarmin connectウェブページからスクレイピングする感じ

- garminconnectをインストールする際のwithings-syncでcp932のエラーが出る
  - set PYTHONUTF8=1 して解決