import requests
import time
import random 
from collections import deque
from urllib.parse import urlparse
from parser import parse_page
from utils import normalize_url

HEADERS = {"User-Agent": "SEO-Audit-Bot/6.0"}

def fetch(url):
    """Performs a GET request, handles errors, and returns the final URL, status, and text."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        r.raise_for_status()
        return r.url, r.status_code, r.text
    except requests.RequestException as e:
        print(f"  -> Error fetching {url}: {e}")
        return url, None, None

def crawl_site(base_url, max_pages):
    """Crawls a website, fetching only HTML pages, and returns the parsed data."""
    crawled_data = []
    start_url = normalize_url(base_url)
    queue = deque([start_url])
    visited = {start_url}
    base_netloc = urlparse(start_url).netloc.replace("www.", "")

    next_pause_at = random.randint(50, 100)
    
    while queue and len(crawled_data) < max_pages:
        url = queue.popleft()
        print(f"Crawling [{len(crawled_data) + 1}/{max_pages}]: {url}")

        if len(crawled_data) > 0 and (len(crawled_data) % 100 == 0 or len(crawled_data) == next_pause_at):
            wait_time = random.randint(300, 800)  # 5 to 10 minutes in seconds
            print(f"Pausing for {wait_time // 60} minutes ({wait_time} seconds) to avoid being blocked...")
            time.sleep(wait_time)
            next_pause_at = len(crawled_data) + random.randint(30, 80)

        try:
            head_response = requests.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
            content_type = head_response.headers.get("Content-Type", "")
            final_url = normalize_url(head_response.url)

            if final_url in visited and final_url != url:
                print(f"  -> Redirected to already visited page: {final_url}")
                continue
            
            if "text/html" not in content_type:
                print(f"  -> Skipping non-HTML content: {content_type}")
                visited.add(final_url)
                continue

        except requests.RequestException as e:
            print(f"  -> Could not perform HEAD request for {url}: {e}")
            continue

        # Now we know it's an HTML page, so we fetch the full content
        # The final_url from the HEAD request is the one we use
        _final_url, status, html = fetch(final_url)
        if not html:
            continue
        
        visited.add(final_url)

        page_data = parse_page(final_url, html, base_netloc)
        crawled_data.append(page_data)

        for link in page_data["internal_links"]:
            if link not in visited:
                visited.add(link)
                queue.append(link)
    
    return crawled_data