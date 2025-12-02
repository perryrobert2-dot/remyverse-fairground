import os
import json
import datetime
import random
import re
import shutil
import zipfile
from openai import OpenAI
import google.generativeai as genai
from google.cloud import storage # Required for GCS upload

# --- CONFIGURATION ---
local_client = OpenAI(base_url="http://192.168.0.52:1234/v1", api_key="lm-studio", timeout=20.0)
GOOGLE_KEY = "AIzaSyCINOm3_0n3z-1D6WJNJyg7t_TYRwTt5y8"

SATIRE_SYSTEM_INSTRUCTION = "You are an intellectual, cynical dachshund writing a highly satirical, hyper-local newspaper called The Remy Digest. All content must be treated as fictional and exaggerated social commentary on suburban life in the Northern Beaches, Australia. DO NOT write factual journalism; write creative, opinionated content based on the prompt."

try:
    genai.configure(api_key=GOOGLE_KEY)
except:
    pass

# --- GCS ASSET CONFIGURATION ---
# FIX: Using the verified path provided by the user, ending with /deep-dive/
GCS_BASE_URL_WITH_PREFIX = "https://storage.googleapis.com/remys-digest-public-assets/deep-dive/"

# Array of image names matching the day of the week (0=Mon, 6=Sun)
LIBRARIAN_IMAGE_NAMES = [
    "monday_librarian.png",    # 0 - Monday
    "tuesday_librarian.png",   # 1 - Tuesday
    "wednesday_librarian.png", # 2 - Wednesday
    "thursday_librarian.png",  # 3 - Thursday
    "friday_librarian.png",    # 4 - Friday
    "saturday_librarian.png",  # 5 - Saturday
    "sunday_librarian.png"     # 6 - Sunday
]
# -----------------------------------

# Determine Project Root (Robust Path Logic)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = SCRIPT_DIR if os.path.exists(os.path.join(SCRIPT_DIR, "fairground")) else os.path.dirname(SCRIPT_DIR)
NEWS_DUMP_FILE = os.path.join(PROJECT_ROOT, "scout", "news_dump.txt")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "fairground", "public", "data", "current_issue.json")

# New Directories for Deep Dive Integration
ASSET_ROOT = os.path.join(PROJECT_ROOT, "fairground", "public")
DEEP_DIVE_ASSETS_PATH = os.path.join(ASSET_ROOT, "deep_dive_assets") 
STUDIO_EXPORTS_PATH = os.path.join(PROJECT_ROOT, "Remy_Studio_Exports") 
STUDIO_ARCHIVE_PATH = os.path.join(STUDIO_EXPORTS_PATH, "ARCHIVE")

# --- GRIPES DB (Unchanged) ---
LOCAL_GRIPES = [
    "The 'Binfluencer' on our street put the Blue bin out on Yellow week. We all followed him. Now the whole street is wrong.",
    "Why is the B-Line double-decker always set to 'Arctic'? It's a 40-minute freeze from Dee Why to Wynyard.",
    "Trucks from the industrial estate are using South Creek Road as a drag strip at 5am.",
    "I tried to park at Dee Why beach on Sunday. Ended up parking in Narraweena and hiking down.",
    "The Cockatoos have started eating my deck railing again. They look you right in the eye while they do it.",
    "Getting stuck in the Warringah Mall carpark vortex. I spent more time trying to exit than shopping.",
    "To the person who keeps hitting golf balls from the range into my gutter: You have a slice.",
    "The B-Line dash. The bus arrives, everyone runs, and then we sit at the Spit Bridge for 20 minutes."
]

# --- TEXT SURGEONS AND PARSERS ---
def clean_and_format(text):
    if not text: return ""
    text = re.sub(r'(HEADLINE|TITLE|TEASER|BODY|DESCRIPTION|TOPIC|RATING|VERDICT|LETTER):', '', text, flags=re.IGNORECASE).strip()
    text = re.sub(r'^[=\-]{3,}', '', text, flags=re.MULTILINE).strip()
    text = re.sub(r'(News dump|From the desk|News:|Prof Remy)', '', text, flags=re.IGNORECASE).strip()

    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    for s in sentences:
        if not s.strip(): continue
        current_chunk.append(s)
        if len(current_chunk) >= 2:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk: chunks.append(" ".join(current_chunk))
    text = "\n\n".join(chunks)

    text = text.lower()
    sentences = text.split('. ')
    capitalized = [s.capitalize() for s in sentences]
    return '. '.join(capitalized)

