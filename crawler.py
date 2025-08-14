import requests
from collections import deque
from urllib.parse import urlparse
from parser import parse_page

HEADERS = {"User-Agent": "SEO-Audit-Bot/6.0"}

def fetch(url):
    """Performs a GET request, handles errors, and returns status and text."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.status_code, r.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None

def crawl_site(base_url, max_pages):
    """Crawls a website and returns the parsed data for each page."""
    crawled_data = []
    queue = deque([base_url])
    visited = {base_url}
    base_netloc = urlparse(base_url).netloc

    while queue and len(crawled_data) < max_pages:
        url = queue.popleft()
        print(f"Crawling [{len(crawled_data) + 1}/{max_pages}]: {url}")

        # Check content type before full download
        try:
            head_response = requests.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
            content_type = head_response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                print(f"Skipping non-HTML content at {url}")
                continue
        except requests.RequestException as e:
            print(f"Could not check headers for {url}: {e}")
            continue

        status, html = fetch(url)
        if not html:
            continue

        page_data = parse_page(url, html, base_netloc)
        crawled_data.append(page_data)

        for link in page_data["internal_links"]:
            if link not in visited:
                visited.add(link)
                queue.append(link)
    
    return crawled_data
