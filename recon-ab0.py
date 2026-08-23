import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
import threading

####################################################################################################
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
####################################################################################################


def Clean_url():
    User_Agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        url = input("URL: ").strip()
        if not url.startswith(("https://", "http://")):
            try:
                url = "https://" + url
                response = requests.get(url, headers=User_Agent, timeout=5)
            except:
                url = "http://" + url
                response = requests.get(url, headers=User_Agent, timeout=5)
        else:
            response = requests.get(url, headers=User_Agent, timeout=5)
    except Exception as error:
        print(f"{RED}[-] error: {error}{RESET}")
        Clean_url()
    return response, url


response, url = Clean_url()
parsed_main_url = urlparse(url)
setop = set()

header = [
    "X-Content-Type-Options",
    "Permissions-Policy",
    "X-Frame-Options",
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "Referrer-Policy",
    "Cross-Origin-Embedder-Policy",
    "X-Permitted-Cross-Domain-Policies",
    "Cross-Origin-Opener-Policy",
    "Server",
    "X-Powered-By",
    "X-Generator"
]


def Scanning_headers():
    try:
        for headers in header:
            if headers in response.headers:
                print(
                    f"{GREEN}[+] {headers}: {response.headers[headers]}{RESET}")
            else:
                print(f"{RED}[-] Not found: {headers}{RESET}")
    except Exception as error:
        print(f"{RED}[-] error: {error}{RESET}")
        Clean_url()


Scanning_headers()

print("=" * 60)


def path_scan():
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.select('[src], [href]')

    if not script:
        print("[-] No paths were found")
        return

    for scripts in script:
        path = scripts.get('src') or scripts.get('href')

        if path and path not in setop:
            setop.add(path)
            join_url = urljoin(url, path)
            parsed_url = urlparse(join_url)
            root_domain = parsed_url.netloc
            print(f"{GREEN}[+] Path: {path}")
            print(f"    └── Absolute: {join_url}")
            print(f"    └── Root/Domain: {root_domain}\n{RESET}")


path_scan()

print("=" * 60)


def Subdomain():
    url_1 = parsed_main_url.netloc
    Sub = f"https://api.hackertarget.com/hostsearch/?q={url_1}"
    get = requests.get(Sub)
    if get.status_code == 200:
        get_text = get.text.splitlines()
        for get_all in get_text:
            if get_all and get_all not in setop:
                setop.add(get_all)
                print(f"Subdomain: {get_all.split(',')[0]}")
                print(f"  └── IP Address: {get_all.split(',')[1]}\n")


Subdomain()


def Ask():
    ip = socket.gethostbyname(parsed_main_url.netloc)
    print("\n" + "=" * 40)
    print(f"[+] IP Address: [{ip}]")
    print("=" * 40)
    print("[1] Scan ports from 1 to 1024 (Well-known ports)")
    print("[2] Scan ports from 1 to 49151 (Registered ports)")
    print("[3] Scan ports from 1 to 65535 (All ports)")
    print("[4] Skip port scanning")
    print("=" * 40)
    try:
        choice = int(input("Select an option (1-4): ").strip())
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
            print(f"{RED}[-] Invalid choice{RESET}")
            Ask()
    except Exception as error:
        print(f"{RED}[-] error : {error}{RESET}")
        Ask()
    return ports, ip


ports, ip = Ask()

print_lock = threading.Lock()


def sok(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            connect = s.connect_ex((ip, port))
            if connect == 0:
                with print_lock:
                    print(f"{GREEN}[+] port  [{port}] is open{RESET}")
            else:
                pass
    except Exception as error:
        print(f"{RED}[-] error : {error}{RESET}")


with ThreadPoolExecutor(max_workers=100) as workers:
    workers.map(sok, ports)
