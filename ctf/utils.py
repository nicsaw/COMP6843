import requests
import git
from pathlib import Path
import re
import inspect

FLAG_PATTERN = r"(COMP6443{.+?})"

def get_session() -> requests.Session:
    session = requests.Session()
    repo = git.Repo(".", search_parent_directories=True)
    repo_root = Path(repo.working_dir)
    session.cert = str(repo_root / "z5437741.pem")
    return session

def find_flag(text: str, flag_pattern: str = FLAG_PATTERN):
    if flag_match := re.search(flag_pattern, text):
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}\n" * 10)

        caller_frame = inspect.stack()[1]
        caller_path = Path(caller_frame.filename)
        output_file = caller_path.with_name(f"{caller_path.stem}.flag.txt")
        with output_file.open("a") as f:
            f.write(f"{flag}\n")

        return flag
    return None

class WebhookSite:
    def __init__(self):
        self.token = self.create_token()
        self.uuid = self.get_uuid()
        self.url = self.get_url(self.uuid)
        self.view_url = self.get_view_url(self.uuid)
        self.requests_url = self.get_requests_url(self.uuid)

    def create_token(self) -> dict:
        return requests.post("https://webhook.site/token").json()

    def get_uuid(self) -> str:
        return self.token["uuid"]

    def get_url(self, uuid: str = None) -> str:
        uuid = uuid if uuid else self.uuid
        return f"https://webhook.site/{uuid}"

    def get_view_url(self, uuid: str = None) -> str:
        uuid = uuid if uuid else self.uuid
        return f"https://webhook.site/#!/view/{uuid}"

    def get_requests_url(self, uuid: str = None) -> str:
        uuid = uuid if uuid else self.uuid
        return f"https://webhook.site/token/{uuid}/requests"

    def find_flag(self, max_attempts=3, delay_seconds=1, uuid: str = None) -> str | None:
        import time, json
        for _ in range(max_attempts):
            time.sleep(delay_seconds)
            response = requests.get(self.get_requests_url(uuid))
            response_json = response.json()
            if response_json["data"]:
                response_json_text = json.dumps(response_json, indent=2)
                return find_flag(response_json_text)