def split_editorial(text):
    parts = text.split("|||")
    title = "The Professor's Analysis"
    teaser = "A wealth of news awaits you today."
    body = text

    if len(parts) >= 3:
        title = clean_and_format(parts[0])
        teaser = clean_and_format(parts[1])
        body = clean_and_format(parts[2])
    
    bad_words = ["news dump", "november", "december", "january", "october", "2024", "2025"]
    if any(x in title.lower() for x in bad_words) or len(title) > 100:
        title = "The Professor's Analysis"

    return {"title": title, "teaser": teaser, "body": body}

def read_clean_news():
    if not os.path.exists(NEWS_DUMP_FILE): return ""
    with open(NEWS_DUMP_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) > 3:
        return "".join(lines[3:])
    return "".join(lines)

def generate_text(prompt, context=""):
    
    if GOOGLE_KEY == "PASTE_YOUR_KEY_HERE":
        print("   (❌ Cloud API Key Missing! Check line 12.)")
        return "Brain Offline: API Key Missing."

    is_editorial = "Professor Remy" in prompt
    model_name = 'gemini-2.5-pro' if is_editorial else 'gemini-2.5-flash'
    
    user_content = prompt
    if is_editorial and context:
         user_content = f"INSTRUCTION: {prompt}\n\nBACKGROUND INFO (Use only if relevant): {context}"
        
    try:
        print(f"   (🧠 Consulting {model_name}...)")
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SATIRE_SYSTEM_INSTRUCTION
        )
        
        response = model.generate_content(user_content)

        if not response.text:
            if response.prompt_feedback.block_reason:
                print("   (⛔ CENSOR BLOCK: Prompt was rejected by safety filter.)")
                return "CENSOR_FAILURE: The requested content was blocked. Topic must be revised."
            
        return response.text.strip()
    except Exception as e:
        print(f"   (❌ Cloud Brain Error: {e})")
        if "Outraged of Cromer" in prompt:
            return "TOPIC: System Failure ||| BODY: Please check API key/internet connection."
        elif "Professor Remy" in prompt:
             return "HEADLINE: Local AI Failure ||| TEASER: Cannot connect to the server. ||| BODY: Content unavailable."
        return "Brain Offline: Connection Failed."

