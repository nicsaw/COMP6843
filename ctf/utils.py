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
    cert_path = repo_root / "z5437741.pem"
    session.cert = str(cert_path)
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
