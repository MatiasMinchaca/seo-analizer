# --- CHECKS TO RUN ---
# Warning: Enabling image size check will significantly slow down the audit
ENABLE_IMAGE_SIZE_CHECK = False 

# --- REPORT STYLING ---
HEADER_COLOR = "9a86ff"

# --- SEO THRESHOLDS ---
TITLE_MIN_LENGTH = 30
TITLE_MAX_LENGTH = 60
META_DESC_MIN_LENGTH = 70
META_DESC_MAX_LENGTH = 160
H1_MAX_LENGTH = 70
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
    # Content
    "Low_Word_Count": {
        "sheet_name": "Low Word Count",
        "description": f"Issue: Pages with fewer than {LOW_WORD_COUNT_THRESHOLD} words, which may be perceived as thin content.",
        "recommendation": "Recommendation: Expand the content on these pages to provide more value to users and search engines."
    },
    # Images & Performance
    "Img_Missing_Alt": {
        "sheet_name": "Images Missing Alt Text",
        "description": "Issue: Images without alt text, affecting accessibility and image SEO.",
        "recommendation": "Recommendation: Add descriptive alt text to all important images."
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
}