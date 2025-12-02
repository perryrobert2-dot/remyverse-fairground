import feedparser
import time

# --- CONFIGURATION ---
TARGETS = {
    "Manly Observer": "https://manlyobserver.com.au/feed/",
    "The Guardian (Aus)": "https://www.theguardian.com/au/rss",
    "ABC News (Sydney)": "https://www.abc.net.au/news/feed/1088/rss.xml"
}

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

if __name__ == "__main__":
    run_recon()
    input("\nPress Enter to finish...")