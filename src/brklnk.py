import argparse
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException,MissingSchema


def check_recursive(current_url, depth, checked_urls):
    if depth >= 0 and not current_url in checked_urls:
        checked_urls.add(current_url)
        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                content_html = BeautifulSoup(response.text, 'html.parser')
                for link in content_html.find_all('a', href=True):
                    href_value = link.get('href')
                    absolute_link = urljoin(current_url, href_value)
                    check_recursive(absolute_link, depth - 1, checked_urls)
            elif response.status_code == 404:
                print(f"Broken link (404): {current_url}")
            else:
                print(f"Unexpected status code {response.status_code} for link: {current_url}")
        except MissingSchema as e:
            print(f"Invalid URL {current_url}")     
        except RequestException as e:
            # HTTP page return an exception if they are broken
            print(f"Broken link (404): {current_url}")
        except Exception as e:
            print(f"Invalid URL {current_url}: {e}")

def check_links(url, depth):
    checked_urls = set()
    check_recursive(url, depth, checked_urls)
    print(f"Number of links checked : {len(checked_urls)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to check for broken links")
    parser.add_argument("--depth", type=int, default=1, help="Depth of link checking (default: 1)")
    args = parser.parse_args()
    check_links(args.url, args.depth)