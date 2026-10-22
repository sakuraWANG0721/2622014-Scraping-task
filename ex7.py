import csv
import time
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def get_page(url):
    """ページにアクセスする前に6秒待つ。"""
    time.sleep(6)
    return requests.get(url, timeout=20)


def save_csv(page_title):
    """現在までに取得したURLとタイトルをCSVに保存する。"""
    with open("musashino_site_map.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "title"])
        for url, title in page_title.items():
            writer.writerow([url, title])


# 練習問題：阿部寛さんの映画出演ページから作品名を集める
movie_url = "http://abehiroshi.la.coocan.jp/movie/eiga.htm"
try:
    movie_res = get_page(movie_url)
    movie_res.encoding = movie_res.apparent_encoding
    movie_soup = BeautifulSoup(movie_res.text, "html.parser")

    print("阿部寛さんの映画出演タイトル")
    for link in movie_soup.select("a"):
        title = link.get_text(strip=True)
        if title:
            print(title)
except requests.RequestException as error:
    print(f"映画ページにアクセスできません: {error}")


# 個別課題：武蔵野大学トップページから同じドメインのリンクを調べる
start_url = "https://www.musashino-u.ac.jp/"
domain = urlparse(start_url).netloc
page_title = {}

try:
    home_res = get_page(start_url)
    home_res.encoding = home_res.apparent_encoding
    home_soup = BeautifulSoup(home_res.text, "html.parser")
except requests.RequestException as error:
    print(f"大学トップページにアクセスできません: {error}")
    raise SystemExit(1)

if home_soup.title is not None:
    page_title[start_url] = home_soup.title.get_text(strip=True)
    save_csv(page_title)

# トップページにある同じドメインのURLを重複しないように集める
url_list = []
for link in home_soup.select("a[href]"):
    next_url = urljoin(start_url, link.get("href"))
    next_url, _ = urldefrag(next_url)
    if urlparse(next_url).netloc == domain and next_url not in url_list:
        url_list.append(next_url)

print(f"トップページから見つかった同じドメインのリンク: {len(url_list)}件", flush=True)

# 各リンク先を6秒間隔で確認し、取得したタイトルをその都度CSVに保存する
for number, url in enumerate(url_list, start=1):
    try:
        res = get_page(url)
    except requests.RequestException as error:
        print(f"{number}/{len(url_list)} アクセス失敗: {url} ({error})", flush=True)
        continue

    if urlparse(res.url).netloc != domain:
        print(f"{number}/{len(url_list)} 別ドメインへ移動したため除外: {url}", flush=True)
        continue
    if "text/html" not in res.headers.get("Content-Type", ""):
        print(f"{number}/{len(url_list)} HTMLではないため除外: {url}", flush=True)
        continue

    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")
    page_title[url] = soup.title.get_text(strip=True) if soup.title else ""
    save_csv(page_title)
    print(f"{number}/{len(url_list)} 取得済み: {url}", flush=True)

print(f"完了: {len(page_title)}ページのURLとタイトルを musashino_site_map.csv に保存しました")
