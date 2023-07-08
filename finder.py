import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from multiprocessing import Pool, Manager
from time import sleep
import robotexclusionrulesparser

def visit_url(queue, visited_urls, discovered_urls, robots_parsers):
    while True:
        if not queue.empty():
            url = queue.get()
            visited_urls[url] = True

            print(f'Visiting: {url}')

            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"

            if base_url not in robots_parsers:
                try:
                    robots_url = urljoin(base_url, "robots.txt")
                    response = requests.get(robots_url)
                    robots_parser = robotexclusionrulesparser.RobotExclusionRulesParser()
                    robots_parser.parse(response.text)
                    robots_parsers[base_url] = robots_parser
                except requests.exceptions.RequestException as e:
                    print(f"Failed to retrieve robots.txt for {base_url}: {e}")
                    robots_parsers[base_url] = None

            if robots_parsers[base_url] is not None and not robots_parsers[base_url].is_allowed("*", url):
                print(f"Skipping {url} due to robots.txt")
                continue

            if parsed.path and parsed.path != '/':
                # This URL has a path, so write it to the paths file
                with open('paths.txt', 'a') as f:
                    f.write(url + '\n')
            else:
                # This URL does not have a path, so write it to the no_paths file
                with open('no_paths.txt', 'a') as f:
                    f.write(url + '\n')
                    if url not in visited_urls and url not in discovered_urls:
                        queue.put(url)
                        discovered_urls[url] = True

            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a'):
                    new_url = link.get('href')
                    if new_url:
                        new_url = urljoin(url, new_url)
                        if new_url.startswith('http://') or new_url.startswith('https://'):
                            if new_url not in visited_urls and new_url not in discovered_urls:
                                queue.put(new_url)
                                discovered_urls[new_url] = True
            except requests.exceptions.RequestException as e:
                print(f"Failed to visit {url}: {e}")

            print(f'URLs in queue: {queue.qsize()}')
            print(f'Visited URLs: {len(visited_urls)}')
            print('---------------------------------------------------')
        else:
            sleep(1)

if __name__ == "__main__":
    manager = Manager()

    urls_to_visit = manager.Queue()
    urls_to_visit.put("https://www.site1.com/")
    urls_to_visit.put("https://www.site2.com/")
    visited_urls = manager.dict()
    discovered_urls = manager.dict()
    robots_parsers = manager.dict()

    with Pool() as p:
        for _ in range(p._processes):
            p.apply_async(visit_url, (urls_to_visit, visited_urls, discovered_urls, robots_parsers))

        p.close()
        p.join()
