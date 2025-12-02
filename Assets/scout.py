import feedparser
import time
import os

# --- CONFIGURATION ---
TARGETS = {
    "Manly Observer": "https://manlyobserver.com.au/feed/",
    "The Guardian (Aus)": "https://www.theguardian.com/au/rss",
    "ABC News (Sydney)": "https://www.abc.net.au/news/feed/1088/rss.xml"
}

# Determine base directory (where the script is running from)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Check if we are in root or Assets. If 'scout' folder is not here, try parent.
if os.path.exists(os.path.join(SCRIPT_DIR, "scout")):
    PROJECT_ROOT = SCRIPT_DIR
else:
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

OUTPUT_FILE = os.path.join(PROJECT_ROOT, "scout", "news_dump.txt")

def run_recon():
    print("\n🔭 SCOUT REPORT: INCOMING INTEL...")
    print("======================================")
    
    all_headlines = []

    for source, url in TARGETS.items():
        print(f"\nScanning {source}...")
        try:
            feed = feedparser.parse(url)
            # Grab top 3 headlines
            for i in range(min(3, len(feed.entries))):
                entry = feed.entries[i]
                print(f"   [{i+1}] {entry.title}")
                all_headlines.append(entry.title)
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")

    print("\n======================================")
    print("💡 SUGGESTED SATIRE ANGLES:")
    
    for h in all_headlines:
        lower_h = h.lower()
        if "council" in lower_h or "plan" in lower_h:
            print(f"   -> COUNCIL: '{h}'")
        elif "police" in lower_h or "crime" in lower_h:
            print(f"   -> CRIME: '{h}'")
        elif "beach" in lower_h or "weather" in lower_h:
            print(f"   -> LOCAL: '{h}'")

    # Save to file for Night Shift
    try:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"Scout Report Generated: {time.ctime()}\n")
            f.write("======================================\n\n")
            for h in all_headlines:
                f.write(f"{h}\n")
        print(f"\n✅ Intel saved to: {OUTPUT_FILE}")
    except Exception as e:
        print(f"\n❌ Failed to save intel: {e}")

if __name__ == "__main__":
    run_recon()
    input("\nPress Enter to finish...")
