import requests
import re

session = requests.Session()
session.cert = "../../z5437741.pem"

URL = "https://haas-v4.quoccacorp.com"

def append_carriage_return(request: str) -> str:
    return '\n'.join(line + '\r' for line in request.split('\n'))

def create_post_request(path: str, data) -> str:
    request = f"""POST {path} HTTP/1.1
Host: kb.quoccacorp.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://haas.quoccacorp.com/
Content-Type: application/x-www-form-urlencoded
Content-Length: {len(data)}
Origin: http://haas.quoccacorp.com
Connection: keep-alive

{data}
"""
    return append_carriage_return(request)

get_request = """GET / HTTP/1.1
Host: kb.quoccacorp.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://haas.quoccacorp.com/
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Origin: http://haas.quoccacorp.com
Connection: keep-alive

"""

QUESTION_PATTERN = r"What is (\d+)\s*([\+\-\*/])\s*(\d+)\?"
FLAG_PATTERN = r"(COMP6443{.+?})"

def contains_flag(text: str):
    return re.search(FLAG_PATTERN, text)

def solve():
    for i in range(21):
        get_response = session.post(URL, data={"requestBox": get_request})
        get_response_text = get_response.content.decode()
        print(get_response_text)

        match = re.search(QUESTION_PATTERN, get_response.content.decode())
        num1, operator, num2 = match.groups()
        num1, num2 = int(num1), int(num2)
        answer = str(eval(f"{num1} {operator} {num2}"))

        post_request = create_post_request("/", f"answer={answer}")
        post_response = session.post(URL, data={"requestBox": post_request})
        post_response_text = post_response.content.decode()
        print(post_response_text)

        if contains_flag(post_response_text):
            print("\n===== FLAG FOUND =====\n" * 10)
            return

solve()