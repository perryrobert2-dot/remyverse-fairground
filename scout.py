import requests
import json
import datetime
import sys
import time
import os
import feedparser

# --- Configuration ---
# API Key for TheyVoteForYou.org.au
API_KEY = os.getenv("TVFY_API_KEY", "Gv2bM9C84dQPFvNnkVBVcidf").strip()

# API Endpoints
TVFY_URLS = [
    "https://theyvoteforyou.org.au/api/v1",
    "https://www.theyvoteforyou.org.au/api/v1"
]

# RSS Feed URLs
RSS_MANLY = "https://manlyobserver.com.au/feed/"

# Updated to use Google News Proxy with Chaos Filter (Crocs, UFOs, Aliens, etc.)
RSS_NT_NEWS = "https://news.google.com/rss/search?q=site:ntnews.com.au+OR+site:cairnspost.com.au+(croc+OR+crocodile+OR+snake+OR+brawl+OR+beer+OR+naked+OR+weird+OR+attack+OR+ufo+OR+alien)&hl=en-AU&gl=AU&ceid=AU:en"

# Fallback for Troppo if NT News is restricted/empty (often happens with NewsCorp feeds)
RSS_TROPPO_FALLBACK = "https://www.betootaadvocate.com/feed/" 

def fetch_rss_headlines(feed_url, limit=3, fallback_url=None):
    """
    Fetches headlines using feedparser. 
    Returns a list of titles.
    """
    print(f"[*] Fetching RSS: {feed_url}...")
    try:
        feed = feedparser.parse(feed_url)
        
        # Check if feed is empty or failed (bozo bit or empty entries)
        if not feed.entries and fallback_url:
            print(f"[!] Primary feed empty. Switching to fallback: {fallback_url}")
            feed = feedparser.parse(fallback_url)

        headlines = []
        for i, entry in enumerate(feed.entries):
            if i >= limit:
                break
            headlines.append(entry.title)
            
        if not headlines:
            return ["No headlines found."]
            
        return headlines

    except Exception as e:
        print(f"[!] RSS Error ({feed_url}): {e}")
        return ["Error fetching feed"]

def determine_party_position(votes, party_name):
    """
    Determines if a party voted Yes or No based on majority rule.
    """
    party_votes = [v['vote'] for v in votes if party_name.lower() in v['party'].lower()]
    
    if not party_votes:
        return None
    
    yes_count = party_votes.count('Aye')
    no_count = party_votes.count('No')
    
    if yes_count > no_count:
        return "Yes"
    elif no_count > yes_count:
        return "No"
    else:
        return "Split"

def get_working_base_url():
    """
    Checks connection to API. Returns valid URL or None.
    """
    if API_KEY == "YOUR_KEY_HERE" or API_KEY == "":
        return None

    for url in TVFY_URLS:
        test_endpoint = f"{url}/divisions.json?key={API_KEY}"
        try:
            response = requests.get(test_endpoint, timeout=5)
            if response.status_code in [401, 403]:
                print(f"[!] API Auth Failed: {response.status_code}")
                return None
            response.raise_for_status()
            return url
        except requests.exceptions.RequestException:
            continue
    return None

def fetch_receipt():
    """
    Fetches voting data.
    Returns a dict with 'status': 'success'/'failed' and details.
    """
    # Initialize failure state
    failure_receipt = {
        "status": "failed",
        "bill_title": None,
        "vote_result": None,
        "duopoly_check": None
    }

    base_url = get_working_base_url()
    
    if not base_url:
        print("[-] API unreachable or unauthorized. Generating Null Receipt.")
        return failure_receipt
        
    print(f"[*] Scanning recent divisions for receipt...")
    
    try:
        # Get recent divisions
        url = f"{base_url}/divisions.json?key={API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        divisions_list = response.json()
        
        # Iterate (Check last 5)
        for i, div_summary in enumerate(divisions_list[:5]):
            div_id = div_summary['id']
            
            # Fetch details
            detail_url = f"{base_url}/divisions/{div_id}.json?key={API_KEY}"
            detail_resp = requests.get(detail_url, timeout=10)
            
            if detail_resp.status_code != 200:
                continue
                
            data = detail_resp.json()
            votes = data.get('votes', [])
            
            labor_pos = determine_party_position(votes, "Labor")
            liberal_pos = determine_party_position(votes, "Liberal")
            
            # Duopoly Check
            if labor_pos and liberal_pos and labor_pos == liberal_pos:
                if labor_pos in ["Yes", "No"]:
                    print(f"[+] FOUND RECEIPT: Division {div_id}")
                    return {
                        "status": "success",
                        "bill_title": data.get('name', 'Unknown Bill'),
                        "vote_result": "Passed" if data.get('passed') else "Failed",
                        "duopoly_check": f"Both Voted {labor_pos}"
                    }
            time.sleep(0.5)

        print("[-] No bipartisan receipt found in recent scan.")
        return failure_receipt

    except Exception as e:
        print(f"[!] API Error during scan: {e}")
        return failure_receipt

def generate_wire_copy():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Fetch Receipts
    receipt_data = fetch_receipt()
    
    # 2. Fetch Red Balloons (Distractions)
    manly_headlines = fetch_rss_headlines(RSS_MANLY, limit=3)
    troppo_headlines = fetch_rss_headlines(RSS_NT_NEWS, limit=2, fallback_url=RSS_TROPPO_FALLBACK)
    
    # 3. Construct JSON
    wire_data = {
        "status": "ready",
        "timestamp": timestamp,
        "receipt": receipt_data,
        "red_balloon": {
            "prime_local": {
                "source": "Manly Observer",
                "headlines": manly_headlines
            },
            "elsewhere_troppo": {
                "source": "NT News (or Fallback)",
                "headlines": troppo_headlines,
                "flavor": "chaotic"
            }
        }
    }
    
    # 4. Save
    filename = "wire_copy.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(wire_data, f, indent=2)
        print(f"[+] Wire Copy Updated")
    except IOError as e:
        print(f"[CRITICAL] Failed to write file: {e}")

if __name__ == "__main__":
    generate_wire_copy()