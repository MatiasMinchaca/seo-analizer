# SEO Audit Tool

This is a Python-based SEO auditing tool that crawls a website to analyze its on-page SEO factors. It generates a comprehensive, multi-sheet Excel report highlighting various issues and providing recommendations for improvement.

## Features

- **Comprehensive SEO Checks:** Analyzes dozens of factors, including:
  - **Titles:** Missing, duplicate, short, and long titles.
  - **Meta Descriptions:** Missing, duplicate, short, and long descriptions.
  - **Headings:** Missing or duplicate H1 tags, long H1s, multiple H1s.
  - **Content:** Low word count pages.
  - **Images:** Images missing alt text and (optionally) images with a large file size.
  - **Canonicals:** Missing, multiple, or non-self-referencing canonical tags.
- **Styled Excel Reports:** Generates a professional `.xlsx` report with issues separated into sheets, including descriptions and recommendations.
- **Interactive Execution:** Prompts for the target URL and page limit at runtime.
- **Configurable:** Advanced options can be configured in the `config.py` file.

## Requirements

- Python 3.x
- The following Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `openpyxl`

You can install all dependencies by running:
```bash
pip install requests beautifulsoup4 pandas openpyxl
```

## How to Run

1.  **Configure the Audit (Optional):**
    - Open the `config.py` file.
    - To enable the check for large images (which can be slow), set `ENABLE_IMAGE_SIZE_CHECK = True`.
    - You can also adjust other thresholds like title length, word count, and image size limits.

2.  **Execute the Script:**
    - Open your terminal or command prompt.
    - Navigate to the script's directory: `cd "c:\Dev\seo analizer\my scripts for SEO"`
    - Run the main script:
      ```bash
      python app.py
      ```

3.  **Provide Input:**
    - The script will prompt you to enter the **Base URL** you want to audit.
    - It will then ask for the **maximum number of pages** to crawl.
    - You can press `Enter` to use the default values shown in the prompt.

## Output

The script will generate two files:

1.  **`seo_audit_report.xlsx`**: A detailed and styled Excel report. The first sheet is a summary, and subsequent sheets detail each specific SEO issue found, along with recommendations.
2.  **`seo_audit_raw_data.csv`**: A CSV file containing the raw data collected for each crawled page. This is useful for more in-depth, custom analysis.
