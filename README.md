# 2622014-Scraping-task

DS Programming のスクレイピング練習コードです。

- `ex2.py`〜`ex7.py`: 授業の練習
- `test.html`: ex4〜ex6で使う自作HTML
- `example1.py`: HTTPリクエストの練習
- `musashino_site_map.csv`: 武蔵野大学サイト内で見つけたURLとページタイトル

Python環境に `requests` と `beautifulsoup4` をインストールして実行してください。

`ex7.py` は映画ページの作品名を表示します。その後、武蔵野大学のトップページから同じドメインのリンクをたどり、見つかったHTMLページからも次のリンクを集めます。各ページにアクセスする前に6秒待ち、URLとページタイトルを `musashino_site_map.csv` に保存します。取得中も10ページごとに途中結果を保存します。
