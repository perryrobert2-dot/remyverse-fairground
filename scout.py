import feedparser
import os
import datetime

# --- CONFIGURATION ---
# We force the path to ensure Night Shift can always find it
OUTPUT_DIR = r"C:\RemyVerse\scout"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "news_dump.txt")

# The Listening Posts (RSS Feeds)
FEEDS = {
    "LOCAL (Northern Beaches)": "https://news.google.com/rss/search?q=Northern+Beaches+Council+when:7d&hl=en-AU&gl=AU&ceid=AU:en",
    "STATE (NSW)": "https://www.abc.net.au/news/feed/1672/rss.xml",  # ABC NSW
    "NATIONAL (Australia)": "https://www.theguardian.com/au/rss"     # Guardian Aus
}

def clean_html(raw_html):
    """Simple cleaner to remove HTML tags from summaries."""
    from xml.etree.ElementTree import fromstring
    try:
        return ''.join(fromstring(f'<root>{raw_html}</root>').itertext())
    except:
        return raw_html

def scout_news():
    print("🔭 Scout is scanning the horizon...")

    # Ensure the folder exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"   Created directory: {OUTPUT_DIR}")
    
    all_stories = []
    
    for category, url in FEEDS.items():
        print(f"   Listening to: {category}...")
        try:
            feed = feedparser.parse(url)
            
            # Grab top 5 stories from each feed
            for entry in feed.entries[:5]:
                headline = entry.title
                
                # Google News puts the source at the end "Headline - Source", let's clean it
                if " - " in headline:
                    headline = headline.rsplit(" - ", 1)[0]
                
                all_stories.append(f"[{category}] {headline}")
                
        except Exception as e:
            print(f"❌ Error scanning {category}: {e}")

    # Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        header = f"NEWS DUMP FOR {datetime.date.today().strftime('%d %B %Y')}\n"
        f.write(header + "="*40 + "\n\n")
        
        for i, story in enumerate(all_stories, 1):
            f.write(f"{i}. {story}\n")
            
    print(f"✅ Scout report saved to: {OUTPUT_FILE}")
    print(f"   Found {len(all_stories)} stories.")

if __name__ == "__main__":
    scout_news()