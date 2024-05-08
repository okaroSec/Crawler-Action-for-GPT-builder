## for testing purposes, using actions within GPT builder


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time

def crawl_site(start_url, output_file):
    visited = set()
    queue = deque([start_url])
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

    with requests.Session() as session, open(output_file, 'w') as file:
        while queue:
            url = queue.popleft()
            if url in visited:
                continue
            visited.add(url)
            print("Crawling:", url)
            file.write(url + '\n') 
            #rate limter
            try:
                response = session.get(url, headers=headers, timeout=5)
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    absolute_link = urljoin(url, link['href'])
                    if urlparse(absolute_link).netloc == urlparse(start_url).netloc:
                        queue.append(absolute_link)

            except requests.RequestException as e:
                print(f"Failed to retrieve {url}: {e}")
                continue

            time.sleep(1) 


crawl_site('test-site', 'test_site.txt')
