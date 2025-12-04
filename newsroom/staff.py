import os
import json
import google.generativeai as genai
import random

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # UPDATED MODEL: Using gemini-2.5-flash
    model = genai.GenerativeModel('gemini-2.5-flash')

def load_json(filepath):
    try:
        # Load from root directory
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

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

# --- THE WRITERS ---

class PuddlesLead:
    """The Editor. Writes the main story."""
    def write_full_column(self):
        card = load_json("fight_card.json")
        prompt = f"""
        Write a 300-word lead article for 'The Remyverse'.
        Topic: The upcoming debate rumble between {card['blue_team']} vs {card['red_team']}.
        Subject: {card['topic']}.
        Tone: Reserved, intellectual, matter-of-fact, yet subtly hyping the violence of the debate.
        
        CRITICAL REQUIREMENT:
        You must reference our rival newspaper, 'The Cronulla Beige', which is boring and irrelevant. 
        Contrast our exciting intellectual rumble with their headline about "Fence Painted Grey".
        
        Format: HTML <article> with <h2> and <p> tags.
        """
        return generate_text(prompt)

    def write_teaser(self, link_to):
        # The lead story is generally shown in full on the index, but we return a summary structure for consistency
        return self.write_full_column()

class ComicPITD:
    """The Visual Gag."""
    def write_full_column(self):
        # IMAGE PATH FIXED: 'images/'
        return """
        <article class="pitd">
            <h2>Picture in the Dirt (The Inevitable)</h2>
            <img src="images/pitd_current.jpg" alt="Fig 1: The Inevitable Stalemate" style="width:100%; border:2px solid #000;">
            <p class="caption">Fig 1: The inevitable philosophical stalemate. See full analysis on our Back Page.</p>
        </article>
        """

    def write_teaser(self, link_to):
        # Teaser is just the image and a link
        return self.write_full_column()

class RoastMaster:
    """The Burn."""
    def write_full_column(self):
        # IMAGE PATH FIXED: 'images/'
        return """
        <article class="roast">
            <h2>Remy Roasts History (Opinion)</h2>
            <img src="images/roast_current.jpg" alt="Remy judging history" style="width:100%; border:2px solid #d32f2f;">
            <p>He has seen your timeline, and he is not impressed. He requires a stronger narrative arc.</p>
        </article>
        """

    def write_teaser(self, link_to):
        return self.write_full_column()

class SoliloquySoul:
    """The Melancholic Poet."""
    def write_full_column(self):
        # Placeholder logic for image name to set the subject
        img_name = "soliloquy_onion.jpg"
        subject = "A Raw Onion"
        
        prompt = f"""
        Write a 150-word Shakespearean soliloquy for a Dachshund named Puddles.
        Subject: Contemplating {subject} (based on image {img_name}).
        Tone: Melancholic, tragic, overly dramatic about a vegetable.
        Format: HTML <p> wrapping the <i> tags for the poem.
        """
        return f"<article class='soliloquy'><h2>The Soliloquy of Self-Doubt</h2>{generate_text(prompt)}</article>"

    def write_teaser(self, link_to):
        prompt = "Write a 50-word dramatic prologue for a Shakespearean soliloquy about sadness. End with an ellipses."
        teaser_text = generate_text(prompt)
        return f"""
        <article class='soliloquy-teaser'>
            <h2>The Soliloquy...</h2>
            {teaser_text}
            <p><a href="{link_to}">Read the full, tragic column...</a></p>
        </article>
        """

class LettersSpit:
    """The Community Outrage."""
    def write_full_column(self):
        saga = load_json("saga.json")
        rules = load_json("council_rules.json")
        
        prompt = f"""
        Write two detailed 'Letters to the Editor' (200 words total).
        1. From Arthur Pumble ('Outraged of Cromer'). He denies the "{saga['incident']}" regarding the {saga['details']}. He cites {rules['bin_night']} confusion, noting the strict rules for the {rules['bins']['red']} bin.
        2. A reply from The Neighbor (Mrs. Higgins). She exposes Arthur, noting she has the {saga['evidence']}.
        Tone: Petty, passive-aggressive, high-stakes council drama.
        Format: HTML <div class='letter'>...</div>.
        """
        return f"<article class='letters'><h2>Letters to the Editor: The Bulky Goods War</h2>{generate_text(prompt)}</article>"

    def write_teaser(self, link_to):
        prompt = "Write a 50-word teaser introduction for a community mailbag section focused on bin disputes and neighborhood feuds. Mention 'The Phantom Booking' incident."
        teaser_text = generate_text(prompt)
        return f"""
        <article class='letters-teaser'>
            <h2>Back Page Teaser: Spit Gripes</h2>
            {teaser_text}
            <p><a href="{link_to}">Read all the neighborhood complaints and Mrs. Higgins' CCTV evidence.</a></p>
        </article>
        """

