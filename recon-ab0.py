import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
import threading
import tldextract



####################################################################################################
GREEN = "\033[92m" 
RED = "\033[91m"
RESET = '\033[0m'
CYAN = "\033[96m"
UNDERLINE = "\033[4m"
BOLD = "\033[1m" 
####################################################################################################

banner = f"""{CYAN}
   ███████╗ ██████╗ █████╗ ███╗   ██╗██╗  ██╗       ██████╗ 
   ██╔════╝██╔════╝██╔══██╗████╗  ██║╚██╗██╔╝      ██╔═████╗
   ███████╗██║     ███████║██╔██╗ ██║ ╚███╔╝ █████╗██║██╔██║
   ╚════██║██║     ██╔══██║██║╚██╗██║ ██╔██╗ ╚════╝████╔╝██║
   ███████║╚██████╗██║  ██║██║ ╚████║██╔╝ ██╗      ╚██████╔╝
   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═════╝ 
  {RESET}"""

print(banner)

def get_target_url():
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        url = input("URL: ").strip()
        if not url.startswith(("https://", "http://")):
            try:
                url = "https://" + url
                response = requests.get(url, headers=user_agent, timeout=5)
            except:
                url = "http://" + url
                response = requests.get(url, headers=user_agent, timeout=5)
        else:
            response = requests.get(url, headers=user_agent, timeout=5)

        return response, url, user_agent
    
    except Exception as error:
        print(f"{UNDERLINE}{RED}[-] error: {error}{RESET}")
        return get_target_url()

response, url, user_agent = get_target_url()
parsed_main_url = tldextract.extract(url)
discovered_items = set()
domain_name = f"{parsed_main_url.domain}.{parsed_main_url.suffix}"

security_headers = [
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


def scan_security_headers():
    try:
        for headers in security_headers:
            if headers in response.headers:
                print(
                    f"{BOLD}{GREEN}[+] {headers}: {response.headers[headers]}{RESET}")
            else:
                print(f"{BOLD}{RED}[-] Not found: {headers}{RESET}")
    except Exception as error:
        print(f"{UNDERLINE}{RED}[-] error: {error}{RESET}")
        get_target_url()


scan_security_headers()

print("=" * 60)


def scan_html_paths():
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.select('[src], [href]')

    if not script:
        print(f"{BOLD}{RED}[-] No paths were found{RESET}")
        return

    for scripts in script:
        path = scripts.get('src') or scripts.get('href')

        if path and path not in discovered_items:
            discovered_items.add(path)
            join_url = urljoin(url, path)
            parsed_url = urlparse(join_url)
            root_domain = parsed_url.netloc
            print(f"{BOLD}[+] Path: {path}")
            print(f"    └── Absolute: {join_url}")
            print(f"    └── Root/Domain: {root_domain}\n{RESET}")


scan_html_paths()

print("=" * 60)


def fetch_subdomains():
    try:
        Sub = f"https://api.hackertarget.com/hostsearch/?q={domain_name}"
        get = requests.get(Sub)
        all_subdomains = []

        if get.status_code == 200:
            get_text = get.text.splitlines()

            for get_all in get_text:
                if get_all and get_all not in discovered_items:
                    discovered_items.add(get_all.split(",")[0])
                    discovered_items.add(get_all.split(",")[1])
                    all_subdomains.append(get_all.split(",")[0])

                    print(f"{BOLD}Subdomain: {get_all.split(',')[0]}")
                    print(f"  {BOLD}└── IP Address: {get_all.split(',')[1]}\n")

        return all_subdomains

    except Exception as error:
        print(f"{UNDERLINE}{RED}[-] error : {error}{RESET}")
        return


all_subdomains = fetch_subdomains()
if all_subdomains:
    def scan_common_paths():
        Common_paths = [
            "/admin",
            "/wp-admin",
            "/dashboard",
            "/controlpanel",
            "/manage",
            "/login.php",
            "/signin",
            "/config.php",
            "/configuration.php",
            "/settings.json",
            "/appsettings.json",
            "/backup",
            "/backups",
            "/.env",
            "/db.sql",
            "/database.sql",
            "/api",
            "/api/v1/",
            "/api/v2/",
            "/swagger",
            "/swagger-ui.html",
            "/graphql",
            "/phpinfo.php",
            "/server-status",
            "/server-info",
            "/test",
            "/testing/",
            "/phpmyadmin",
            "/.git",
            "/.svn",
            "/robots.txt",
            "/sitemap.xml"
            ]
        try:
            for in_subdomains in all_subdomains:
                get_subdomains = requests.get("https://" + in_subdomains)

                if get_subdomains.status_code == 200:
                    print(f"Scanning subdomain: {in_subdomains}")
                    link = f"https://{in_subdomains}"

                    for All_paths in Common_paths:
                        Complete_link = link + All_paths
                        gets = requests.get(Complete_link, headers=user_agent, timeout=5)

                        if gets.status_code == 200:
                            print(f"link: {Complete_link}")
                        else:
                            pass

                else:
                    get_subdomains = requests.get("http://" + in_subdomains)

                    if get_subdomains.status_code == 200:
                        link = f"http://{in_subdomains}"

                        for All_paths in Common_paths:
                            Complete_link = link + All_paths
                            gets = requests.get(Complete_link, headers=user_agent, timeout=5)

                            if gets.status_code == 200:
                                print(f"link: {Complete_link}")
                            else:
                                pass
        except Exception as error:
            print(f"{UNDERLINE}{RED}[-] error : {error}{RESET}")
            pass


    scan_common_paths()

def get_port_range():
    ip = socket.gethostbyname(domain_name)

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
            get_port_range()
    except Exception as error:
        print(f"{UNDERLINE}{RED}[-] error : {error}{RESET}")
        return get_port_range()
    
    return ports, ip


ports, ip = get_port_range()

print_lock = threading.Lock()


def check_port(port):
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
        print(f"{UNDERLINE}{RED}[-] error : {error}{RESET}")


with ThreadPoolExecutor(max_workers=100) as workers:
    workers.map(check_port, ports)

