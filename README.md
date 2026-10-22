# 2622014-Scraping-task

DS Programming のスクレイピング練習コードです。

- `ex2.py`〜`ex7.py`: 授業の練習
- `test.html`: ex4〜ex6で使う自作HTML
- `example1.py`: HTTPリクエストの練習
- `musashino_site_map.csv`: 武蔵野大学トップページから見つけた同じドメインのURLとページタイトル

Python環境に `requests` と `beautifulsoup4` をインストールして実行してください。

`ex7.py` は映画ページの作品名を表示し、武蔵野大学トップページ内の同じドメインのリンク先を確認します。各ページにアクセスする前に6秒待ち、取得したURLとタイトルを `musashino_site_map.csv` に保存します。
