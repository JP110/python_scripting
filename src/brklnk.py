import argparse
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException,MissingSchema

def get_links(url):
    try:
        response = requests.get(url)
    except MissingSchema as e:
        print(f"Invalid URL {url}")
        return []
    except Exception as e:
        print(e)
        return []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            href_value = link.get('href')
            links.append(href_value)
        return links
    else:
        return []

def check_recursive(current_url, depth, checked_links):
    if depth == 0:
        return
    try:
        links = get_links(current_url)
        for link in links:
            if link in checked_links:
                continue
            absolute_link = urljoin(current_url, link)
            if absolute_link.startswith(("http://", "https://")) and absolute_link not in checked_links:
                try:
                    response = requests.head(absolute_link)
                    if response.status_code == 302 or response.status_code == 301:
                        new_location = response.headers['Location']
                        response = requests.head(new_location)
                    if response.status_code == 404:
                        print(f"Broken link (404): {absolute_link}")
                    elif response.status_code != 200:
                        print(f"Unexpected status code {response.status_code} for link: {absolute_link}")
                except RequestException as e:
                    # HTTP page return an exception if they are broken
                    print(f"Broken link (404): {absolute_link}")
                checked_links.add(absolute_link)
                check_recursive(absolute_link, depth - 1, checked_links)
    except Exception as e:
        print(f"Invalid URL {current_url}: {e}")

def check_links(url, depth):
    checked_links = set()
    check_recursive(url, depth, checked_links)
    print(f"Number of links checked : {len(checked_links)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to check for broken links")
    parser.add_argument("--depth", type=int, default=1, help="Depth of link checking (default: 1)")
    args = parser.parse_args()
    check_links(args.url, args.depth)