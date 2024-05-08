import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_site(start_url):
    visited = set()
    queue = [start_url]

    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        print("Crawling:", url)

        try:
            response = requests.get(url)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                absolute_link = urljoin(url, link['href'])
                if urlparse(absolute_link).netloc == urlparse(start_url).netloc:
                    queue.append(absolute_link)

        except requests.RequestException:
            continue

crawl_site('https://arxiv.org/html/2402.06664v1')