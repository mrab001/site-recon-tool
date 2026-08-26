ScanX-0 (Recon)

A powerful, lightweight, and multi-threaded Python script designed for fast web reconnaissance and security assessment. 



Key Features

 Security Headers Analysis:** Inspects the target for active or missing critical security headers (CSP, HSTS, X-Frame-Options, etc.)
 HTML Path Extraction:** Parses the target's source code to extract internal links, resources, and endpoints.
 Subdomain Enumeration:** Discovers subdomains and retrieves their IP addresses using external intelligence APIs.
 Common Paths Fuzzing:** Automatically scans discovered subdomains for sensitive paths, config files, and administrative panels.
 Fast Port Scanner:** Built-in high-performance, multi-threaded port scanner supporting multiple ranges (1-1024, 1-49151, or all 65535 ports).



 Requirements & Dependencies

Make sure you have Python 3 and pip installed on your system.

 Install Required Packages:

* **For Windows & macOS:**

      pip install requests beautifulsoup4 tldextract

    For Linux (Debian/Ubuntu/Arch/Fedora):
    (Using system-wide installation without virtual environments)
    

      pip install requests beautifulsoup4 tldextract --break-system-packages

    (Note: You can also use your package manager if available, e.g., sudo apt install python3-requests python3-bs4 python3-tldextract)

 How to Install & Run
1. Clone the Repository

       git clone https://github.com/mrab001/ScanX-0.git
   
        cd ScanX-0

3. Run the Tool

    On Windows:
    

       python recon-ab0.py

On Linux / macOS:


    python3 recon-ab0.py

⚠️ Disclaimer

This tool is created for educational purposes and authorized security auditing only. The author is not responsible for any misuse or damage caused by this program.
