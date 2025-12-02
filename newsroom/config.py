# newsroom/config.py
import os
from pathlib import Path

# GLOBAL SETTINGS
BASE_DIR = Path(__file__).parent.parent

# 1. DIRECTORIES
# FIX: Added 'fairground' to the path so the website can see the file
OUTPUT_DIR = os.path.join(BASE_DIR, 'fairground', 'public', 'data') 
ASSETS_DIR = os.path.join(BASE_DIR, 'fairground', 'public', 'stock') # Updated for safety too

# 2. CRITICAL FILE PATHS
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'current_issue.json')
NEWS_DUMP_FILE = os.path.join(BASE_DIR, 'scout', 'news_dump.txt')

# 3. GOOGLE GEMINI API KEY
GOOGLE_API_KEY = "AIzaSyCLQmcxSKUBtYmfZxiQNgCG9YTP13U3Ewg" # <--- MAKE SURE YOUR KEY IS HERE

# 4. THE VISUAL DIRECTOR'S ASSET MAP
ASSET_LIBRARY = {
    # --- NEWS / EDITORIAL ---
    "editor": "Academic Portrait.jpg",
    "news": "Newspaper Editor Look.jpg",
    "politics": "Politician Suit.jpg",
    
    # --- POLICE / CRIME ---
    "police": "Cartoon Policeman.png",
    "crime": "Detective Ibis.jpg",
    "siren": "Blue Suit and Red Tie.jpg",

    # --- LIFESTYLE / REAL ESTATE ---
    "real estate": "The Real Estate Agent.jpg",
    "agent": "The Sly Cat Agent.jpg",
    "property": "Modern House.jpg",
    "box": "Cardboard Box Stacks.jpg",
    "minimalist": "Giant Saturated Cardboard Box.jpg",
    
    # --- SUBURBAN GRIPES ---
    "suv": "4WD Outside Cafe.jpg",
    "parking": "Badly Parked 4WD.jpg",
    "car": "Red 4WD Facing Cafe.png",
    "traffic": "Traffic Jam Props.jpg",
    "bin": "Bins on a Delineated Curb.jpg",
    "rubbish": "Overflowing Street Bin Cascade.jpg",
    "noise": "Shouting Clown Profile.png",

    # --- ARTS / CULTURE ---
    "critic": "Grumpy Maltese with Specs.jpg",
    "art": "The Artistic Cat Painter.jpg",
    "ibis": "Architect Ibis.jpg",
    "theatre": "Lecture Hall Pose.jpg",
    
    # --- SPORTS ---
    "zoomie": "Dynamic Angry Dachshund.jpg",
    "sport": "Referee and Accessories.jpg",
    "netball": "Netball Post Detail.jpg",
    "whistle": "Referee and Accessories.jpg",
    
    # --- MYSTIC ---
    "mystic": "Gemini Concept.jpg",
    "zodiac": "Gemini Concept.jpg"
}

def get_visual_filename(text, default_tag="news"):
    """
    Scans the story text for keywords and returns the matching filename.
    """
    text_lower = text.lower()
    
    # 1. Check for specific matches in the library
    for keyword, filename in ASSET_LIBRARY.items():
        if keyword in text_lower:
            return filename
            
    # 2. Fallback based on tag if it exists
    if default_tag in ASSET_LIBRARY:
        return ASSET_LIBRARY[default_tag]

    # 3. ABSOLUTE FALLBACK
    return "Snarling Clown Dachshund.png"