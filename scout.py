import feedparser
import json
import requests
import datetime
import os
import random

# --- CONFIGURATION ---
# Load OpenAustralia Key from newsroom/keys.json
KEY_FILE = os.path.join("newsroom", "keys.json")
API_KEY = None

try:
    with open(KEY_FILE, "r") as f:
        keys = json.load(f)
        API_KEY = keys.get("openaustralia")
except Exception:
    print("[!] Warning: Could not load OpenAustralia Key from keys.json")

# Data Sources
MANLY_RSS = "https://manlyobserver.com.au/feed/"
TROPPO_RSS = "https://news.google.com/rss/search?q=site:ntnews.com.au+OR+site:cairnspost.com.au+(croc+OR+crocodile+OR+snake+OR+brawl+OR+beer+OR+naked+OR+weird+OR+attack+OR+ufo+OR+alien)&hl=en-AU&gl=AU&ceid=AU:en"

OUTPUT_FILE = "wire_copy.json"

def fetch_receipt():
    """Fetches the latest political vote/division."""
    print(f"[*] Fetching political receipts...")
    
    if not API_KEY:
        print("[-] No OpenAustralia Key found. Skipping Receipt.")
        return None

    # Endpoint: OpenAustralia getDivisions
    url = f"https://www.openaustralia.org.au/api/getDivisions?key={API_KEY}&output=json"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    "status": "success",
                    "bill_title": data[0].get('name', 'Unknown Bill'),
                    "date": data[0].get('date', 'Unknown Date'),
                    "house": data[0].get('house', 'representatives')
                }
        else:
            print(f"[!] OpenAustralia API Auth Failed: {response.status_code}")
    except Exception as e:
        print(f"[!] Connection Error: {e}")
    
    return None

def fetch_rss(url, limit=3):
    """Fetches headlines from an RSS feed."""
    print(f"[*] Fetching RSS: {url}...")
    try:
        feed = feedparser.parse(url)
        headlines = []
        for entry in feed.entries[:limit]:
            headlines.append(entry.title)
        return headlines
    except Exception as e:
        print(f"[!] RSS Error: {e}")
        return []

def run_scout():
    # 1. Get Receipt
    receipt_data = fetch_receipt()
    if not receipt_data:
        receipt_data = {"status": "failed", "bill_title": None}

    # 2. Get Local News (Manly)
    local_news = fetch_rss(MANLY_RSS)

    # 3. Get Troppo News (NT/Weird)
    troppo_news = fetch_rss(TROPPO_RSS)

    # 4. Construct Wire Copy
    wire_data = {
        "status": "ready",
        "timestamp": str(datetime.datetime.now()),
        "receipt": receipt_data,
        "red_balloon": {
            "prime_local": {
                "source": "Manly Observer",
                "headlines": local_news
            },
            "elsewhere_troppo": {
                "source": "NT News / Google Proxy",
                "headlines": troppo_news,
                "flavor": "chaotic"
            }
        }
    }

    # 5. Save to File
    with open(OUTPUT_FILE, "w") as f:
        json.dump(wire_data, f, indent=2)
    
    print(f"[+] Wire Copy Updated")

if __name__ == "__main__":
    run_scout()