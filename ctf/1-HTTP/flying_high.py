import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        response = self.session.get("https://quoccaair.quoccacorp.com/home_files/HOB-BNE.html")
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()