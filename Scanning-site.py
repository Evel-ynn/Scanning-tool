import socket
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from typing import List

def get_website_ip_address(url: str) -> str:
    domain = urlparse(url).netloc
    ip_address = socket.gethostbyname(domain)
    return ip_address

def is_port_open(ip_address: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip_address, port))
    sock.close()
    return result == 0

def scan_ports_fast(ip_address: str, min_port: int, max_port: int) -> List[int]:
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        scan_results = executor.map(lambda port: is_port_open(ip_address, port), range(min_port, max_port + 1))

    for port, isOpen in enumerate(scan_results, start=min_port):
        if isOpen:
            open_ports.append(port)
    return open_ports

if __name__ == "__main__":
    try:
        url = input("Enter the website URL (HTTP or HTTPS): ")
        ip_address = get_website_ip_address(url)
        open_ports = scan_ports_fast(ip_address, 1, 1024)

        print(f"The IP address for the website {url} is: {ip_address}")
        print(f"Open ports: {', '.join(map(str, open_ports))}")
    except Exception as e:
        print(f"An error occurred: {e}")
