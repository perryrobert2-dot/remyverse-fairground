# newsroom/main.py
import json
import os
import datetime
from newsroom.config import OUTPUT_PATH, NEWS_DUMP_FILE
from newsroom.desks import news_desk, lifestyle_desk, arts_desk, sports_desk

def get_user_topic():
    print("\n📰 --- MORNING NEWS MEETING --- 📰")
    
    headlines = []
    if os.path.exists(NEWS_DUMP_FILE):
        try:
            with open(NEWS_DUMP_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            headlines = [l.strip() for l in lines if len(l) > 20 and not l.startswith("=")]
            for i, h in enumerate(headlines[:5]):
                print(f"   [{i+1}] {h[:60]}...")
        except:
            print("   (Scout report unreadable)")
    else:
        print("   (Scout report missing)")

    print("\n   [C] Custom Topic")
    choice = input("👉 Select topic (Number or 'C'): ")
    
    if choice.lower() == 'c':
        return input("   Enter Custom Topic: ")
    elif choice.isdigit() and 0 < int(choice) <= len(headlines):
        return headlines[int(choice)-1]
    else:
        return "Life in the Northern Beaches"

def run_night_shift():
    # 1. THE INTERACTIVE PHASE
    selected_topic = get_user_topic()
    print(f"\n🚀 STARTING PRESS RUN: '{selected_topic}'")
    
    # 2. GENERATION PHASE
    print("   ... 🤡 The Editor is writing...")
    editorial = news_desk.get_editorial(selected_topic)
    blotter = news_desk.get_blotter()
    
    print("   ... 📂 Digging through Archives...")
    deep_dive = lifestyle_desk.get_deep_dive()
    
    print("   ... 🐈 The Cats are scheming...")
    real_estate = lifestyle_desk.get_real_estate()
    
    print("   ... 🎨 The Critics are arguing...")
    arts = arts_desk.get_reviews() # List
    
    print("   ... 🏐 The Netball war begins...")
    sports = sports_desk.get_the_circus() # List
    
    # 3. ASSEMBLE (HYBRID STRUCTURE RESTORED)
    full_issue = {
        "meta": {
            "version": "9.8-Hybrid",
            "generated_at": datetime.datetime.now().isoformat()
        },
        "news": {  # DICTIONARY (Fixes the crash)
            "editorial": editorial,
            "blotter": blotter
        },
        "lifestyle": { # DICTIONARY (Fixes the crash)
            "deep_dive": deep_dive,
            "real_estate": real_estate
        },
        "arts": arts,   # LIST
        "sports": sports # LIST
    }
    
    # 4. PUBLISH
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(full_issue, f, indent=2)
        
    print(f"✅ PRESS RUN COMPLETE. Data saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    run_night_shift()