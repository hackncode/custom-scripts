"""
Domain Availability Checker
===========================

This script reads a list of domain names from a text file and checks if the domains are live by sending HTTP requests
to ports 80 (HTTP) and 443 (HTTPS).

Usage:
    python domain_checker.py [filename]
"""

import sys
import requests
from concurrent.futures import ThreadPoolExecutor
import os

def read_domain_list(file_path):
    """
    Reads a list of domain names from a text file.
    
    Args:
    - file_path (str): Path to the text file containing domain names.

    Returns:
    - List of domain names.
    """
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r') as file:
        domain_list = [line.strip() for line in file.readlines()]
    return domain_list

def sanitize_url(url):
    """
    Removes 'http://' or 'https://' prefixes from a URL.
    
    Args:
    - url (str): URL to sanitize.

    Returns:
    - Sanitized URL without 'http://' or 'https://' prefixes.
    """
    if url.startswith(('http://', 'https://')):
        return url.split('://')[1]
    return url

def check_domain_availability(domain):
    """
    Checks if a domain is live by sending HTTP requests to ports 80 and 443.
    
    Args:
    - domain (str): Domain name to check.

    Returns:
    - Boolean indicating whether the domain is live or not.
    """
    domain = sanitize_url(domain)
    urls = [f"http://{domain}", f"https://{domain}"]

    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
    return False

def check_domains(domain_list):
    """
    Checks domain availability using a thread pool.
    
    Args:
    - domain_list (list): List of domain names to check.

    Returns:
    - List of tuples containing domain name and availability status.
    """
    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_domain = {executor.submit(check_domain_availability, domain): domain for domain in domain_list}
        for future in future_to_domain:
            domain = future_to_domain[future]
            try:
                availability = future.result()
                results.append((domain, availability))
            except Exception as exc:
                print(f'{domain} generated an exception: {exc}')
    return results

def main():
    if len(sys.argv) < 2:
        filename = input("Enter the filename containing domain names: ")
    else:
        filename = sys.argv[1]

    domain_list = read_domain_list(filename)
    print(f"Checking availability of {len(domain_list)} domains...")

    results = check_domains(domain_list)

    live_domains = [domain for domain, available in results if available]
    not_live_domains = [domain for domain, available in results if not available]

    with open('live_domains.txt', 'w') as file:
        for domain in live_domains:
            file.write(f"{domain}\n")

    print("\nSummary:")
    print(f"Total domains checked: {len(domain_list)}")
    print(f"Live domains: {len(live_domains)}")
    print(f"Not live domains: {len(not_live_domains)}")
    print("\nLive domains have been saved to 'live_domains.txt'.")

if __name__ == "__main__":
    main()
