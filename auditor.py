from collections import defaultdict
import requests
from config import (
    TITLE_MIN_LENGTH, TITLE_MAX_LENGTH, META_DESC_MIN_LENGTH, 
    META_DESC_MAX_LENGTH, H1_MAX_LENGTH, LOW_WORD_COUNT_THRESHOLD,
    ENABLE_IMAGE_SIZE_CHECK, IMAGE_SIZE_THRESHOLD_KB
)

HEADERS = {"User-Agent": "SEO-Audit-Bot/6.0"}

def run_audit(crawled_data):
    """Runs all SEO checks on the crawled data and returns a dictionary of issues."""
    issues = {}

    # Prepare data for analysis
    titles = {p['url']: p['title'] for p in crawled_data}
    meta_descs = {p['url']: p['meta_descriptions'] for p in crawled_data}
    h1s = {p['url']: p['h1s'] for p in crawled_data}
    word_counts = {p['url']: p['word_count'] for p in crawled_data}
    canonicals = {p['url']: p['canonicals'] for p in crawled_data}
    images = {p['url']: p['images'] for p in crawled_data}

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

    issues["Low_Word_Count"] = [{"URL": url, "Word Count": count} for url, count in word_counts.items() if count < LOW_WORD_COUNT_THRESHOLD]
    
    missing_alts = []
    for url, img_list in images.items():
        for img in img_list:
            if not img['alt']:
                missing_alts.append({"URL": url, "Image Source": img['src']})
    issues["Img_Missing_Alt"] = missing_alts

    issues["Non_Self_Canonicals"] = [{"URL": url, "Canonical URL": cans[0]} for url, cans in canonicals.items() if len(cans) == 1 and url != cans[0]]

    # --- Large Images Check ---
    if ENABLE_IMAGE_SIZE_CHECK:
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

    return {key: val for key, val in issues.items() if val}

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