def get_editorial_topic():
    print("\n📰 --- MORNING NEWS MEETING --- 📰")
    if os.path.exists(NEWS_DUMP_FILE):
        with open(NEWS_DUMP_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        headlines = [line.strip() for line in lines[3:] if len(line) > 20][:5]
    else:
        headlines = []

    for i, h in enumerate(headlines):
        print(f"   [{i+1}] {h[:60]}...")
    
    print("\n   [C] Custom Topic (Type your own)")
    choice = input("\n👉 Select a Story Number or type a Custom Topic: ")

    if choice.isdigit() and 1 <= int(choice) <= len(headlines):
        selected_topic = headlines[int(choice)-1]
    else:
        selected_topic = choice if choice.lower() != 'c' else input("   Enter Custom Topic: ")
        
    print(f"\n✅ Topic Locked: {selected_topic}")
    return selected_topic

def parse_with_fallback(text, keys):
    parts = text.split("|||")
    result = {}
    for i, part in enumerate(parts):
        if i < len(keys):
            val = part.split(":", 1)[-1].strip() if ":" in part else part.strip()
            result[keys[i]] = clean_and_format(val)
    return result

# --- DEEP DIVE MANAGER ---
def find_content_files(root_dir):
    """Recursively searches for metadata.json and content.md."""
    files = {'metadata': None, 'content': None, 'image_dir': None}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'metadata.json' in filenames and 'content.md' in filenames:
            files['metadata'] = os.path.join(dirpath, 'metadata.json')
            files['content'] = os.path.join(dirpath, 'content.md')
            
            if 'images' in dirnames:
                files['image_dir'] = os.path.join(dirpath, 'images')
            elif os.path.exists(os.path.join(dirpath, 'images')):
                 files['image_dir'] = os.path.join(dirpath, 'images')
            
            return files
    return files

def extract_latest_zip():
    """Finds the latest ZIP export and extracts its content to a temporary folder."""
    
    temp_extract_path = os.path.join(STUDIO_EXPORTS_PATH, "TEMP_LATEST_EXPORT")
    if os.path.exists(temp_extract_path):
        shutil.rmtree(temp_extract_path)
    os.makedirs(temp_extract_path, exist_ok=True)
    
    zip_files = [f for f in os.listdir(STUDIO_EXPORTS_PATH) if f.endswith('.zip')]
    if not zip_files:
        print("   ❌ ERROR: No .zip archive found in the exports folder.")
        return None, None
        
    latest_zip_name = max(zip_files, key=lambda f: os.path.getmtime(os.path.join(STUDIO_EXPORTS_PATH, f)))
    latest_zip_path = os.path.join(STUDIO_EXPORTS_PATH, latest_zip_name)
    
    try:
        with zipfile.ZipFile(latest_zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_path)
        print(f"   ✅ Successfully extracted {latest_zip_name}")
        
        extracted_folder_name = os.listdir(temp_extract_path)[0]
        return os.path.join(temp_extract_path, extracted_folder_name), latest_zip_path
        
    except Exception as e:
        print(f"   ❌ EXTRACTION FAILED: {e}")
        return None, None

def sync_deep_dive():
    """Manages the Deep Dive Library: Extracts zip, copies images, reads content, and archives the ZIP."""
    
    extracted_content_path, original_zip_path = extract_latest_zip()
    if not extracted_content_path:
        return {"title": "Library Offline", "body": "No valid deep dive archive found or extraction failed."}

    content_files = find_content_files(extracted_content_path)

    if not content_files['metadata'] or not content_files['content']:
        print(f"   ❌ Export is incomplete. Missing metadata.json or content.md after extraction.")
        return {"title": "Library Incomplete", "body": "Export archive is missing metadata.json or content.md."}

    # 1. Process Content and Metadata
    with open(content_files['metadata'], 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    with open(content_files['content'], 'r', encoding='utf-8') as f:
        content = f.read()
        
    # --- START GCS UPLOAD ---
    # We assume GCS has been configured outside of this script.
    
    # 2. Sync Images (The GCS Upload - Assumes gsutil or Service Account setup is functional)
    image_path_url = "/deep_dive_assets/" # Fallback/Local URL path
    
    if os.path.exists(GCS_SERVICE_ACCOUNT_KEY_PATH):
        try:
            storage_client = storage.Client.from_service_account_json(GCS_SERVICE_ACCOUNT_KEY_PATH)
            bucket = storage_client.bucket(GCS_BUCKET_NAME)
            
            source_image_folder = content_files['image_dir']
            if source_image_folder:
                for filename in os.listdir(source_image_folder):
                    local_path = os.path.join(source_image_folder, filename)
                    # Upload with a simple prefix
                    remote_path = f"deep-dive-assets/{filename}" 
                    
                    bucket.blob(remote_path).upload_from_filename(local_path)
                
                print(f"   ✅ Upload Complete: Assets synced to GCS.")
                image_path_url = GCS_BASE_URL + "deep-dive-assets/" # Use GCS path for JSON
            
        except Exception as e:
            print(f"   ❌ GCS UPLOAD FAILED: {e}")
            print("   (Reverting to local asset path /deep_dive_assets/)")
            
    else:
        print("   ⚠️ Skipping GCS upload (Key file not found).")
        
    # 3. ARCHIVE THE PROCESSED ZIP FILE
    if not os.path.exists(STUDIO_ARCHIVE_PATH):
        os.makedirs(STUDIO_ARCHIVE_PATH)
    
    archive_zip_name = os.path.basename(original_zip_path)
    shutil.move(original_zip_path, os.path.join(STUDIO_ARCHIVE_PATH, archive_zip_name))
    print(f"   📦 Archived ZIP: {archive_zip_name}")

    # 4. Package for JSON
    deep_dive_data = {
        "title": metadata.get("Topic/Subject", "Remarkable Find"),
        "body": clean_and_format(content),
        "image_path": image_path_url, # Dynamic GCS or local URL
        "author": metadata.get("Author", "The Archivist")
    }

    return deep_dive_data

# --- PROMPTS (Unchanged) ---
PROMPTS = {
    "professor": """You are Professor Remy. Write a satirical Op-Ed about THIS SPECIFIC TOPIC: '{topic}'.
    CRITICAL INSTRUCTION: Write ONLY about '{topic}'. Do not summarize the background info unless it is directly related.
    Format: HEADLINE: [Short Title] ||| TEASER: [Hook] ||| BODY: [300 words]""",
    
    "letter_response": "You are 'Outraged of Cromer'. Write a complaint letter (80 words). Format: TOPIC: [Brief Subject] ||| BODY: [The Rant]",
    "critic": """You are Remy Senior, a famously pompous art critic. Review ONE of the following using sophisticated art jargon: 
    1. 'Peecaso' (Urinary Art Installation) - Focus on scent, fluidity, and ephemeral nature.
    2. 'Barksie' (Chewing/Mud Art) - Focus on raw texture, rebellion, and social commentary.
    3. 'Cat Art' (Dead Mouse/Feathers) - Be scathing, dismissive, and call it vulgar. Explain it lacks depth.
    Format: TITLE: [text] ||| TEASER: [text] ||| BODY: [150 words] ||| RATING: [0-5 Bones]""",
    "pitd": "You are the Curator. Describe a conceptual installation. Format: TITLE: [text] ||| DESCRIPTION: [text]",
    "blotter": "You are the Police Dog. Write a Blotter Report. Format: INCIDENT: [text] ||| LOCATION: [text] ||| DETAILS: [text]",
    "classifieds": "Write 3 short, punchy ads (MAX 40 words total per ad). Use |||. AD1_TYPE: LOST ||| AD1_TITLE: [text] ||| AD1_BODY: [text] ||| AD2_TYPE: SALE ||| AD2_TITLE: [text] ||| AD2_BODY: [text] ||| AD3_TYPE: WANTED ||| AD3_TITLE: [text] ||| AD3_BODY: [text]",
    "aunt": "Auntie Remy. Use |||. MAIN_Q: [Q] ||| MAIN_A: [A] ||| SNAP1_Q: [Q] ||| SNAP1_A: [A] ||| SNAP2_Q: [Q] ||| SNAP2_A: [A]",
    "mystic": "You are The Seer. Horoscope for '{sign}'. MAX 40 words. Output: [Prediction]"
}

def run_newsroom():
    print("🗞️  THE REMY DIGEST (V11.3: GCS Integration Check)")
    
    topic = get_editorial_topic()
    clean_news = read_clean_news()
    
    print("\n⚙️  Ghostwriter is drafting...")
    
    # EDITORIAL (Cloud Brain)
    editorial_raw = generate_text(PROMPTS["professor"].replace("{topic}", topic), clean_news)
    editorial = split_editorial(editorial_raw)
    editorial["author"] = "Professor Remy"

    # Deep Dive Integration
    print("\n📚 SYNC: Checking Deep Dive Assets...")
    deep_dive = sync_deep_dive()
    
    # FILLER CONTENT (Cloud Brain)
    letters = []
    for _ in range(3):
        l_raw = generate_text(PROMPTS["letter_response"], context="")
        l_parsed = parse_with_fallback(l_raw, ["topic", "body"])
        letters.append({
            "topic": l_parsed.get("topic", "Brain Offline: Letter Topic"), 
            "body": l_parsed.get("body", "Brain Offline: Body Text"), 
            "author": random.choice(["Frustrated of Collaroy", "Exasperated of Avalon", "Outraged of Cromer"])
        })

    arts = parse_with_fallback(generate_text(PROMPTS["critic"], context=""), ["title", "teaser", "body", "rating"])
    pitd = parse_with_fallback(generate_text(PROMPTS["pitd"], context=""), ["title", "description"])
    blotter = parse_with_fallback(generate_text(PROMPTS["blotter"], context=""), ["incident", "location", "details"])
    ads = parse_with_fallback(generate_text(PROMPTS["classifieds"], context=""), ["ad1_type", "ad1_title", "ad1_body", "ad2_type", "ad2_title", "ad2_body", "ad3_type", "ad3_title", "ad3_body"])
    advice_raw = generate_text(PROMPTS["aunt"], context="")
    advice_keys = ["main_q", "main_a", "snap1_q", "snap1_a", "snap2_q", "snap2_a"]
    advice = parse_with_fallback(advice_raw, advice_keys)
    advice["main_pseudo"] = "Worried in Warringah"
    advice["snap1_pseudo"] = "Manic in Manly"
    advice["snap2_pseudo"] = "Bored in Brookvale"

    horoscopes = []
    full_zodiac = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    for sign in full_zodiac:
        pred = generate_text(PROMPTS["mystic"].replace("{sign}", sign), context="")
        horoscopes.append({ "sign": sign, "prediction": clean_and_format(pred) })

    full_issue = {
        "meta": { "version": "11.3", "generated_at": datetime.datetime.now().isoformat() },
        "editorial": editorial, "letters": letters, "arts": arts, "pitd": pitd, 
        "blotter": blotter, "ads": ads, "advice": advice, "horoscopes": horoscopes,
        "deep_dive": deep_dive
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f: json.dump(full_issue, f, indent=2)
    print(f"✅ V11.3 Published.")

if __name__ == "__main__":
    run_newsroom()