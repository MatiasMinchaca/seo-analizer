from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib

def parse_page(url, html, base_netloc):
    """Extracts all relevant SEO data from a single HTML page."""
    soup = BeautifulSoup(html, "html.parser")

    # --- Basic Tags ---
    title = soup.title.string.strip() if soup.title else ""
    
    # --- Meta Descriptions ---
    meta_desc_tags = soup.find_all("meta", attrs={"name": "description"})
    meta_descriptions = [tag["content"].strip() for tag in meta_desc_tags if tag.has_attr("content")]
    
    # --- Headings ---
    h1s = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]

    # --- Canonicals ---
    canonical_tags = soup.find_all("link", rel="canonical")
    canonicals = [tag["href"].strip() for tag in canonical_tags if tag.has_attr("href")]

    # --- Content Analysis ---
    text_content = soup.get_text(separator=' ', strip=True)
    word_count = len(text_content.split())
    content_hash = hashlib.sha256(text_content.encode('utf-8')).hexdigest()

    # --- Links ---
    internal_links = set()
    external_links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue
        
        full_url = urljoin(url, href)
        parsed_full_url = urlparse(full_url)

        if parsed_full_url.netloc == base_netloc:
            internal_links.add(full_url)
        else:
            external_links.add(full_url)

    # --- Images ---
    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src:
            full_src_url = urljoin(url, src)
            images.append({"src": full_src_url, "alt": img.get("alt", "").strip()})

    return {
        "url": url,
        "title": title,
        "meta_descriptions": meta_descriptions,
        "h1s": h1s,
        "canonicals": canonicals,
        "word_count": word_count,
        "content_hash": content_hash,
        "internal_links": list(internal_links),
        "external_links": list(external_links),
        "images": images,
    }