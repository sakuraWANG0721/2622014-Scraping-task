from bs4 import BeautifulSoup


# 自分で作ったHTMLファイルを読む
with open("test.html", "r", encoding="utf-8") as f:
    html = f.read()

# HTMLからタグを探す
html_soup = BeautifulSoup(html, "html.parser")
print(f"HTMLの型: {type(html_soup)}")

print("タイトル")
print(html_soup.title.string)

print("最初のaタグ")
soup_a = html_soup.a
print(soup_a)
print(f"{type(soup_a)}")

print("最初のpタグ")
soup_p = html_soup.p
print(soup_p)
print(f"{type(soup_p)}")

print("divタグ")
soup_div = html_soup.div
print(soup_div)

print("中にあるdivタグ")
soup_div_div = soup_div.div
print(soup_div_div)
print(f"{type(soup_div_div)}")

print("aタグの文字")
print(soup_a.string)

print("divタグの文字")
print(soup_div_div.string)