class SprayPolice:
    """The Police Blotter."""
    def write_full_column(self):
        saga = load_json("saga.json")
        prompt = f"""
        Write a 150-word dry, bureaucratic NSW Police Force media release snippet.
        Incident: {saga['incident']} at {saga['location']}.
        Details: {saga['details']}. Include a warning about misuse of council resources.
        Tone: Extremely dry, official, boring police jargon.
        Format: HTML <div class='police-report'>...</div>
        """
        return f"<article class='spray'><h2>The Daily Spray: Waste Management Dispute</h2>{generate_text(prompt)}</article>"

    def write_teaser(self, link_to):
        prompt = "Write a 75-word brief, matter-of-fact police blotter summary concerning a local dispute over a large, discarded item. Use police jargon."
        teaser_text = generate_text(prompt)
        return f"""
        <article class='spray-teaser'>
            <h2>Police Blotter Brief</h2>
            {teaser_text}
            <p><a href="{link_to}">Full report on the Waste Dispute...</a></p>
        </article>
        """

class ArtsCornelius:
    """The Critic."""
    def write_full_column(self):
        prompt = f"""
        You are Cornelius, the arts critic. 
        Task: Review the latest issue of our rival paper, 'The Cronulla Beige'.
        Their Headline: "Local Man Considers Buying A Hat".
        Your Review: Write a 200-word review. Praise it as "High Art Minimalism." Use snobbish, pretentious art-school jargon (e.g., 'negative space', 'existential ennui') to describe how incredibly boring and beige it is.
        Format: HTML <article>...</article>
        """
        return f"<article class='arts'><h2>The Lounge (Arts): Review of 'The Beige'</h2>{generate_text(prompt)}</article>"

    def write_teaser(self, link_to):
        prompt = "Write a 50-word pretentious review snippet about a boring piece of art ('The Cronulla Beige'). Use words like 'existential' and 'void'."
        teaser_text = generate_text(prompt)
        return f"""
        <article class='arts-teaser'>
            <h2>Cornelius Reviews...</h2>
            {teaser_text}
            <p><a href="{link_to}">Full review of the art-world void.</a></p>
        </article>
        """

class ZoomiesMenace:
    """The Youth Voice."""
    def write_full_column(self):
        saga = load_json("saga.json")
        prompt = f"""
        Write a 100-word chaotic column from the perspective of a hyperactive puppy (The Zoomies Reporter).
        Topic: The pile of rubbish at {saga['location']}. Focus on how it disrupts the run route and smells weird.
        Tone: Chaotic, all caps, distracted by smells, fast.
        Format: HTML <p> wrapping the chaotic text.
        """
        return f"<article class='zoomies'><h2>ZOOMIES REPORT: My Run Is RUINED!</h2>{generate_text(prompt)}</article>"

    def write_teaser(self, link_to):
        prompt = "Write a 50-word chaotic headline and summary for a youth column about a trash pile blocking a puppy's running path. Use excited, all-caps language."
        teaser_text = generate_text(prompt)
        return f"""
        <article class='zoomies-teaser'>
            <h2>ZOOMIES!</h2>
            {teaser_text}
            <p><a href="{link_to}">Read the full, frantic report.</a></p>
        </article>
        """

class MysticFifi:
    """The Seance."""
    def write_full_column(self):
        prompt = "Channel the spirit of a historical pet (e.g., Douglas Adams style) and write a 100-word passage containing one piece of cryptic advice, mentioning the meaning of life."
        return f"<article class='mystic'><h2>Madame Fifi's Seance: The Meaning of Biscuits</h2>{generate_text(prompt)}</article>"
        
    def write_teaser(self, link_to):
        prompt = "Write a 50-word psychic teaser for a column where a historical pet gives cryptic advice about the future."
        teaser_text = generate_text(prompt)
        return f"""
        <article class='mystic-teaser'>
            <h2>Fifi Speaks!</h2>
            {teaser_text}
            <p><a href="{link_to}">Dare to read the pet's prophecy.</a></p>
        </article>
        """