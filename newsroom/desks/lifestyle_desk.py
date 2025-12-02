# newsroom/desks/lifestyle_desk.py
from .. import brain
from ..personas import character_sheets
from .. import config
import random
from datetime import datetime

def get_real_estate():
    """
    Generates the 'Property Listing' for the Cat Agent.
    """
    agent = character_sheets.CAT_AGENT
    listing = random.choice(["A cardboard box", "A sun-drenched studio", "A waterfront tap"])
    
    prompt = f"You are {agent['name']}. Write a luxury listing for: {listing}. Max 80 words. No markdown."
    text = brain.think(prompt, model_type="flash").replace("**", "")
    
    image_file = config.get_visual_filename(text, 'real estate')

    return {
        "id": f"life-listing-{datetime.now().strftime('%Y%m%d')}",
        "title": f"Just Listed: {listing}",
        "headline": f"Just Listed: {listing}", 
        "author": agent['name'],
        "body": text,
        "content": text,
        "tag": "Real Estate",
        "category": "Lifestyle",
        "image": f"/stock/{image_file}",
        "secondary_image": "/personas/cat_agent.jpg", 
        "timestamp": datetime.now().isoformat()
    }

def get_deep_dive():
    """
    Generates a 'Deep Dive' interesting fact.
    Uses remote Google Cloud assets for The Librarian.
    """
    # 1. GET CURRENT DAY (monday, tuesday, etc.)
    current_day = datetime.now().strftime('%A').lower()
    
    # 2. CONSTRUCT REMOTE URL
    image_path = f"https://storage.googleapis.com/remys-digest-public-assets/deep-dive/{current_day}_librarian.png"
    
    persona = "The Librarian"
    print(f"📂 Lifestyle Desk: {persona} is accessing the cloud archives for {current_day}...")

    # 3. GENERATE CONTENT
    # We want obscure, fascinating facts (The Cosmic Receipt, etc.)
    topic_prompt = random.choice([
        "an obscure archaeological discovery",
        "a lost manuscript or ancient text",
        "a strange statistical anomaly in history",
        "a forgotten astronomical event"
    ])

    prompt = f"""
    You are {persona}.
    Tone: Intellectual, fascinating, slightly academic but accessible.
    
    Write a short 'Remarkable Find' column (approx 100 words) about: {topic_prompt}.
    
    GUIDELINES:
    1. Title format: 'Remarkable Find: [Topic Name]'
    2. Start with 'Did you know...' or a hook.
    3. Be factual but engaging (like a museum plaque).
    4. Do NOT use markdown bolding (**).
    """
    
    text = brain.think(prompt, model_type="pro").replace("**", "")
    
    # Extract title if possible
    title = f"Deep Dive: {persona}"
    if ":" in text.split('\n')[0]:
        title = text.split('\n')[0]

    return {
        "id": f"life-deepdive-{datetime.now().strftime('%Y%m%d')}",
        "title": title,
        "headline": title,      # Zombie Fix
        "author": persona,
        "body": text,
        "content": text,        # Zombie Fix
        "tag": "History",
        "category": "Lifestyle",
        "image": image_path,    # NOW USES THE REMOTE URL
        "timestamp": datetime.now().isoformat()
    }