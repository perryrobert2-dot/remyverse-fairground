import os
import shutil
import glob
import sys
import re

# --- Configuration ---
CONTENT_DIR = "content"
LIVE_FILE = "index.html"
TEMPLATE_FILE = "layout.html"

def get_latest_edition():
    """
    Scans the content directory for the latest HTML edition.
    Assumes filenames are in format: YYYY-MM-DD_edition.html
    """
    if not os.path.exists(CONTENT_DIR):
        print(f"[!] Error: Content directory '{CONTENT_DIR}' does not exist.")
        return None

    # Search for matching files
    pattern = os.path.join(CONTENT_DIR, "*_edition.html")
    files = glob.glob(pattern)

    if not files:
        print("[!] No edition files found in content directory.")
        return None

    # Sort files by name (which works for ISO dates YYYY-MM-DD) descending
    files.sort(reverse=True)
    latest_file = files[0]
    
    return latest_file

def extract_body_content(html_content):
    """
    Extracts the content inside the <body> tags of the generated edition.
    If no body tags are found, returns the whole content.
    """
    # Regex to find everything between <body> and </body>
    match = re.search(r"<body[^>]*>(.*?)</body>", html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return html_content

def publish_edition():
    """
    Merges the latest edition content into the site template and publishes it.
    """
    print("[*] Publisher Module Initialized.")
    
    # 1. Check for Template
    if not os.path.exists(TEMPLATE_FILE):
        print(f"[!] Critical Error: Template file '{TEMPLATE_FILE}' missing.")
        return

    # 2. Find Latest Content
    latest_file = get_latest_edition()
    if not latest_file:
        print("[-] Publishing aborted.")
        return

    print(f"    -> Latest edition found: {latest_file}")

    try:
        # 3. Read Files
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            template_content = f.read()
            
        with open(latest_file, "r", encoding="utf-8") as f:
            edition_full_html = f.read()
            
        # 4. Extract Article Content (remove <html>, <head>, etc from the edition)
        article_body = extract_body_content(edition_full_html)
        
        # 5. Merge Content into Template
        if "{{CONTENT_GOES_HERE}}" in template_content:
            final_html = template_content.replace("{{CONTENT_GOES_HERE}}", article_body)
        else:
            print("[!] Warning: Placeholder {{CONTENT_GOES_HERE}} not found in layout.")
            final_html = template_content + article_body # Fallback append
            
        # 6. Publish to Live Site
        with open(LIVE_FILE, "w", encoding="utf-8") as f:
            f.write(final_html)
        
        print(f"[+] SUCCESS: Merged {latest_file} into {LIVE_FILE}")
        print("    The site is now live.")
        
    except IOError as e:
        print(f"[!] Critical Error: File operation failed. {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    publish_edition()