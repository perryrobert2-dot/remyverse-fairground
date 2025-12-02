import os
import json
import random
import shutil
import datetime
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---
BASE_DIR = r"C:\RemyVerse"
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")

# Website Connections
WEB_IMG_DIR = os.path.join(BASE_DIR, "fairground", "public", "issues")
WEB_DATA_DIR = os.path.join(BASE_DIR, "fairground", "public", "data")
CALENDAR_FILE = os.path.join(BASE_DIR, "editorial_calendar.json")

# Visual Settings (Calibrated for 4K)
NOTE_SIZE = (500, 700)  
NOTE_XY = (2500, 300)   
TEXT_COLOR = (0, 0, 0)
PAPER_COLOR = (255, 255, 250)

# Fonts (Filename, Size)
FONT_HEADLINE = ("ComicNeue-Bold.ttf", 60)
FONT_BODY = ("ComicNeue-Regular.ttf", 32)
FONT_STAMP = ("Stamp.ttf", 100)

def ensure_dirs():
    """Create necessary directories if they don't exist."""
    for d in [OUTPUT_DIR, WEB_IMG_DIR, WEB_DATA_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"Created directory: {d}")

def get_font(font_name, size):
    """Load a font or fallback to default."""
    try:
        path = os.path.join(ASSETS_DIR, font_name)
        return ImageFont.truetype(path, size)
    except IOError:
        print(f"Warning: Could not load {font_name}. Using default.")
        return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within a specific width."""
    lines = []
    words = text.split()
    if not words: return []
    
    current_line = words[0]
    for word in words[1:]:
        test_line = current_line + " " + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def create_note(headline, body, stamp_text):
    """Generates the paper note image with text and stamp."""
    note = Image.new('RGBA', NOTE_SIZE, PAPER_COLOR)
    draw = ImageDraw.Draw(note)
    
    # Headline
    font_h = get_font(*FONT_HEADLINE)
    draw.text((40, 40), headline, font=font_h, fill=TEXT_COLOR)
    
    # Body
    font_b = get_font(*FONT_BODY)
    lines = wrap_text(body, font_b, NOTE_SIZE[0] - 80, draw)
    y_text = 130
    for line in lines:
        draw.text((40, y_text), line, font=font_b, fill=TEXT_COLOR)
        y_text += 40
        
    # Stamp
    if stamp_text:
        font_s = get_font(*FONT_STAMP)
        stamp_img = Image.new('RGBA', (500, 250), (255, 255, 255, 0))
        stamp_draw = ImageDraw.Draw(stamp_img)
        stamp_draw.text((10, 10), stamp_text.upper(), font=font_s, fill=(200, 0, 0, 180)) 
        rotated_stamp = stamp_img.rotate(random.randint(-15, 15), expand=True)
        note.paste(rotated_stamp, (NOTE_SIZE[0] - 350, NOTE_SIZE[1] - 250), rotated_stamp)
        
    # Pin
    try:
        pin = Image.open(os.path.join(ASSETS_DIR, "pin.png")).convert("RGBA")
        pin = pin.resize((60, 60))
        note.paste(pin, (int(NOTE_SIZE[0]/2)-30, 10), pin)
    except:
        pass 

    return note

def publish_to_web_data(entry):
    """Saves the FULL RICH DATA so the website can read it."""
    json_path = os.path.join(WEB_DATA_DIR, "current_issue.json")
    
    # --- DATE CALCULATOR (Target: Wednesday) ---
    today = datetime.datetime.now()
    # Wednesday is index 2 (Mon=0, Tue=1, Wed=2...)
    wednesday_index = 2 
    days_ahead = (wednesday_index - today.weekday() + 7) % 7
    
    # If today is Wednesday, this keeps it today.
    target_date = today + datetime.timedelta(days=days_ahead)
    formatted_date = target_date.strftime("%B %d, %Y")
    iso_date = target_date.strftime("%Y-%m-%d")
    # -------------------------------------------

    web_data = {
        "headline": entry.get('topic', 'Breaking News'),
        "body": entry.get('details', 'No details available.'),
        
        # USE THE CALCULATED WEDNESDAY DATE
        "date": formatted_date, 
        
        "author": "The Editor",
        "stamp": entry.get('stamp', 'FRESH'),
        
        # New Sections (Remy Senior & Co)
        "arts": entry.get("arts", {
            "title": "Review: The Vacuum Cleaner",
            "rating": "0/5 Paws",
            "body": "It screams. It sucks. It is the void manifest. I hate it."
        }),
        "horoscope": entry.get("horoscope", "The stars are dim today. Stay in bed."),
        "classified": entry.get("classified", ["Wanted: Quiet", "Lost: Hope"]),
        "pitd": entry.get("pitd", {
            "topic": "Is The Ball Real?",
            "contenders": "Remy Senior vs. The Concept of Object Permanence"
        }),
        "agony": entry.get("agony", "Get over it, kid.")
    }
    
    # 1. WRITE LIVE ISSUE
    with open(json_path, 'w') as f:
        json.dump(web_data, f, indent=4)
    print(f"[DATA] Published rich text to: {json_path}")
    print(f"[DATA] Issue Date set to: {formatted_date}")

    # 2. ARCHIVE ISSUE (For History)
    archive_filename = f"issue_{iso_date}.json"
    archive_path = os.path.join(WEB_DATA_DIR, archive_filename)
    with open(archive_path, 'w') as f:
        json.dump(web_data, f, indent=4)
    print(f"[ARCHIVE] Saved permanent record to: {archive_filename}")

def generate_issue(entry):
    """Composites the note onto the background and saves."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(x for x in str(entry.get('topic', 'news')) if x.isalnum())[:10]
    filename = f"issue_{timestamp}_{safe_topic}.png"
    
    # 1. Load Background
    bg_files = [f for f in os.listdir(ASSETS_DIR) if f.startswith("template_") and f.endswith(".png")]
    if not bg_files:
        print("Error: No 'template_*.png' found in Assets.")
        return
    bg_choice = random.choice(bg_files)
    background = Image.open(os.path.join(ASSETS_DIR, bg_choice)).convert("RGBA")
    
    # 2. Generate Note (Main Story Only)
    note = create_note(entry.get('topic', 'News'), entry.get('details', 'Details'), entry.get('stamp', ''))
    
    # 3. Composite
    note = note.rotate(random.uniform(-1, 1), expand=True, fillcolor=(0,0,0,0))
    background.paste(note, NOTE_XY, note)
    
    # 4. Save WIDE (Local)
    local_path = os.path.join(OUTPUT_DIR, filename)
    background.save(local_path)
    
    # 5. PUBLISH Image
    web_path = os.path.join(WEB_IMG_DIR, filename)
    try:
        shutil.copy2(local_path, web_path)
        print(f"[PUBLISH] Image synced: {web_path}")
    except Exception as e:
        print(f"[ERROR] Could not sync image: {e}")

    # 6. PUBLISH Full Data (And Archive)
    publish_to_web_data(entry)

    # 7. Save SQUARE (Social)
    width, height = background.size
    left = (width - height) / 2
    top = 0
    right = (width + height) / 2
    bottom = height
    
    square_img = background.crop((left, top, right, bottom))
    sq_path = os.path.join(OUTPUT_DIR, f"sq_{filename}")
    square_img.save(sq_path)

