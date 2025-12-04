import os
import json
import google.generativeai as genai
import random

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')

def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# --- THE WRITERS ---

class PuddlesLead:
    """The Editor. Writes the main story."""
    def write(self):
        card = load_json("fight_card.json")
        prompt = f"""
        Write a 250-word lead article for 'The Remyverse'.
        Topic: The upcoming debate rumble between {card['blue_team']} vs {card['red_team']}.
        Subject: {card['topic']}.
        Tone: Reserved, intellectual, matter-of-fact, yet subtly hyping the violence of the debate.
        
        CRITICAL REQUIREMENT:
        You must reference our rival newspaper, 'The Cronulla Beige', which is boring and irrelevant. 
        Contrast our exciting intellectual rumble with their headline about "Fence Painted Grey".
        
        Format: HTML <article> with <h2> and <p> tags.
        """
        return generate_text(prompt)

class ComicPITD:
    """The Visual Gag."""
    def write(self):
        return """
        <article class="pitd">
            <h2>Picture in the Dirt</h2>
            <img src="../content/images/pitd_current.jpg" alt="Fig 1: The Inevitable Stalemate" style="width:100%; border:2px solid #000;">
            <p class="caption">Fig 1: The inevitable philosophical stalemate.</p>
        </article>
        """

class RoastMaster:
    """The Burn."""
    def write(self):
        return """
        <article class="roast">
            <h2>Remy Roasts History</h2>
            <img src="../content/images/roast_current.jpg" alt="Remy judging history" style="width:100%; border:2px solid #d32f2f;">
            <p>He has seen your timeline, and he is not impressed.</p>
        </article>
        """

class SoliloquySoul:
    """The Melancholic Poet."""
    def write(self):
        # Check for image (Mocking existence for logic)
        img_name = "soliloquy_onion.jpg" # Default mock
        subject = "A Raw Onion"
        
        prompt = f"""
        Write a 100-word Shakespearean soliloquy for a Dachshund named Puddles.
        Subject: Contemplating {subject} (based on image {img_name}).
        Tone: Melancholic, tragic, overly dramatic about a vegetable.
        Format: HTML <i> tags for the poem.
        """
        return f"<article class='soliloquy'><h2>The Soliloquy</h2>{generate_text(prompt)}</article>"

class LettersSpit:
    """The Community Outrage."""
    def write(self):
        saga = load_json("saga.json")
        rules = load_json("council_rules.json")
        
        prompt = f"""
        Write two 'Letters to the Editor'.
        1. From Arthur Pumble ('Outraged of Cromer'). He denies the "{saga['incident']}" regarding the {saga['details']}. He cites {rules['bin_night']} confusion.
        2. A reply from The Neighbor (Mrs. Higgins). She has the {saga['evidence']}.
        Tone: Petty, passive-aggressive, high-stakes council drama.
        Format: HTML <div class='letter'>...</div>.
        """
        return f"<article class='letters'><h2>Letters to the Editor</h2>{generate_text(prompt)}</article>"

class SprayPolice:
    """The Police Blotter."""
    def write(self):
        saga = load_json("saga.json")
        prompt = f"""
        Write a dry, bureaucratic NSW Police Force media release snippet.
        Incident: {saga['incident']} at {saga['location']}.
        Details: {saga['details']}.
        Tone: Extremely dry, official, boring police jargon.
        Format: HTML <div class='police-report'>...</div>
        """
        return f"<article class='spray'><h2>The Daily Spray</h2>{generate_text(prompt)}</article>"

class ArtsCornelius:
    """The Critic."""
    def write(self):
        prompt = f"""
        You are Cornelius, the arts critic. 
        Task: Review the latest issue of our rival paper, 'The Cronulla Beige'.
        Their Headline: "Local Man Considers Buying A Hat".
        Your Review: Praise it as "High Art Minimalism." Use pretentious art-school jargon to describe how boring it is.
        Tone: Snobbish, reserved, intellectual.
        Format: HTML <article>...
        """
        return f"<article class='arts'><h2>The Lounge (Arts)</h2>{generate_text(prompt)}</article>"

class ZoomiesMenace:
    """The Youth Voice."""
    def write(self):
        saga = load_json("saga.json")
        prompt = f"""
        Write a short, chaotic paragraph from the perspective of a hyperactive puppy (The Zoomies Reporter).
        Topic: The pile of rubbish at {saga['location']}.
        Tone: Chaotic, all caps, distracted by smells, fast.
        Format: HTML <p>...
        """
        return f"<article class='zoomies'><h2>ZOOMIES REPORT</h2>{generate_text(prompt)}</article>"

class MysticFifi:
    """The Seance."""
    def write(self):
        prompt = "Channel the spirit of a historical pet (e.g., Napoleon's Pug) and give one piece of cryptic advice."
        return f"<article class='mystic'><h2>Madame Fifi's Seance</h2>{generate_text(prompt)}</article>"

# --- HELPER ---
def generate_text(prompt):
    if not GEMINI_API_KEY:
        return "<p>[API Key Missing - Writer on Strike]</p>"
    try:
        response = model.generate_content(prompt)
        # Strip markdown code blocks if present
        clean = response.text.replace("```html", "").replace("```", "")
        return clean
    except Exception as e:
        return f"<p>[Writer Blocked: {e}]</p>"