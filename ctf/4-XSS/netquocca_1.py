import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://netquocca.quoccacorp.com"
MOBILE_URL = "https://m.netquocca.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        response = self.session.get(MOBILE_URL, headers={ "User-Agent": "Mobile" })
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()
