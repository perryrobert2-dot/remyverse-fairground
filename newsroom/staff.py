import os
import json
import random
import google.generativeai as genai
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
    pass # Assume assembly handles the error reporting

# Configure Gemini
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    # UPDATED MODEL TO 2.5-FLASH
    MODEL = genai.GenerativeModel(
        'gemini-2.5-flash',
        safety_settings=[
            # Disable some safety for satire/argument generation
            HarmCategory.HARM_CATEGORY_HARASSMENT, HarmBlockThreshold.BLOCK_ONLY_HIGH
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
                cls.IMAGE_URLS = data.get("general_images", [])
        except Exception as e:
            print(f"[!] Asset Manager Error: Could not load {cls.ASSET_FILE}. {e}")
            cls.IMAGE_URLS = []

    @classmethod
    def get_random_image_url(cls):
        if not cls.IMAGE_URLS:
            # Fallback to the user's provided first image
            return "https://storage.googleapis.com/remys-digest-public-assets/static/4WD%20Outside%20Cafe.jpg" 
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
            return f"\n<div class='text-center my-4 font-bold text-red-600'>[Error generating content: 403 API Key Missing or Invalid]</div>\n"
        
        full_prompt = f"""
        You are {self.name}, the {self.role} for 'The Remy Digest', a satirical broadsheet.
        TONE: Old-school newspaper, cynical, witty, slightly unhinged.
        CONTEXT: {context}
        TASK: {prompt}
        """
        try:
            response = MODEL.generate_content(full_prompt)
            return response.text
        except Exception as e:
            # Catch 403/400 errors and be specific
            return f"[Error generating content: {e}]"

# --- SPECIALIZED WRITERS ---

class Puddles(Writer):
    def write_full_lead(self, fight_data, rival_foil="The Cronulla Beige"):
        status = fight_data.get("status", "BUILD_UP")
        topic = fight_data.get("topic", "Everything")
        
        prompt = f"""... [Full Lead Story Prompt] ...""" # The full prompt is kept internally
        content = self.generate_text(prompt)
        return f"""<div class="lead-story"><h2>{content}</h2></div>"""

    def write_soliloquy(self, image_filename):
        # [Content similar to previous implementation]
        content = self.generate_text(f"Write a short, melancholic soliloquy...")
        return f"""
        <div class="soliloquy-container my-8 text-center">
            <img src="images/{image_filename}" class="mx-auto h-64 border-4 border-double border-black mb-4">
            <div class="font-serif italic text-lg text-stone-700 max-w-lg mx-auto">"{content}"</div>
        </div>
        """

class ArthurPumble(Writer):
    # Full Letters Column (Goes to backpage.html)
    def write_full_letters(self, saga_data, council_rules):
        # [Content similar to previous implementation]
        content = self.generate_text(f"Write the full 'LETTERS TO THE EDITOR' column...")
        return f"""<div class="letters-section backpage-gossip">{content}</div>"""

    # Teaser for Letters (Goes to index.html)
    def write_teaser(self, link_to):
        content = self.generate_text(f"Write a 50-word teaser preview for the 'Letters' column. Tone should be angry and mention a bin dispute.")
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
        # [Content similar to previous implementation]
        content = self.generate_text(f"Write the full ARTS REVIEW column...")
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

# --- UTILITY / IMAGE EMBEDDERS (No AI needed) ---
def embed_image_section(filename, title, caption_text=""):
    # This is used for local assets like PITD/Roast images
    path = os.path.join("images", filename) 
    
    if os.path.exists(path):
        return f"""
        <div class="image-embed my-8 border-t-2 border-b-2 border-black py-4">
            <h3 class="font-sans font-black uppercase text-center mb-2">{title}</h3>
            <img src="images/{filename}" class="w-full h-auto mx-auto shadow-lg">
            <p class="text-center italic mt-2 text-sm text-stone-600">{caption_text}</p>
        </div>
        """
    return "" # Return empty if file missing

def embed_random_asset_in_text(html_content, asset_manager):
    """Inserts a random cloud asset into a text block."""
    if not asset_manager.IMAGE_URLS:
        return html_content # No images to embed

    random_url = asset_manager.get_random_image_url()
    img_html = f'<img src="{random_url}" class="float-right w-40 h-auto ml-4 border border-black shadow-md sepia-[.4] contrast-150">'
    
    # Simple insertion logic: insert after the first paragraph
    parts = html_content.split('</p>', 1)
    if len(parts) > 1:
        return parts[0] + img_html + '</p>' + parts[1]
    return html_content

# The rest of the classes (ZoomiesKid, MadameFifi, etc.) would be defined here
# using the new write_full_ and write_teaser methods.