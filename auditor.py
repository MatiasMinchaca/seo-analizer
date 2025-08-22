import requests
from collections import defaultdict
from config import (
    TITLE_MIN_LENGTH, TITLE_MAX_LENGTH, META_DESC_MIN_LENGTH, 
    META_DESC_MAX_LENGTH, H1_MAX_LENGTH, LOW_WORD_COUNT_THRESHOLD,
    IMAGE_SIZE_THRESHOLD_KB,
    H2_MAX_LENGTH 
)
from crawler import fetch_sitemap

HEADERS = {"User-Agent": "SEO-Audit-Bot/6.0"}

def run_audit(crawled_data, max_links_to_check, sitemap_url=None, enable_image_size_check=False, enable_sitemap_check=False):
    """Runs all SEO checks on the crawled data and returns a dictionary of issues."""
    issues = {}

    # Prepare data for analysis
    titles = {p['url']: p['title'] for p in crawled_data}
    meta_descs = {p['url']: p['meta_descriptions'] for p in crawled_data}
    h1s = {p['url']: p['h1s'] for p in crawled_data}
    h2s = {p['url']: p['h2s'] for p in crawled_data}
    word_counts = {p['url']: p['word_count'] for p in crawled_data}
    canonicals = {p['url']: p['canonicals'] for p in crawled_data}
    images = {p['url']: p['images'] for p in crawled_data}
    hreflangs = {p['url']: p['hreflangs'] for p in crawled_data}

    # Convert crawled_data to a set of URLs for easy comparison
    crawled_urls = {p['url'] for p in crawled_data}

    # --- Run Checks ---
    issues["Missing_Title"] = [{"URL": url} for url, title in titles.items() if not title]
    issues["Short_Titles"] = [{"URL": url, "Title": title, "Length": len(title)} for url, title in titles.items() if title and len(title) < TITLE_MIN_LENGTH]
    issues["Long_Titles"] = [{"URL": url, "Title": title, "Length": len(title)} for url, title in titles.items() if len(title) > TITLE_MAX_LENGTH]
    issues["Duplicate_Titles"] = find_duplicates({k: v for k, v in titles.items() if v})

    issues["Missing_Meta_Desc"] = [{"URL": url} for url, descs in meta_descs.items() if not descs]
    issues["Multiple_Meta_Desc"] = [{"URL": url, "Count": len(descs)} for url, descs in meta_descs.items() if len(descs) > 1]
    issues["Short_Meta_Desc"] = [{"URL": url, "Description": descs[0], "Length": len(descs[0])} for url, descs in meta_descs.items() if len(descs) == 1 and len(descs[0]) < META_DESC_MIN_LENGTH]
    issues["Long_Meta_Desc"] = [{"URL": url, "Description": descs[0], "Length": len(descs[0])} for url, descs in meta_descs.items() if len(descs) == 1 and len(descs[0]) > META_DESC_MAX_LENGTH]
    issues["Duplicate_Meta_Desc"] = find_duplicates({k: v[0] for k, v in meta_descs.items() if len(v) == 1})

    issues["Missing_H1s"] = [{"URL": url} for url, h1_list in h1s.items() if not h1_list]
    issues["Multiple_H1s"] = [{"URL": url, "Count": len(h1_list)} for url, h1_list in h1s.items() if len(h1_list) > 1]
    issues["Long_H1s"] = [{"URL": url, "H1": h1, "Length": len(h1)} for url, h1_list in h1s.items() for h1 in h1_list if len(h1) > H1_MAX_LENGTH]
    issues["Duplicate_H1s"] = find_duplicates({k: v[0] for k, v in h1s.items() if len(v) == 1})

    # New: H2 Checks
    issues["Missing_H2s"] = [{"URL": url} for url, h2_list in h2s.items() if not h2_list]
    issues["Multiple_H2s"] = [{"URL": url, "Count": len(h2_list)} for url, h2_list in h2s.items() if len(h2_list) > 1]
    issues["Long_H2s"] = [{"URL": url, "H2": h2, "Length": len(h2)} for url, h2_list in h2s.items() for h2 in h2_list if len(h2) > H2_MAX_LENGTH]
    issues["Duplicate_H2s"] = find_duplicates({k: v[0] for k, v in h2s.items() if len(v) == 1})

    issues["Low_Word_Count"] = [{"URL": url, "Word Count": count} for url, count in word_counts.items() if count < LOW_WORD_COUNT_THRESHOLD]
    
    missing_alts = []
    for url, img_list in images.items():
        for img in img_list:
            if not img['alt']:
                missing_alts.append({"URL": url, "Image Source": img['src']})
    issues["Img_Missing_Alt"] = missing_alts

    issues["Non_Self_Canonicals"] = [{"URL": url, "Canonical URL": cans[0]} for url, cans in canonicals.items() if len(cans) == 1 and url != cans[0]]

    # --- Large Images Check ---
    if enable_image_size_check:
        print("Checking image sizes... (This may take a while)")
        all_images = {img['src'] for url_imgs in images.values() for img in url_imgs}
        large_images = []
        for img_url in all_images:
            try:
                res = requests.head(img_url, headers=HEADERS, timeout=5, allow_redirects=True)
                size_bytes = int(res.headers.get('Content-Length', 0))
                size_kb = size_bytes / 1024
                if size_kb > IMAGE_SIZE_THRESHOLD_KB:
                    large_images.append({"Image URL": img_url, "Size (KB)": round(size_kb, 2)})
            except requests.RequestException as e:
                print(f"Could not check image size for {img_url}: {e}")
        issues["Large_Images"] = large_images

    # --- Broken Links Check ---
    print("Checking for broken links... (This may take a while)")
    internal_links_from_crawled_pages = [
        link for p in crawled_data for link in p.get("internal_links", [])
    ]
    issues["Broken_Links"] = check_urls_for_broken_links(internal_links_from_crawled_pages, max_links_to_check, "Internal Page Links")

    # --- Sitemap Check ---
    if enable_sitemap_check and sitemap_url:
        sitemap_urls = set(fetch_sitemap(sitemap_url))
        if sitemap_urls:
            sitemap_issues = check_sitemap_issues(crawled_urls, sitemap_urls, max_links_to_check)
            issues.update(sitemap_issues)
        else:
            print(f"  -> Warning: No URLs found in sitemap at {sitemap_url}")
    
    # --- Hreflang Check ---
    print("Checking hreflang tags...")
    # Pages missing any hreflang tags
    issues["Missing_Hreflang"] = [{"URL": url} for url, hflangs in hreflangs.items() if not hflangs]
    
    # Placeholder for more advanced hreflang validation (e.g., broken links, return tags)
    # issues["Hreflang_Issues"] = check_advanced_hreflang_issues(crawled_data)

    return {key: val for key, val in issues.items() if val}

