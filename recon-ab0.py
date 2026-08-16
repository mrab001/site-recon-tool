import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse
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
        print(f"{RED}[-] Not found: {hr}")
####################################################################################################
soup = BeautifulSoup(rq.text, 'html.parser')
script = soup.select('[src], [href]')

for s in script:
    val = s.get('src') or s.get('href')
    print(f"{RESET}path: {val}")
####################################################################################################
url2 = urlparse(url)
clean = url2.netloc
get = socket.gethostbyname(clean)

print(f"ip: {get}")
print(f"{RED}Note: This may put a strain on the server.")

choice = input(f"{RESET}Do you want to start scanning ports? (y/n): ").strip()

if choice == "y":
    print("[+] Please wait while the scan is in progress...")

    for port in range(1, 65535):
        sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sok.settimeout(0.5)
        
        if sok.connect_ex((get, port)) == 0:
            print(f"port {port} is open")
        else:
            pass

elif choice == "n":
    pass
else:
    print("[-] Invalid input! Please enter 'y' for yes or 'n' for no")
