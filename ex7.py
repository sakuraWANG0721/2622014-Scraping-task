import time
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup

# 練習問題：映画出演ページから作品名を集める
movie_url = "http://abehiroshi.la.coocan.jp/movie/eiga.htm"
movie_res = requests.get(movie_url, timeout=20)
movie_res.encoding = "shift_jis"
movie_soup = BeautifulSoup(movie_res.text, "html.parser")

print("阿部寛さんの映画出演タイトル")
for link in movie_soup.select("a"):
    title = link.get_text(strip=True)
    if title:
        print(title)

# 個別課題：武蔵野大学の同じドメインを調べる
start_url = "https://www.musashino-u.ac.jp/"
domain = urlparse(start_url).netloc
url_list = [start_url]
checked_url = set()
page_title = {}

# 別のサイトへ続けてアクセスしないよう、ここでも待つ
time.sleep(6)

while url_list:
    url = url_list.pop(0)
    url, _ = urldefrag(url)

    if url in checked_url:
        continue
    checked_url.add(url)

    # 2ページ目以降は6秒待ってからアクセスする
    if len(checked_url) > 1:
        time.sleep(6)

    try:
        res = requests.get(url, timeout=20)
    except requests.RequestException as error:
        print(f"アクセスできません: {url} ({error})")
        continue

    if urlparse(res.url).netloc != domain:
        continue

    content_type = res.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        continue

    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    if soup.title is not None:
        page_title[url] = soup.title.get_text(strip=True)
    else:
        page_title[url] = ""

    for link in soup.select("a[href]"):
        next_url = urljoin(url, link.get("href"))
        next_url, _ = urldefrag(next_url)
        if urlparse(next_url).netloc == domain and next_url not in checked_url:
            if next_url not in url_list:
                url_list.append(next_url)

print("武蔵野大学サイトのURLとタイトル")
print(page_title)