def check_urls_for_broken_links(urls_to_check, max_to_check, link_source="Page Content"):
    """Checks a list of URLs for broken links (404, 5xx, etc.).
    link_source is used for reporting context (e.g., 'Page Content' or 'Sitemap')."""
    broken_links = []
    unique_urls = list(set(urls_to_check))

    # Limit the number of links to check
    limited_urls = unique_urls[:max_to_check]
    print(f"  -> Checking a maximum of {len(limited_urls)} unique links from {link_source}...")

    for url in limited_urls:
        try:
            # Using a fixed timeout of 5 seconds for now
            response = requests.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
            if response.status_code >= 400:
                broken_links.append({"URL": url, "Status Code": response.status_code, "Source": link_source})
        except requests.RequestException as e:
            broken_links.append({"URL": url, "Error": str(e), "Status Code": "N/A", "Source": link_source})
    return broken_links

def check_sitemap_issues(crawled_urls, sitemap_urls, max_links_to_check):
    """Compares crawled URLs with sitemap URLs and identifies related issues."""
    sitemap_issues = defaultdict(list)

    # URLs in sitemap but not crawled
    sitemap_only_urls = sitemap_urls - crawled_urls
    for url in sitemap_only_urls:
        sitemap_issues["Sitemap_Only_URLs"].append({"URL": url})

    # URLs crawled but not in sitemap
    crawled_only_urls = crawled_urls - sitemap_urls
    for url in crawled_only_urls:
        sitemap_issues["Crawled_Only_URLs"].append({"URL": url})

    # Check for broken links within sitemap URLs
    # Convert set to list for check_urls_for_broken_links
    sitemap_broken_links = check_urls_for_broken_links(list(sitemap_urls), max_links_to_check, "Sitemap")
    sitemap_issues["Sitemap_Broken_Links"].extend(sitemap_broken_links)

    return sitemap_issues

def find_duplicates(data_dict):
    """Finds duplicate values in a dictionary and returns a list of issue dicts."""
    dupe_map = defaultdict(list)
    for url, text in data_dict.items():
        if text:
            dupe_map[text].append(url)
    
    duplicate_issues = []
    for text, urls in dupe_map.items():
        if len(urls) > 1:
            for url in urls:
                duplicate_issues.append({"URL": url, "Duplicate Text": text})
    return duplicate_issues