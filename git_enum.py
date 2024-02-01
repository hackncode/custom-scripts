import argparse
import requests
from getpass import getpass
import time

# ANSI escape codes for colored output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def rate_limit_handler(response):
    """Handle GitHub API rate limits."""
    if 'X-RateLimit-Remaining' in response.headers and int(response.headers['X-RateLimit-Remaining']) == 0:
        reset_time = int(response.headers['X-RateLimit-Reset'])
        wait_time = max(reset_time - time.time(), 0)
        print(f"{YELLOW}Rate limit reached. Waiting for {int(wait_time)} seconds to reset...{RESET}")
        time.sleep(wait_time)

# Setup command-line argument parsing
parser = argparse.ArgumentParser(description='Enhanced GitHub search tool.')
parser.add_argument('keywords', type=str, help='Keywords to search, separated by commas (e.g., "keyword1,keyword2")')
parser.add_argument('-r', '--repositories', action='store_true', help='Search in repositories')
parser.add_argument('-c', '--code', action='store_true', help='Search in code')
parser.add_argument('-i', '--issues', action='store_true', help='Search in issues')
parser.add_argument('-m', '--commits', action='store_true', help='Search in commits')
parser.add_argument('-o', '--output', default='github_search_results.txt', help='Output file for search results')
parser.add_argument('--language', help='Filter by programming language')
parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
args = parser.parse_args()

if args.interactive:
    args.keywords = input("Enter keywords to search: ")
    args.repositories = 'r' in input("Search in repositories (r)? ")
    args.code = 'c' in input("Search in code (c)? ")
    args.issues = 'i' in input("Search in issues (i)? ")
    args.commits = 'm' in input("Search in commits (m)? ")

# Prompt the user to input the GitHub Personal Access Token securely
auth_token = getpass("Please enter your GitHub Personal Access Token: ")
headers = {
    'Authorization': f'token {auth_token}',
    'Accept': 'application/vnd.github.v3+json',
}

# Parse keywords
keywords = [keyword.strip() for keyword in args.keywords.split(',')]

# Constructing the search query
query = ' OR '.join(f'"{keyword}"' for keyword in keywords)
if args.language:
    query += f" language:{args.language}"

categories = {
    'repositories': args.repositories,
    'code': args.code,
    'issues': args.issues,
    'commits': args.commits
}
if not any(categories.values()):
    categories = {key: True for key in categories}

HORIZONTAL_LINE = RED + '-' * 80 + RESET

# Prepare the output file
with open(args.output, 'w') as file:
    for category, search in categories.items():
        if not search:
            continue
        
        url = f'https://api.github.com/search/{category}?q={query}'
        
        category_header = f"\n{HORIZONTAL_LINE}\nSearching in {category} for keywords: {query}\n{HORIZONTAL_LINE}\n"
        print(category_header)
        file.write(category_header + '\n')

        while url:
            response = requests.get(url, headers=headers)
            rate_limit_handler(response)
            
            if response.status_code == 200:
                data = response.json()
                items = data['items']
                
                for item in items:
                    result_line = f"Found in {category}: {item['html_url']}\n"
                    print(f"{GREEN}{result_line}{RESET}")
                    file.write(result_line)
                
                if 'next' in response.links.keys():
                    url = response.links['next']['url']
                else:
                    url = None
            else:
