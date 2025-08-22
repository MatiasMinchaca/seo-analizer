from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
from utils import normalize_url

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
    h2s = [h2.get_text(strip=True) for h2 in soup.find_all("h2")]

    # --- Canonicals ---
    canonical_tags = soup.find_all("link", rel="canonical")
    # Normalize canonical URLs as well
    canonicals = [normalize_url(tag["href"].strip()) for tag in canonical_tags if tag.has_attr("href")]

    # --- Hreflang Tags ---
    hreflang_tags = []
    for link_tag in soup.find_all("link", rel="alternate", hreflang=True):
        if link_tag.has_attr("href") and link_tag.has_attr("hreflang"):
            hreflang_tags.append({
                "hreflang": link_tag["hreflang"].strip(),
                "href": normalize_url(link_tag["href"].strip())
            })

    # --- Content Analysis ---
    text_content = soup.get_text(separator=' ', strip=True)
    word_count = len(text_content.split())
    content_hash = hashlib.sha256(text_content.encode('utf-8')).hexdigest()

    # --- Links ---
    internal_links = set()
    external_links = set()
    all_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href or href.startswith(('#', 'mailto:', 'tel:')):
            continue
        
        full_url = urljoin(url, href)
        # Normalize every link found
        normalized_link = normalize_url(full_url)
        parsed_full_url = urlparse(normalized_link)

        # Get anchor text
        anchor_text = a.get_text(strip=True)

        all_links.append({"url": normalized_link, "anchor_text": anchor_text})

        if parsed_full_url.netloc.replace("www.", "") == base_netloc:
            internal_links.add(normalized_link)
        else:
            external_links.add(normalized_link)

    # --- Images (with lazy loading and data URI handling) ---
    images = []
    for img in soup.find_all("img"):
        # Prioritize data-src for lazy-loaded images, then fall back to src
        src = img.get('data-src') or img.get('src', '')
        src = src.strip()

        # Ignore empty and data URIs
        if not src or src.startswith('data:image'):
            continue

        # Prioritize data-alt for lazy-loaded images, then fall back to alt
        alt = img.get('data-alt') or img.get('alt', '')
        
        full_src_url = urljoin(url, src)
        images.append({"src": full_src_url, "alt": alt.strip()})

    return {
        "url": url,
        "title": title,
        "meta_descriptions": meta_descriptions,
        "h1s": h1s,
        "h2s": h2s,
        "canonicals": canonicals,
        "hreflangs": hreflang_tags,
        "word_count": word_count,
        "content_hash": content_hash,
        "internal_links": list(internal_links),
        "external_links": list(external_links),
        "images": images,
        "all_links": all_links,
    }