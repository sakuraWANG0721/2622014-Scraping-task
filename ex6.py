from bs4 import BeautifulSoup
import requests

# 自分で作ったHTMLファイルを読む
with open("test.html", "r", encoding="utf-8") as f:
    html = f.read()

html_soup = BeautifulSoup(html, "html.parser")

print("idでリンクを探す")
print(html_soup.select("#study-link"))

print("classで授業メモを探す")
print(html_soup.select(".study-note"))

print("HTMLの順番を指定して見出しを探す")
print(html_soup.select("body > div > div.study-note > h1"))

print("授業メモの2つ目の段落を探す")
print(html_soup.select("body > div > div.study-note > p:nth-of-type(2)"))

# 大学のページでもCSSセレクタを試す
url = "https://www.musashino-u.ac.jp"
res = requests.get(url, timeout=15)
res.encoding = res.apparent_encoding
web_soup = BeautifulSoup(res.text, "html.parser")

print(f"ステータスコード: {res.status_code}")
print("大学ページの紹介文")
intro_list = web_soup.select("p.p-introduction__detail.u-text")
for intro in intro_list:
    print(intro.get_text(strip=True))
