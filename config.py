# --- REPORT STYLING ---
HEADER_COLOR = "9a86ff"

# --- SEO THRESHOLDS ---
TITLE_MIN_LENGTH = 30
TITLE_MAX_LENGTH = 60
META_DESC_MIN_LENGTH = 70
META_DESC_MAX_LENGTH = 160
H1_MAX_LENGTH = 70
H2_MAX_LENGTH = 150
LOW_WORD_COUNT_THRESHOLD = 300 # For blog posts or important pages
IMAGE_SIZE_THRESHOLD_KB = 100 # Images larger than this (in KB) will be flagged

# --- ISSUE DEFINITIONS --- 
# This dictionary maps internal issue keys to their descriptions for the report.
ISSUE_DETAILS = {
    # Titles
    "Missing_Title": {
        "sheet_name": "Missing Title",
        "description": "Issue: These pages are missing a <title> tag.",
        "recommendation": "Recommendation: Add a unique, descriptive title to every page."
    },
    "Duplicate_Titles": {
        "sheet_name": "Duplicate Titles",
        "description": "Issue: Two or more pages share the same title.",
        "recommendation": "Recommendation: Write a unique title for each page to differentiate them in search results."
    },
    "Short_Titles": {
        "sheet_name": "Short Titles",
        "description": f"Issue: Titles with fewer than {TITLE_MIN_LENGTH} characters, which are often uninformative.",
        "recommendation": "Recommendation: Expand titles to be more descriptive and engaging."
    },
    "Long_Titles": {
        "sheet_name": "Long Titles",
        "description": f"Issue: Titles with more than {TITLE_MAX_LENGTH} characters may be truncated in search results.",
        "recommendation": "Recommendation: Shorten titles to ensure they display correctly."
    },
    # Meta Descriptions
    "Missing_Meta_Desc": {
        "sheet_name": "Missing Meta Description",
        "description": "Issue: Pages without a meta description are missing an opportunity to attract clicks.",
        "recommendation": f"Recommendation: Add a unique meta description (between {META_DESC_MIN_LENGTH}-{META_DESC_MAX_LENGTH} chars) to each page."
    },
    "Short_Meta_Desc": {
        "sheet_name": "Short Meta Descriptions",
        "description": f"Issue: Meta descriptions with fewer than {META_DESC_MIN_LENGTH} characters.",
        "recommendation": "Recommendation: Expand meta descriptions to provide a more compelling summary of the page content."
    },
    "Long_Meta_Desc": {
        "sheet_name": "Long Meta Descriptions",
        "description": f"Issue: Meta descriptions with more than {META_DESC_MAX_LENGTH} characters will be cut off.",
        "recommendation": "Recommendation: Shorten meta descriptions to fit within the recommended length."
    },
    "Duplicate_Meta_Desc": {
        "sheet_name": "Duplicate Meta Descriptions",
        "description": "Issue: Multiple pages share the same meta description.",
        "recommendation": "Recommendation: Write a unique meta description for each page."
    },
    # H1 Headings
    "Missing_H1s": {
        "sheet_name": "Missing H1",
        "description": "Issue: Pages without an H1 tag, which is key for defining the main topic.",
        "recommendation": "Recommendation: Add a single, relevant H1 tag to every page."
    },
    "Long_H1s": {
        "sheet_name": "H1 Too Long",
        "description": f"Issue: H1 tags with more than {H1_MAX_LENGTH} characters.",
        "recommendation": "Recommendation: Keep H1 tags concise and focused on the main page topic."
    },
    "Multiple_H1s": {
        "sheet_name": "Multiple H1",
        "description": "Issue: Pages with more than one H1 tag, which dilutes the topic signal.",
        "recommendation": "Recommendation: Use only one H1 tag per page. Use H2-H6 for subheadings."
    },
    "Duplicate_H1s": {
        "sheet_name": "Duplicate H1",
        "description": "Issue: Multiple pages share the same primary H1 tag.",
        "recommendation": "Recommendation: Write a unique H1 for each page that reflects its specific content."
    },
    # H2 Headings
    "Missing_H2s": {
        "sheet_name": "Missing H2",
        "description": "Issue: Pages without any H2 tags, which are crucial for content organization.",
        "recommendation": "Recommendation: Add H2 tags to break down content into logical sections and improve readability."
    },
    "Long_H2s": {
        "sheet_name": "H2 Too Long",
        "description": f"Issue: H2 tags with more than {H2_MAX_LENGTH} characters.",
        "recommendation": "Recommendation: Keep H2 tags concise and descriptive of the subsection they introduce."
    },
    "Multiple_H2s": {
        "sheet_name": "Multiple H2",
        "description": "Issue: Pages with an unusually high number of H2 tags might indicate poor content structure.",
        "recommendation": "Recommendation: Review pages with many H2s. Consider using H3-H6 for further content hierarchy or simplifying the structure."
    },
    "Duplicate_H2s": {
        "sheet_name": "Duplicate H2",
        "description": "Issue: Multiple pages share the same primary H2 tag, indicating potential keyword cannibalization or poor differentiation.",
        "recommendation": "Recommendation: Ensure H2s are unique across pages where content significantly differs."
    },
    # Content
    "Low_Word_Count": {
        "sheet_name": "Low Word Count",
        "description": f"Issue: Pages with fewer than {LOW_WORD_COUNT_THRESHOLD} words, which may be perceived as thin content.",
        "recommendation": "Recommendation: Expand the content on these pages to provide more value to users and search engines."
    },
    # Images & Performance
    "Img_Missing_Alt_Attribute": {
        "sheet_name": "Images Missing Alt Attribute",
        "description": "Issue: Images without an 'alt' attribute, affecting accessibility and image SEO.",
        "recommendation": "Recommendation: Add a descriptive alt attribute to all images to improve accessibility and SEO."
    },
    "Large_Images": {
        "sheet_name": "Large Images",
        "description": f"Issue: Images larger than {IMAGE_SIZE_THRESHOLD_KB} KB, which can slow down page load times.",
        "recommendation": "Recommendation: Compress and resize images to reduce their file size without sacrificing quality."
    },
    # Canonicals
    "Non_Self_Canonicals": {
        "sheet_name": "Non-Self-Referencing Canonical",
        "description": "Issue: The canonical URL does not match the page URL.",
        "recommendation": "Recommendation: This may be intentional for duplicate pages. Review to ensure the canonical points to the correct primary page."
    },
    # Hreflang Issues
    "Missing_Hreflang": {
        "sheet_name": "Missing Hreflang Tags",
        "description": "Issue: Pages are missing hreflang tags, which are crucial for international SEO.",
        "recommendation": "Recommendation: Implement hreflang tags on all international/multilingual pages, ensuring each page references itself and all alternate versions."
    },
    "Hreflang_Issues": {
        "sheet_name": "Hreflang Issues (Advanced)",
        "description": "Issue: Potential problems with hreflang implementation (e.g., incorrect syntax, broken URLs, missing return tags). This requires manual inspection.",
        "recommendation": "Recommendation: Manually verify the hreflang implementation using Google Search Console or a third-party tool. Ensure all URLs are valid, self-referencing, and have reciprocal links."
    },
    # Broken Links
    "Broken_Links": {
        "sheet_name": "Broken Links 4xx-5xx",
        "description": "Issue: These links returned a 4xx (client error) or 5xx (server error) status code.",
        "recommendation": "Recommendation: Update or remove these broken links to improve user experience and SEO."
    },
    # Sitemap Issues
    "Sitemap_Only_URLs": {
        "sheet_name": "Sitemap Only URLs",
        "description": "Issue: These URLs are present in the sitemap but were not found during the crawl. This could indicate crawlability issues or outdated sitemap entries.",
        "recommendation": "Recommendation: Verify these URLs are crawlable and reachable. If not, investigate robots.txt, noindex tags, or remove them from the sitemap."
    },
    "Crawled_Only_URLs": {
        "sheet_name": "Crawled Only URLs",
        "description": "Issue: These URLs were found during the crawl but are not present in the sitemap. This means they might not be properly submitted to search engines.",
        "recommendation": "Recommendation: Review these URLs and add important ones to your sitemap to ensure search engines are aware of them."
    },
    "Sitemap_Broken_Links": {
        "sheet_name": "Sitemap Broken Links",
        "description": "Issue: These URLs are listed in the sitemap but returned a 4xx (client error) or 5xx (server error) status code.",
        "recommendation": "Recommendation: Remove or correct these broken links in your sitemap. Broken links in the sitemap can negatively impact crawl efficiency."
    },
}