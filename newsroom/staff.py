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
            return f"[{self.name} is on strike due to missing API Key]"
        
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
    def write_lead(self, fight_data, rival_foil="The Cronulla Beige"):
        status = fight_data.get("status", "BUILD_UP")
        topic = fight_data.get("topic", "Everything")
        blue = fight_data.get("blue_team", "Unknown")
        red = fight_data.get("red_team", "Unknown")

        prompt = f"""
        Write the LEAD STORY (Headline + 250 words).
        The current status of the weekly philosophical fight is: {status}.
        The topic is: {topic}.
        The Blue Team is: {blue}. The Red Team is: {red}.
        
        If status is BUILD_UP: Hype the upcoming match. Quote the fighters trash-talking.
        If status is MAIN_EVENT: Describe the carnage.
        
        MANDATORY: Make a snide reference to our boring rival newspaper, '{rival_foil}', implied to be run by a coward named Trevor.
        """
        content = self.generate_text(prompt)
        # Wrap in HTML
        return f"""
        <div class="lead-story">
            {content}
        </div>
        """

    def write_soliloquy(self, image_filename):
        # Infer topic from filename (e.g., soliloquy_onion.jpg -> Onion)
        topic_hint = image_filename.replace("soliloquy_", "").replace(".jpg", "")
        
        prompt = f"""
        Write a short, melancholic Shakespearean soliloquy (100 words).
        You are holding an object related to: {topic_hint}.
        Reflect on how this object changed history (or could have).
        """
        content = self.generate_text(prompt)
        return f"""
        <div class="soliloquy-container">
            <img src="images/{image_filename}" class="w-full border-4 border-double border-black mb-4">
            <div class="font-serif italic text-lg text-center">"{content}"</div>
        </div>
        """

class ArthurPumble(Writer):
    def write_letters_column(self, saga_data, council_rules):
        incident = saga_data.get("incident", "Nothing")
        details = saga_data.get("details", "Silence")
        
        prompt = f"""
        Write the 'LETTERS TO THE EDITOR' column.
        
        LETTER 1: From 'Outraged of Cromer' (Arthur).
        He is complaining about: {incident} ({details}).
        He must reference specific Council Bin Rules: {council_rules}.
        He is projecting his own guilt onto his neighbor.
        
        LETTER 2: A reply from 'The Neighbor at #42'.
        Polite but passive-aggressive, exposing Arthur's hypocrisy.
        """
        content = self.generate_text(prompt)
        return f"""
        <div class="letters-section">
            <h3 class="font-serif font-bold uppercase text-xl border-b border-black mb-2">The Spit Gripes</h3>
            {content}
        </div>
        """

class Cornelius(Writer):
    def write_arts(self, saga_data):
        item_of_dispute = saga_data.get("details", "rubbish")
        
        prompt = f"""
        Write an ARTS REVIEW.
        You are Cornelius the Ibis. You review trash as if it were high art.
        Today's subject: The {item_of_dispute} involved in the local neighborhood dispute.
        
        ALSO: Review a headline from 'The Cronulla Leader' (invent a boring one like 'Fence Painted Grey').
        Call it a masterpiece of minimalism.
        """
        content = self.generate_text(prompt)
        return f"""
        <div class="arts-section">
            <h3 class="font-serif font-bold uppercase text-xl border-b border-black mb-2">The Lounge (Arts)</h3>
            {content}
        </div>
        """

class ZoomiesKid(Writer):
    def write_rant(self, saga_data):
        prompt = f"""
        Write a short, angry rant from a 'Youth on an E-Bike'.
        Complain about the local dispute ({saga_data.get('details')}) blocking the footpath.
        Use slang (Eshays, Brah, etc).
        """
        content = self.generate_text(prompt)
        return f"""
        <div class="zoomies-section border-l-4 border-red-600 pl-4 my-4">
            <h4 class="font-sans font-black uppercase text-red-600">MENACE WATCH</h4>
            {content}
        </div>
        """

class MadameFifi(Writer):
    def write_seance(self):
        prompt = f"""
        You are Madame Fifi (Standard Poodle).
        Channel the spirit of a Famous Historical Pet (e.g., Blondi, Checkers, Laika).
        Write a 50-word message from them. Tone: Douglas Adams. Focus on smells/food, ignore historical gravity.
        """
        content = self.generate_text(prompt)
        return f"""
        <div class="seance-section bg-stone-200 p-4 mt-4">
            <h4 class="font-gothic text-xl">The Seance</h4>
            {content}
        </div>
        """

# --- ASSET EMBEDDERS (No AI needed) ---
def embed_image_section(filename, title, caption_text=""):
    path = os.path.join("images", filename)
    # Check relative to where the script is RUN (root)
    if os.path.exists(path):
        return f"""
        <div class="image-embed my-8 border-t-2 border-b-2 border-black py-4">
            <h3 class="font-sans font-black uppercase text-2xl text-center mb-2">{title}</h3>
            <img src="images/{filename}" class="w-full h-auto mx-auto shadow-lg">
            <p class="text-center italic mt-2 text-sm">{caption_text}</p>
        </div>
        """
    return ""  # Return empty if file missing