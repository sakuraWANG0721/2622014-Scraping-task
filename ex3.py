import requests


url = "https://ja.wikipedia.org/w/index.php"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

params = {
    "title": "武蔵野大学",
    "oldid": "100769128",
    "action": "history",
}

res = requests.get(url, params=params, headers=headers, timeout=15)

print(f"レスポンス: {res}")
print(f"ステータスコード: {res.status_code}")
print(f"ステータスメッセージ: {res.reason}")
print(f"リクエストヘッダー: {res.request.headers}")
print(f"リクエストのURL: {res.request.url}")

with open("wiki-musashino-history.html", "w") as f:
    f.write(res.text)
