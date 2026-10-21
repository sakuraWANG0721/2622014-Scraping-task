from bs4 import BeautifulSoup


# 自分で作ったHTMLファイルを読む
with open("test.html", "r", encoding="utf-8") as f:
    html = f.read()

html_soup = BeautifulSoup(html, "html.parser")

print("最初のh2タグを探す")
h2 = html_soup.find("h2")
print(type(h2))
print(h2.string)

print("全部のh2タグを探す")
h2_all = html_soup.find_all("h2")
for h2 in h2_all:
    if h2.span is not None:
        print(h2.span.string)

print("aタグを5個まで探す")
a_list = html_soup.find_all("a", limit=5)
for a in a_list:
    print(a.string)

print("aタグとspanタグを合わせて探す")
tag_list = html_soup.find_all(["a", "span"], limit=5)
for tag in tag_list:
    print(tag)

print("href属性があるタグを探す")
tag_href_list = html_soup.find_all(attrs={"href": True})
for tag in tag_href_list:
    print(tag)

print("武蔵野大学のリンクを探す")
school_link = html_soup.find(attrs={"href": "https://www.musashino-u.ac.jp"})
print(school_link)

print("idでリンクを探す")
print(html_soup.find(id="study-link"))

print("classで授業メモを探す")
print(html_soup.find_all(class_="study-note"))
