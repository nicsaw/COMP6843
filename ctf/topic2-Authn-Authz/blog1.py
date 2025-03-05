import requests
import re

session = requests.Session()
session.cert = "../../z5437741.pem"

BASE_URL = "https://blog.quoccacorp.com/?p="
START_PAGE = 0
FLAG_PATTERN = r"(COMP6443{.+?})"

def find_flag(text: str):
    if flag_match := re.search(FLAG_PATTERN, text):
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}" * 10)
        exit()

PAGE_NOT_FOUND_CONTENT = """<head>
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name='robots' content='max-image-preview:large' />
	<style>img:is([sizes="auto" i], [sizes^="auto," i]) { contain-intrinsic-size: 3000px 1500px }</style>
	<title>Page not found &#8211; Quoccacorp Blog</title>
<link rel="alternate" type="application/rss+xml" title="Quoccacorp Blog &raquo; Feed" href="https://blog.quoccacorp.com/?feed=rss2" />
<link rel="alternate" type="application/rss+xml" title="Quoccacorp Blog &raquo; Comments Feed" href="https://blog.quoccacorp.com/?feed=comments-rss2" />"""

def main():
    page_num = START_PAGE
    while True:
        url = BASE_URL + str(page_num)
        print(f"Visiting {url}")
        response = session.get(url)
        response_text = response.content.decode("utf-8", "ignore")

        find_flag(response_text)

        if PAGE_NOT_FOUND_CONTENT not in response_text:
            print(f"{page_num = }")

        page_num += 1

if __name__ == "__main__":
    main()