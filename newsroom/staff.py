import os
import json
import random
import google.generativeai as genai

# --- CONFIGURATION & AUTH ---
# Load the keys from the secure local file
KEY_FILE = os.path.join(os.path.dirname(__file__), "keys.json")
GOOGLE_API_KEY = None

try:
    with open(KEY_FILE, "r") as f:
        secrets = json.load(f)
        GOOGLE_API_KEY = secrets.get("gemini")
except FileNotFoundError:
    print(f"[!] CRITICAL: Key file missing at {KEY_FILE}")
except Exception as e:
    print(f"[!] Error loading keys: {e}")

# Configure Gemini
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    MODEL = genai.GenerativeModel('gemini-2.5-flash')
else:
    MODEL = None
    print("[!] Writers are on strike (No Gemini Key found).")

# --- BASE WRITER CLASS ---
class Writer:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def generate_text(self, prompt, context=""):
        if not MODEL:
            # If API key fails, return the fallback message
            return f"\n<div class='text-center my-4 font-bold text-red-600'>[{self.name} is on strike due to missing API Key]</div>\n"
        
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
            return f"[Error generating content: {e}]"

# --- SPECIALIZED WRITERS ---

class Puddles(Writer):
    # Full Lead Story (always on index.html)
    def write_full_lead(self, fight_data, rival_foil="The Cronulla Beige"):
        status = fight_data.get("status", "BUILD_UP")
        topic = fight_data.get("topic", "Everything")
        blue = fight_data.get("blue_team", "Unknown")
        red = fight_data.get("red_team", "Unknown")

        prompt = f"""
        Write the LEAD STORY (Headline + 250 words) for the front page.
        The current status of the weekly philosophical fight is: {status}.
        The topic is: {topic}. The Blue Team is: {blue}. The Red Team is: {red}.
        
        If status is BUILD_UP: Hype the upcoming match. Quote the fighters trash-talking.
        MANDATORY: Make a snide reference to our boring rival newspaper, '{rival_foil}', implied to be run by a secret dachshund named Trevor.
        """
        content = self.generate_text(prompt)
        # Wrap in HTML
        return f"""
        <div class="lead-story">
            <h2>{content}</h2>
        </div>
        """

    # Puddles Soliloquy (Image/Text)
    def write_soliloquy(self, image_filename):
        topic_hint = image_filename.replace("soliloquy_", "").replace(".jpg", "")
        
        prompt = f"""
        Write a short, melancholic Shakespearean soliloquy (100 words).
        You are Puddles, a sad clown, reflecting on the alternate political history of: {topic_hint}.
        """
        content = self.generate_text(prompt)
        return f"""
        <div class="soliloquy-container my-8 text-center">
            <img src="images/{image_filename}" class="mx-auto h-64 border-4 border-double border-black mb-4">
            <div class="font-serif italic text-lg text-stone-700 max-w-lg mx-auto">"{content}"</div>
        </div>
        """

class ArthurPumble(Writer):
    # Full Letters Column (Goes to backpage.html)
    def write_full_letters(self, saga_data, council_rules):
        incident = saga_data.get("incident", "Nothing")
        details = saga_data.get("details", "Silence")
        
        prompt = f"""
        Write the entire 'LETTERS TO THE EDITOR' column (The Spit Gripes).
        
        LETTER 1: From 'Outraged of Cromer' (Arthur). He complains about: {incident} ({details}). He must reference specific Council Bin Rules: {council_rules}. He is projecting his own guilt onto his neighbor.
        LETTER 2: A passive-aggressive reply from 'The Neighbor at #42', exposing Arthur's hypocrisy and referencing the stolen booking slot.
        """
        content = self.generate_text(prompt)
        return f"""
        <div class="letters-section">
            <h2>The Spit Gripes (Letters to the Editor)</h2>
            {content}
        </div>
        """

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
        item_of_dispute = saga_data.get("incident", "rubbish")
        
        prompt = f"""
        Write the full ARTS REVIEW column. You are Cornelius the Ibis. You review trash as if it were high art.
        Review the {item_of_dispute} involved in the local neighborhood dispute as an installation piece.
        ALSO: Review a simulated, boring headline from 'The Cronulla Leader' (invent a boring one). Critique its banality as 'Minimalist Nihilism'.
        """
        content = self.generate_text(prompt)
        return f"""
        <div class="arts-section">
            <h2>The Lounge (Arts & Critique)</h2>
            {content}
        </div>
        """

    # Teaser for Arts (Goes to index.html)
    def write_teaser(self, link_to):
        content = self.generate_text(f"Write a 50-word teaser preview for the 'Arts' column. The tone should be high-brow and mention Ibis reviewing garbage.")
        return f"""
        <div class="teaser-box my-4 p-3 border border-stone-300">
            <h4 class='font-bold uppercase text-stone-700'>The Lounge: Arts</h4>
            <p class='text-sm italic'>{content}</p>
            <a href="{link_to}" class="text-red-600 font-bold text-xs mt-1 block">[VIEW THE INSTALLATION]</a>
        </div>
        """

class ZoomiesKid(Writer):
    # Rant (Goes to a Subpage for now, but will be merged later)
    def write_rant(self, saga_data):
        prompt = f"""
        Write a short, angry rant (150 words) from a 'Youth on an E-Bike'.
        Complain about the local dispute blocking the footpath. Use slang (Eshays, Brah, etc).
        """
        content = self.generate_text(prompt)
        return f"""
        <div class="zoomies-section">
            <h2>Zoomies: Local Menace</h2>
            {content}
        </div>
        """
    
    # Teaser for Zoomies
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
        prompt = f"""
        Write the full SEANCE column. You are Madame Fifi (Standard Poodle).
        Channel the spirit of a Famous Historical Pet (e.g., Blondie, Laika, Bucephalus).
        Write a short (100 word) monologue from the pet's perspective. Tone: Douglas Adams. Focus on smells/food, ignore historical gravity.
        """
        content = self.generate_text(prompt)
        return f"""
        <div class="seance-section">
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

class Horoscope(Writer):
    def write_full_horoscope(self):
        # Placeholder
        return "Horoscope Placeholder"

# --- ASSET EMBEDDERS (No AI needed) ---
def embed_image_section(filename, title, caption_text=""):
    path = os.path.join("images", filename) # Corrected path
    
    # Check relative to where the script is RUN (root)
    if os.path.exists(path):
        return f"""
        <div class="image-embed my-8 border-t-2 border-b-2 border-black py-4">
            <h3 class="font-sans font-black uppercase text-center mb-2">{title}</h3>
            <img src="images/{filename}" class="w-full h-auto mx-auto shadow-lg">
            <p class="text-center italic mt-2 text-sm text-stone-600">{caption_text}</p>
        </div>
        """
    return "" # Return empty if file missing