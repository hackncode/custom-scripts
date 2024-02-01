# Usage
# python enhanced_web_enum.py -d example.com --user-agent "MyCustomAgent/2.0" --no-ssl-verify


import argparse
import re
import requests
from termcolor import colored
from urllib.parse import urljoin

# Function to parse command-line arguments
def setup_parser():
    parser = argparse.ArgumentParser(description="Enhanced Web Enumeration Tool")
    parser.add_argument('-d', '--domain', required=True, help='Domain to enumerate')
    parser.add_argument('-o', '--output', default='', help='Base name for output files')
    parser.add_argument('-w', '--wordlist', help='Path to directory enumeration wordlist')
    parser.add_argument('-smap', '--sitemap', help='URL of sitemap if known')
    parser.add_argument('-u', '--userlist', help='Username wordlist for enumeration')
    parser.add_argument('--no-ssl-verify', action='store_true', help='Disable SSL verification')
    parser.add_argument('--user-agent', default='WebEnumTool/1.0', help='User Agent to use for requests')
    parser.add_argument('--proxy', help='Proxy to use for requests (format: http://user:pass@host:port)')
    return parser.parse_args()

# Function to make a GET request with specified options
def make_request(url, args):
    session = requests.Session()
    session.verify = not args.no_ssl_verify
    session.headers.update({'User-Agent': args.user_agent})
    if args.proxy:
        session.proxies.update({'http': args.proxy, 'https': args.proxy})
    return session.get(url)

# Function to process robots.txt
def process_robots_txt(domain_url, args):
    # [ ... existing robots.txt processing logic ... ]
    # Enhanced with make_request function
    pass

# Function to process sitemap.xml
def process_sitemap_xml(domain_url, args):
    # [ ... existing sitemap.xml processing logic ... ]
    # Enhanced with make_request function
    pass

# Function to perform directory enumeration
def directory_enumeration(domain_url, args):
    # [ ... existing directory enumeration logic ... ]
    # Enhanced with make_request function
    pass

# Function to search for email addresses
def search_emails(directories, args):
    # [ ... existing email search logic ... ]
    # Enhanced with make_request function
    pass

# Function to check for admin login page
def check_admin_login(domain_url, args):
    # [ ... existing admin login check logic ... ]
    # Enhanced with make_request function
    pass

# Main function
if __name__ == "__main__":
    args = setup_parser()

    # [ ... existing script logic ... ]
    # Enhanced with added functionalities and improved logic

    print(colored('All done!','green'))
    print(colored('Exiting...','red'))
