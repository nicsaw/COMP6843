import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import get_session, find_flag

BASE_URL = "https://support-v0.quoccacorp.com/raw/"

def main():
    session = get_session()
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