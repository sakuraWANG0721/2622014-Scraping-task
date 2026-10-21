import requests


#アクセスしたいWebサイトのURL
url = "https://www.musashino-u.ac.jp"

# Webサーバにリクエストを出す
# レスポンスを変数に格納しておく
res = requests.get(url, timeout=15)

# 取得したHTMLデータは、res.textに保存されている
print(res.text)

# 取得したHTMLをファイルに書き込む
with open("musashino-u.html", "w") as f:
    f.write(res.text)
