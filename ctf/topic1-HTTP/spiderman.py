import requests
import re
from urllib.parse import urljoin

session = requests.Session()
session.cert = "../../z5437741.pem"

URL = "https://spiderman.quoccacorp.com"
LINK_PATTERN = r'href=["\']([^"\']*)["\']'
FLAG_PATTERN = r"(COMP6443{.+?})"

def find_flag(text: str):
    if flag_match := re.search(FLAG_PATTERN, text):
        flag = flag_match.group(1)
        print(f"\n========== FLAG FOUND ==========\n{flag}" * 10)
        exit()

def crawl_dfs(url: str, visited: set):
    if url in visited:
        return

    visited.add(url)
    response = session.get(url)
    response_text = response.content.decode()

    find_flag(response_text)

    links = re.findall(LINK_PATTERN, response_text)
    for link in links:
        next_url = urljoin(url, link)
        crawl_dfs(next_url, visited)

crawl_dfs(URL, set())