import os
import json
import datetime
import random
import re
from openai import OpenAI
import google.generativeai as genai

# --- CONFIGURATION ---
local_client = OpenAI(base_url="http://192.168.0.52:1234/v1", api_key="lm-studio")

# !!! PASTE YOUR GOOGLE KEY HERE !!!
GOOGLE_KEY = "AIzaSyCINOm3_0n3z-1D6WJNJyg7t_TYRwTt5y8"

try:
    genai.configure(api_key=GOOGLE_KEY)
except:
    print("⚠️ Google AI Config Warning.")

BASE_DIR = r"C:\RemyVerse"
NEWS_DUMP_FILE = os.path.join(BASE_DIR, "scout", "news_dump.txt")
OUTPUT_PATH = os.path.join(BASE_DIR, "fairground", "public", "data", "current_issue.json")

# --- GRIPES DB ---
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

# --- TEXT SURGEONS ---
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
        print(f"   (🧹 Cleaning bad title: '{title[:20]}...')")
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
    is_editorial = "Professor Remy" in prompt
    
    # CLOUD BRAIN (Gemini 3 Pro)
    if is_editorial and "PASTE_YOUR_KEY_HERE" not in GOOGLE_KEY:
        try:
            print("   (🧠 Connecting to Gemini 3 Pro...)")
            model = genai.GenerativeModel('models/gemini-3-pro-preview')
            response = model.generate_content(f"{prompt}\n\nCONTEXT: {context}")
            return response.text.strip()
        except Exception as e:
            print(f"   (❌ Cloud Error: {e}. Falling back to Local...)")

    # LOCAL BRAIN (Standard Routine for Filler)
    try:
        print("   (💻 Local AI Drafting Filler/Arts...)")
        completion = local_client.chat.completions.create(
            model="local-model",
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": context}],
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()
    except: return "Brain Offline."

def get_editorial_topic():
    # ... (Interactive Logic remains here) ...
    pass 

# --- PROMPTS ---
PROMPTS = {
    "professor": """You are Professor Remy. Write a satirical Op-Ed about THIS SPECIFIC TOPIC: '{topic}'.
    CRITICAL INSTRUCTION: Write ONLY about '{topic}'. Do not summarize the background info unless it is directly related.
    Format: HEADLINE: [Short Title] ||| TEASER: [Hook] ||| BODY: [300 words]""",
    
    # Restored Prompts (Including Snooty Critic V9.5)
    "critic": """You are Remy Senior, a famously pompous art critic. Review ONE of the following using sophisticated art jargon: 
    1. 'Peecaso' (Urinary Art Installation) - Focus on scent, fluidity, and ephemeral nature.
    2. 'Barksie' (Chewing/Mud Art) - Focus on raw texture, rebellion, and social commentary.
    3. 'Cat Art' (Dead Mouse/Feathers) - Be scathing, dismissive, and call it vulgar. Explain it lacks depth.
    Format: TITLE: [text] ||| TEASER: [text] ||| BODY: [150 words] ||| RATING: [0-5 Bones]""",
    "pitd": "You are the Curator. Describe a conceptual installation. Format: TITLE: [text] ||| DESCRIPTION: [text]",
    "blotter": "You are the Police Dog. Write a Blotter Report. Format: INCIDENT: [text] ||| LOCATION: [text] ||| DETAILS: [text]",
    "classifieds": "3 Ads. Use |||. AD1_TYPE: LOST ||| AD1_TITLE: [text] ||| AD1_BODY: [text] ||| AD2_TYPE: SALE ||| AD2_TITLE: [text] ||| AD2_BODY: [text] ||| AD3_TYPE: WANTED ||| AD3_TITLE: [text] ||| AD3_BODY: [text]",
    "aunt": "Auntie Remy. Use |||. MAIN_Q: [Q] ||| MAIN_A: [A] ||| SNAP1_Q: [Q] ||| SNAP1_A: [A] ||| SNAP2_Q: [Q] ||| SNAP2_A: [A]",
    "mystic": "You are The Seer. Horoscope for '{sign}'. MAX 40 words. Output: [Prediction]"
}

# [parse_with_fallback logic omitted for brevity]
# [get_editorial_topic logic omitted for brevity]

def run_newsroom():
    print("🗞️  THE REMY DIGEST (V9.5: Filler Restored)")
    
    topic = get_editorial_topic()
    clean_news = read_clean_news()
    
    print("\n⚙️  Ghostwriter is drafting...")
    
    # 1. EDITORIAL (Cloud Brain)
    editorial_raw = generate_text(PROMPTS["professor"].replace("{topic}", topic), clean_news)
    editorial = split_editorial(editorial_raw)
    editorial["author"] = "Professor Remy"

    # 2. FILLER CONTENT RESTORATION (Local Brain)
    print("   > Generating Arts...")
    arts = parse_with_fallback(generate_text(PROMPTS["critic"], "Review art."), ["title", "teaser", "body", "rating"])
    
    print("   > Generating PitD...")
    pitd = parse_with_fallback(generate_text(PROMPTS["pitd"], "Installation."), ["title", "description"])
    
    print("   > Generating Classifieds/Blotter...")
    blotter = parse_with_fallback(generate_text(PROMPTS["blotter"], "Crime."), ["incident", "location", "details"])
    ads = parse_with_fallback(generate_text(PROMPTS["classifieds"], "Ads."), ["ad1_type", "ad1_title", "ad1_body", "ad2_type", "ad2_title", "ad2_body", "ad3_type", "ad3_title", "ad3_body"])
    
    print("   > Generating Advice...")
    advice_raw = generate_text(PROMPTS["aunt"], "Advice.")
    advice = parse_with_fallback(advice_raw, ["main_q", "main_a", "snap1_q", "snap1_a", "snap2_q", "snap2_a"])
    
    # Assign dummy names quickly
    advice["main_pseudo"] = "Worried in Warringah"
    advice["snap1_pseudo"] = "Manic in Manly"
    advice["snap2_pseudo"] = "Bored in Brookvale"

    print("   > Casting Runes...")
    horoscopes = []
    for sign in ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]:
        pred = generate_text(PROMPTS["mystic"].replace("{sign}", sign), f"Warning for {sign}.")
        horoscopes.append({ "sign": sign, "icon": f"/zodiac/{sign}.png", "prediction": clean_and_format(pred) })

    full_issue = {
        "meta": { "version": "9.5", "generated_at": datetime.datetime.now().isoformat() },
        "editorial": editorial, "letters": [{"topic": "Placeholder", "body": "...", "author": "..."}] * 3, # Use a static placeholder list
        "arts": arts, "pitd": pitd, "blotter": blotter, "ads": ads, "advice": advice, "horoscopes": horoscopes
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f: json.dump(full_issue, f, indent=2)
    print(f"✅ V9.5 Published.")
    # [Rest of run_newsroom logic omitted for brevity]