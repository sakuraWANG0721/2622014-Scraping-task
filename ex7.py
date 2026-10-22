import csv
import time
from collections import deque
from urllib.parse import urldefrag, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup


START_URL = "https://www.musashino-u.ac.jp/"
MOVIE_URL = "http://abehiroshi.la.coocan.jp/movie/eiga.htm"
CSV_FILE = "musashino_site_map.csv"
WAIT_SECONDS = 6
SAVE_EVERY = 10


def get_page(url):
    """ウェブページを待ち時間を入れて取得する。"""
    time.sleep(WAIT_SECONDS)
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except requests.RequestException as error:
        print(f"取得できませんでした: {url} ({error})", flush=True)
        return None


def get_movie_titles():
    """練習問題のページから映画タイトルを取り出す。"""
    response = get_page(MOVIE_URL)
    if response is None:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    titles = []
    for link in soup.find_all("a"):
        title = link.get_text(" ", strip=True)
        if title:
            titles.append(title)
    return titles


def is_same_site(url):
    """大学の同じホストにあるHTMLページかを確認する。"""
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https"):
        return False
    if parts.hostname != "www.musashino-u.ac.jp":
        return False

    # 文書以外のファイルはサイトマップのページに含めない。
    file_types = (
        ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
        ".css", ".js", ".zip", ".doc", ".docx", ".xls", ".xlsx",
        ".ppt", ".pptx", ".mp4", ".mp3", ".xml",
    )
    return not parts.path.lower().endswith(file_types)


def save_csv(page_titles):
    """今まで集めたURLとtitleをCSVに保存する。"""
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "title"])
        for url, title in page_titles.items():
            writer.writerow([url, title])


def crawl_site():
    """トップページから同じドメインのページを順番に調べる。"""
    start_url = urldefrag(START_URL)[0]
    waiting_urls = deque([start_url])
    checked_urls = set()
    page_titles = {}

    # 開始直後にも途中結果ファイルを作っておく。
    save_csv(page_titles)

    while waiting_urls:
        url = waiting_urls.popleft()
        if url in checked_urls:
            continue
        checked_urls.add(url)

        response = get_page(url)
        if response is None:
            page_titles[url] = ""
        else:
            page_url = urldefrag(response.url)[0]
            if page_url not in page_titles:
                checked_urls.add(page_url)
            content_type = response.headers.get("Content-Type", "").lower()
            if "html" not in content_type:
                page_titles[url] = ""
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                title_tag = soup.find("title")
                page_titles[url] = title_tag.get_text(strip=True) if title_tag else ""

                for link in soup.find_all("a", href=True):
                    next_url = urljoin(page_url, link["href"])
                    next_url = urldefrag(next_url)[0]
                    if is_same_site(next_url) and next_url not in checked_urls:
                        waiting_urls.append(next_url)

        if len(page_titles) % SAVE_EVERY == 0:
            save_csv(page_titles)
            print(
                f"調査済み: {len(page_titles)}ページ / 待機中: {len(waiting_urls)}ページ",
                flush=True,
            )

    save_csv(page_titles)
    print(f"完了: {len(page_titles)}ページを {CSV_FILE} に保存しました。", flush=True)
    print(f"タイトルが空のページ: {sum(not title for title in page_titles.values())}", flush=True)


if __name__ == "__main__":
    print("練習問題: 映画タイトル", flush=True)
    for movie_title in get_movie_titles():
        print(movie_title)

    print("\n個別課題: 武蔵野大学サイトマップ", flush=True)
    crawl_site()
