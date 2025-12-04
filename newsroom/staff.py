import os
import json
import random
import google.generativeai as genai
# Import necessary types for safety settings
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- CONFIGURATION & AUTH ---
# Load the keys from the secure local file
KEY_FILE = os.path.join(os.path.dirname(__file__), "keys.json")
GOOGLE_API_KEY = None

try:
    with open(KEY_FILE, "r") as f:
        secrets = json.load(f)
        GOOGLE_API_KEY = secrets.get("gemini")
except Exception:
    pass 

# Configure Gemini
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    # UPDATED MODEL TO 2.5-FLASH AND CORRECTED SAFETY SETTINGS SYNTAX
    MODEL = genai.GenerativeModel(
        'gemini-2.5-flash',
        # Correctly passing structured safety settings to avoid ValueError crash
        safety_settings=[
            {
                "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
                "threshold": HarmBlockThreshold.BLOCK_NONE, # Allowing more freedom for satirical tone
            },
            {
                "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                "threshold": HarmBlockThreshold.BLOCK_ONLY_HIGH,
            },
            {
                "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
        ]
    )
else:
    MODEL = None

# --- ASSET MANAGER (NEW) ---
class AssetManager:
    ASSET_FILE = os.path.join(os.path.dirname(__file__), "assets.json")
    IMAGE_URLS = []

    @classmethod
    def load_assets(cls):
        try:
            with open(cls.ASSET_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # User's list is flat array, which is correct for random selection
                cls.IMAGE_URLS = data.get("general_images", [])
        except Exception as e:
            # Note: This will not crash the script, it just means images will use the fallback URL
            cls.IMAGE_URLS = [] 

    @classmethod
    def get_random_image_url(cls):
        if not cls.IMAGE_URLS:
            # Fallback to a placeholder if list is empty
            return "https://storage.googleapis.com/remys-digest-public-assets/static/Professor%20Dachshund%20Desk%20Scene.jpg"
        return random.choice(cls.IMAGE_URLS)

# Load assets on import
AssetManager.load_assets()

# --- BASE WRITER CLASS ---
class Writer:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def generate_text(self, prompt, context=""):
        if not MODEL:
            return f"\n<div class='text-center my-4 font-bold text-red-600'>[{self.name} is on strike due to missing API Key or failed model configuration]</div>\n"
        
        full_prompt = f"""
        You are {self.name}, the {self.role} for 'The Remy Digest', a satirical broadsheet.
        TONE: Old-school newspaper, cynical, witty, slightly unhinged.
        CONTEXT: {context}
        TASK: {prompt}
        """
        try:
            response = MODEL.generate_content(full_prompt)
            # Use Asset Manager to inject a random cloud image into the text block for visual break
            text_with_asset = embed_random_asset_in_text(response.text, AssetManager)
            return text_with_asset
        except Exception as e:
            # Catch 403/400 errors and be specific
            return f"[Error generating content: {e}]"

# --- SPECIALIZED WRITERS ---

class Puddles(Writer):
    # Full Lead Story (always on index.html)
    def write_full_lead(self, fight_data, rival_foil="The Cronulla Beige"):
        # [Implementation details omitted for brevity, assumes full prompt logic from previous turn]
        prompt = f"""
        Write the LEAD STORY (Headline + 250 words) for the front page.
        The topic is the philosophical fight between {fight_data.get('blue_team', 'Unknown')} and {fight_data.get('red_team', 'Unknown')}.
        MANDATORY: Make a snide reference to our boring rival newspaper, '{rival_foil}', implied to be run by a secret dachshund named Trevor.
        """
        content = self.generate_text(prompt)
        return f"""<div class="lead-story"><h2>{content}</h2></div>"""

    def write_soliloquy(self, image_filename):
        topic_hint = image_filename.replace("soliloquy_", "").replace(".jpg", "")
        prompt = f"Write a short, melancholic Shakespearean soliloquy (100 words) from the sad clown Puddles reflecting on the alternate political history of: {topic_hint}."
        content = self.generate_text(prompt)
        return f"""
        <div class="soliloquy-container my-8 text-center">
            <img src="images/{image_filename}" class="mx-auto h-64 border-4 border-double border-black mb-4">
            <div class="font-serif italic text-lg text-stone-700 max-w-lg mx-auto">"{content}"</div>
        </div>
        """
    # Placeholder for write_teaser (as full lead is on index)
    def write_teaser(self, link_to):
        return ""


class ArthurPumble(Writer):
    # Full Letters Column (Goes to backpage.html)
    def write_full_letters(self, saga_data, council_rules):
        # [Implementation details omitted]
        prompt = f"Write the full 'LETTERS TO THE EDITOR' column (The Spit Gripes), including a letter from 'Outraged of Cromer' and a passive-aggressive reply from his neighbor."
        content = self.generate_text(prompt)
        return f"""<div class="letters-section backpage-gossip">{content}</div>"""

    # Teaser for Letters (Goes to index.html)
    def write_teaser(self, link_to):
        content = self.generate_text(f"Write a 50-word teaser preview for the 'Letters' column. The tone should be angry and mention a bin dispute.")
        return f"""
        <div class="teaser-box my-4 p-3 border border-stone-300">
            <h4 class='font-bold uppercase text-stone-700'>The Spit Gripes</h4>
            <p class='text-sm italic'>{content}</p>
            <a href="{link_to}" class="text-red-600 font-bold text-xs mt-1 block">[READ FULL MELTDOWN]</a>
        </div>
        """

class Cornelius(Writer):
    # Full Arts Review (Goes to arts.html)
    def write_full_arts(self, saga_data):
        # [Implementation details omitted]
        prompt = f"Write the full ARTS REVIEW column. You are Cornelius the Ibis. Review a simulated, boring headline from 'The Cronulla Leader' (invent one). Critique its banality as 'Minimalist Nihilism'."
        content = self.generate_text(prompt)
        return f"""<div class="arts-section lounge-academic">{content}</div>"""

    # Teaser for Arts (Goes to index.html)
    def write_teaser(self, link_to):
        content = self.generate_text(f"Write a 50-word teaser preview for the 'Arts' column. Tone should be high-brow and mention Ibis reviewing garbage.")
        return f"""
        <div class="teaser-box my-4 p-3 border border-stone-300">
            <h4 class='font-bold uppercase text-stone-700'>The Lounge: Arts</h4>
            <p class='text-sm italic'>{content}</p>
            <a href="{link_to}" class="text-red-600 font-bold text-xs mt-1 block">[VIEW THE INSTALLATION]</a>
        </div>
        """

class ZoomiesKid(Writer):
    def write_full_rant(self, saga_data):
        prompt = f"Write a short, angry rant (150 words) from a 'Youth on an E-Bike'. Complain about the local dispute blocking the footpath. Use Australian slang (Eshays, Brah, etc)."
        content = self.generate_text(prompt)
        return f"""<div class="zoomies-section spray-bulletin"><h2>Zoomies: Local Menace</h2>{content}</div>"""
    
    def write_teaser(self, link_to):
        content = self.generate_text(f"Write a 50-word teaser preview for the 'Zoomies' column. The tone should be angry and mention E-bikes/curb blocking.")
        return f"""
        <div class="teaser-box my-4 p-3 border border-stone-300">
            <h4 class='font-bold uppercase text-stone-700'>Zoomies/E-Bike Rant</h4>
            <p class='text-sm italic'>{content}</p>
            <a href="{link_to}" class="text-red-600 font-bold text-xs mt-1 block">[READ THE RANT]</a>
        </div>
        """

class MadameFifi(Writer):
    def write_full_seance(self):
        prompt = f"Write the full SEANCE column. You are Madame Fifi (Standard Poodle). Channel the spirit of a Famous Historical Pet (e.g., Blondie, Laika). Write a short (100 word) monologue from the pet's perspective. Tone: Douglas Adams. Focus on smells/food, ignore historical gravity."
        content = self.generate_text(prompt)
        return f"""
        <div class="seance-section backpage-gossip">
            <h2>The Seance: Madame Fifi Channels the Dead</h2>
            {content}
        </div>
        """
    
    def write_teaser(self, link_to):
        content = self.generate_text(f"Write a 50-word teaser preview for 'The Seance'. The tone should be mystical and mention a famous dog or horse.")
        return f"""
        <div class="teaser-box my-4 p-3 border border-stone-300">
            <h4 class='font-bold uppercase text-stone-700'>The Seance (Mystic)</h4>
            <p class='text-sm italic'>{content}</p>
            <a href="{link_to}" class="text-red-600 font-bold text-xs mt-1 block">[SEE WHO IS SPEAKING]</a>
        </div>
        """


# --- UTILITY / IMAGE EMBEDDERS (No AI needed) ---
def embed_image_section(filename, title, caption_text=""):
    # Checks for the local image files (PITD/Roast)
    path = os.path.join("images", filename) 
    
    if os.path.exists(path):
        return f"""
        <div class="image-embed my-8 border-t-2 border-b-2 border-black py-4">
            <h3 class="font-sans font-black uppercase text-center mb-2">{title}</h3>
            <img src="images/{filename}" class="w-full h-auto mx-auto shadow-lg">
            <p class="text-center italic mt-2 text-sm text-stone-600">{caption_text}</p>
        </div>
        """
    return "" 

def embed_random_asset_in_text(html_content, asset_manager):
    """Inserts a random cloud asset into a text block after the first paragraph."""
    if not asset_manager.IMAGE_URLS:
        return html_content 

    random_url = asset_manager.get_random_image_url()
    
    # Check for valid URL before embedding
    if not random_url.startswith("http"):
         return html_content
         
    img_html = f'<img src="{random_url}" class="float-right w-40 h-auto ml-4 border border-black shadow-md sepia-[.4] contrast-150">'
    
    # Simple insertion logic: insert after the first paragraph
    parts = html_content.split('</p>', 1)
    if len(parts) > 1:
        return parts[0] + img_html + '</p>' + parts[1]
    return html_content

# --- Additional classes (Horoscope, etc.) would be defined here ---


# --- Final Utility for Assembly ---

# Attach the main content function logic to the base class
# (This allows assemble.py to call writer.generate_text directly)
Writer.embed_random_asset_in_text = staticmethod(embed_random_asset_in_text)

# The rest of the classes (Horoscope, etc.) would be defined here
# using the new write_full_ and write_teaser methods.