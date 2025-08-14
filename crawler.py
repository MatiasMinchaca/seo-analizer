import requests
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
        # Return the final URL after any redirects
        return r.url, r.status_code, r.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        # Return the original URL on failure, with None for status and text
        return url, None, None

def crawl_site(base_url, max_pages):
    """Crawls a website and returns the parsed data for each page."""
    crawled_data = []
    
    start_url = normalize_url(base_url)
    queue = deque([start_url])
    visited = {start_url}
    
    base_netloc = urlparse(start_url).netloc.replace("www.", "")

    while queue and len(crawled_data) < max_pages:
        url = queue.popleft()
        print(f"Crawling [{len(crawled_data) + 1}/{max_pages}]: {url}")

        final_url, status, html = fetch(url)
        if not html:
            continue

        # Use the final, redirected URL for all checks and data storage
        normalized_final_url = normalize_url(final_url)

        # Check if we have already processed this page via another redirect
        if normalized_final_url in visited and url != normalized_final_url:
            print(f"  -> Redirected to already visited page: {normalized_final_url}")
            continue
        
        visited.add(normalized_final_url)

        page_data = parse_page(normalized_final_url, html, base_netloc)
        crawled_data.append(page_data)

        for link in page_data["internal_links"]:
            # Links from the parser are already normalized
            if link not in visited:
                visited.add(link)
                queue.append(link)
    
    return crawled_data