import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
####################################################################################################
try:
    url = input("URL: ").strip()
    if not url.startswith(("https://", "http://")):
        url = "https://" + url
        rq = requests.get(url, timeout=5)
    else:
        rq = requests.get(url, timeout=5)

except Exception as e:
    print(f"[-] error: {e}")
    exit()

header = ["X-Content-Type-Options", "Permissions-Policy", "X-Frame-Options", "Strict-Transport-Security", "Content-Security-Policy", "Referrer-Policy", "Cross-Origin-Embedder-Policy", "X-Permitted-Cross-Domain-Policies", "Cross-Origin-Opener-Policy", "Server", "X-Powered-By", "X-Generator"]
####################################################################################################
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
####################################################################################################
for hr in header:

    if hr in rq.headers:
        print(f"{GREEN}[+] {hr}: {rq.headers[hr]}")
    else:
        print(f"{RED}[-] Not found: {hr}{RESET}")
####################################################################################################
soup = BeautifulSoup(rq.text, 'html.parser')
script = soup.select('[src], [href]')

for s in script:
    val = s.get('src') or s.get('href')
    print(f"[+] path: {val}")
####################################################################################################
url_2 = urlparse(url)
loc = socket.gethostbyname(url_2.netloc)
print("\n" + "=" * 40)
print(f"[+] IP Address: [{loc}]")
print("=" * 40)
print("[1] Scan ports from 1 to 1024 (Well-known ports)")
print("[2] Scan ports from 1 to 49151 (Registered ports)")
print("[3] Scan ports from 1 to 65535 (All ports)")
print("[4] Skip port scanning")
print("=" * 40)
choice = input("Select an option (1-4): ").strip()
if choice == 1:
    ports = range(1, 1025)
    print(f"{GREEN}[+] Scanning ports 1 to 1024...{RESET}")
elif choice == 2:
    ports = range(1, 49152)
    print(f"{GREEN}[+] Scanning ports 1 to 49151...{RESET}")
elif choice == 3:
    ports = range(1, 65536)
    print(f"{GREEN}[+] Scanning ports 1 to 65535...{RESET}")
elif choice == 4:
    print(f"{RED}[-] Port scanning skipped{RESET}")
    exit()
else:
    print(f"{RED}[-] Invalid choice, skipping port scan{RESET}")
    exit()

print(f"[+] ip: [{loc}]")
def sok(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            connect = s.connect_ex((loc, port))
            if connect == 0:
                print(f"{GREEN}[+] port  [{port}] is open{RESET}")
            else:
                pass
    except Exception as e:
        print(f"{RED}[-] error : {e}{RESET}")

with ThreadPoolExecutor(max_workers=100) as workers:
    workers.map(sok, ports)