def main():
    print("--- REMYVERSE PRODUCTION ENGINE (V15.5 - INTERACTIVE) ---")
    ensure_dirs()
    
    # 1. Load Calendar
    if not os.path.exists(CALENDAR_FILE):
        print(f"❌ Error: No calendar found at {CALENDAR_FILE}")
        return

    with open(CALENDAR_FILE, 'r') as f:
        try:
            calendar = json.load(f)
            # Force list format for easier handling
            if isinstance(calendar, dict): calendar = [calendar]
        except json.JSONDecodeError:
            print("Error: JSON file is corrupt.")
            return

    # 2. The Menu
    print("\n📅 UPCOMING EDITORIAL SLOTS:")
    for i, entry in enumerate(calendar):
        print(f"   [{i+1}] {entry.get('topic', 'Untitled')}")
    
    # 3. The Choice
    print("\n   [Q] Quit")
    choice = input("\n👉 Which topic is for THIS Wednesday? (Enter number): ")
    
    if choice.lower() == 'q':
        print("Exiting.")
        return

    if choice.isdigit() and 1 <= int(choice) <= len(calendar):
        selected_entry = calendar[int(choice)-1]
        print(f"\n✅ Selected: {selected_entry.get('topic')}")
        
        # 4. Generate just that one
        generate_issue(selected_entry)
        
    else:
        print("❌ Invalid selection.")

    print("--- RUN COMPLETE ---")

if __name__ == "__main__":
    main()