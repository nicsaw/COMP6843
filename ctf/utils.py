import requests
import git
from pathlib import Path
import re
import inspect
import subprocess
import paramiko

FLAG_PATTERN = r"(COMP6443{.+?})"
ZID = "z5437741"

def get_session() -> requests.Session:
    session = requests.Session()
    repo = git.Repo(".", search_parent_directories=True)
    repo_root = Path(repo.working_dir)
    session.cert = str(repo_root / "z5437741.pem")
    return session

def get_caller_file_path() -> Path:
    utils_py_path = Path(__file__).resolve()
    for frame in inspect.stack():
        caller_path = Path(frame.filename).resolve()
        if caller_path != utils_py_path:
            return caller_path

def find_flag(text: str, flag_pattern: str = FLAG_PATTERN) -> str:
    if flag_match := re.search(flag_pattern, text):
        flag = flag_match.group(1)
        print(f"\n🚩 FLAG FOUND 🚩\n{flag}\n" * 10)

        caller_path = get_caller_file_path()
        output_file_path = caller_path.with_name(f"{caller_path.stem}.flag.txt")
        with output_file_path.open('a') as f:
            f.write(f"{flag}\n")

        return flag

def find_flags(text: str, flag_pattern: str = FLAG_PATTERN) -> list[str]:
    if matches := re.findall(flag_pattern, text):
        flags = list(set(matches))
        print(f"\n🚩 FLAGS FOUND 🚩\n{'\n'.join(flags)}\n" * 10)

        caller_path = get_caller_file_path()
        output_file_path = caller_path.with_name(f"{caller_path.stem}.flag.txt")
        with output_file_path.open('a') as f:
            for flag in flags:
                f.write(f"{flag}\n")

        return flags

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

    def find_flags(self, max_attempts=5, delay_seconds=1, uuid: str = None) -> list[str] | None:
        import time, json
        for _ in range(max_attempts):
            time.sleep(delay_seconds)
            response = requests.get(self.get_requests_url(uuid))
            response_json = response.json()
            if response_json["data"]:
                response_json_text = json.dumps(response_json, indent=2)
                return find_flags(response_json_text)

class CloudflareTunnel:
    def __init__(self, local_port=8000):
        self.local_port = local_port
        self.public_url = None
        self.process = None

    def start(self) -> str:
        LOCALHOST = "127.0.0.1"
        command = ["cloudflared", "tunnel", "--url", f"http://{LOCALHOST}:{self.local_port}"]
        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        return self._get_public_url()

    def _get_public_url(self) -> str:
        for line in self.process.stdout:
            print(line)
            if match := re.search(r"(https://[a-zA-Z0-9\-]+\.trycloudflare\.com)", line):
                self.public_url = match.group(1)
                return self.public_url

    def get_public_url(self) -> str:
        assert self.public_url
        return self.public_url

    def stop(self):
        self.process.terminate()

    def __del__(self):
        self.stop()

# https://taggi.cse.unsw.edu.au/FAQ/Hosting_services
# https://taggi.cse.unsw.edu.au/FAQ/Creating_a_website
class HostedWebsiteCSE:
    def __init__(self, zid=ZID):
        self.hostname = "cse.unsw.edu.au"
        self.zid = zid

        self.ssh = None
        self.sftp = None

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.connect(self.hostname, username=self.zid)

        self.sftp = self.ssh.open_sftp()

    def mkdir_p(self, dir_path: str):
        parts = dir_path.strip("/").split("/")
        path = ""
        for part in parts:
            path = f"{path}/{part}" if path else part
            try:
                self.sftp.stat(path)
            except IOError:
                self.sftp.mkdir(path)

    def upload_file(self, filename: str, file_content: bytes, write_to_root=False) -> str:
        """
        Returns:
            str: Public URL of uploaded file
        """
        assert self.sftp

        if write_to_root:
            remote_dir = "public_html"
        else:
            caller_name = get_caller_file_path().stem
            remote_dir = f"public_html/{caller_name}"

        remote_path = f"{remote_dir}/{filename}"

        self.mkdir_p(remote_dir)

        with self.sftp.file(remote_path, 'w') as remote_file:
            remote_file.write(file_content)

        # self.sftp.chmod(remote_path, 0o755)

        if write_to_root:
            return f"https://{self.zid}.web.cse.unsw.edu.au/{filename}"
        return f"https://{self.zid}.web.cse.unsw.edu.au/{caller_name}/{filename}"

    def close(self):
        if self.sftp: self.sftp.close()
        if self.ssh: self.ssh.close()

    def __del__(self):
        self.close()
