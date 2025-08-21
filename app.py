import sys
import pandas as pd

from crawler import crawl_site
from auditor import run_audit
from reporter import generate_xlsx_report

def main():
    """Main function to run the full SEO audit process."""
    # --- Get User Input ---
    default_url = "https://example.com"
    base_url_input = input(f"Enter the URL to audit (or press Enter for {default_url}): ")
    base_url = base_url_input or default_url

    default_pages = 100
    while True:
        max_pages_input = input(f"Enter the max number of pages to crawl (or press Enter for {default_pages}): ")
        if not max_pages_input:
            max_pages = default_pages
            break
        try:
            max_pages = int(max_pages_input)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # New: Ask user for image size check preference
    while True:
        enable_image_check_input = input("Enable image size check? (y/n, default: n): ").lower()
        if enable_image_check_input in ('', 'n', 'no'):
            enable_image_size_check = False
            break
        elif enable_image_check_input in ('y', 'yes'):
            enable_image_size_check = True
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    sitemap_url = None
    # New: Ask user for sitemap check preference
    while True:
        enable_sitemap_check_input = input("Enable sitemap check? (y/n, default: y): ").lower()
        if enable_sitemap_check_input in ('', 'y', 'yes'):
            enable_sitemap_check = True
            break
        elif enable_sitemap_check_input in ('n', 'no'):
            enable_sitemap_check = False
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    if enable_sitemap_check:
        default_sitemap_url = f"{base_url.rstrip('/')}/sitemap.xml"
        sitemap_input = input(f"Enter the sitemap URL (or press Enter for {default_sitemap_url}): ")
        sitemap_url = sitemap_input or default_sitemap_url

    print(f"\nStarting SEO audit for {base_url} (max {max_pages} pages)...")
    
    crawled_data = crawl_site(base_url, max_pages)
    
    if not crawled_data:
        print("Crawl failed. Could not retrieve any pages. Please check the BASE_URL and your network connection.")
        sys.exit(1)

    print(f"\nCrawl complete. Found {len(crawled_data)} pages.")
    print("Running SEO audit...")
    
    issues = run_audit(crawled_data, max_pages, sitemap_url, enable_image_size_check, enable_sitemap_check)
    
    if not issues:
        print("Audit finished. No major issues found!")
        sys.exit(0)
        
    print(f"Audit complete. Found {sum(len(v) for v in issues.values())} total issues.")
    print("Generating Excel report...")
    
    generate_xlsx_report(issues, base_url, len(crawled_data))
    
    # Save raw data to CSV for detailed analysis
    try:
        df = pd.DataFrame(crawled_data)
        df.to_csv("seo_audit_raw_data.csv", index=False, encoding="utf-8-sig")
        print(f"Raw data for {len(crawled_data)} pages saved to seo_audit_raw_data.csv")
    except Exception as e:
        print(f"Could not save raw data CSV: {e}")

    print("\nProcess finished successfully.")

if __name__ == "__main__":
    main()