# newsroom/desks/news_desk.py
from .. import brain 
from ..personas import character_sheets
from .. import config 
import random
from datetime import datetime

def get_editorial(topic):
    persona = character_sheets.EDITOR
    if not topic: topic = "The crisis of the empty treat jar"

    prompt = f"You are {persona['name']}. Write a short Editorial (100 words) about: {topic}. No markdown."
    text = brain.think(prompt, model_type="pro").replace("**", "")
    
    image_file = config.get_visual_filename(text, 'editor')

    return {
        "id": f"news-{datetime.now().strftime('%Y%m%d')}",
        "title": f"Editorial: {topic}",     # For New Frontend
        "headline": f"Editorial: {topic}",  # For Old Frontend (Zombie Fix)
        "author": persona['name'],
        "body": text,                       # For New Frontend
        "content": text,                    # For Old Frontend (Zombie Fix)
        "tag": "News",
        "category": "News",
        "image": f"/stock/{image_file}",
        "timestamp": datetime.now().isoformat()
    }

def get_blotter():
    persona = character_sheets.POLICE
    crime = random.choice(["Mismatched Footwear", "Suspicious Loitering", "Unapproved Bird Bath"])
    
    prompt = f"You are {persona['name']}. Write a Police Blotter entry for: {crime}. No markdown."
    text = brain.think(prompt, model_type="flash").replace("**", "")
    
    image_file = config.get_visual_filename(text, 'police')

    return {
        "id": f"blotter-{datetime.now().strftime('%Y%m%d')}",
        "title": "Police Blotter",
        "headline": "Police Blotter",      # Zombie Fix
        "author": persona['name'],
        "body": text,
        "content": text,                   # Zombie Fix
        "tag": "Blotter",
        "category": "News",
        "image": f"/stock/{image_file}",
        "timestamp": datetime.now().isoformat()
    }