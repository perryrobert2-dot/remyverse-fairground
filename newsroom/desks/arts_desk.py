# newsroom/desks/arts_desk.py
from .. import brain
from ..personas import character_sheets
from .. import config
import random
from datetime import datetime

def get_reviews():
    stories = []
    
    # 1. DOG CRITIC
    critic = character_sheets.CRITIC
    text = brain.think(f"You are {critic['name']}. Review a muddy stick. No markdown.", model_type="flash").replace("**", "")
    img = config.get_visual_filename(text, 'critic')
    
    stories.append({
        "id": f"arts-dog-{datetime.now().strftime('%Y%m%d')}",
        "title": "Review: A Muddy Stick",
        "headline": "Review: A Muddy Stick", # Zombie Fix
        "author": critic['name'],
        "body": text,
        "content": text, # Zombie Fix
        "tag": "Review",
        "category": "Culture",
        "image": f"/stock/{img}",
        "timestamp": datetime.now().isoformat()
    })

    # 2. IBIS
    ibis = character_sheets.IBIS
    text = brain.think(f"You are {ibis['name']}. Review a bin. No markdown.", model_type="flash").replace("**", "")
    img = config.get_visual_filename(text, 'ibis')

    stories.append({
        "id": f"arts-ibis-{datetime.now().strftime('%Y%m%d')}",
        "title": "Architecture: The Bin",
        "headline": "Architecture: The Bin", # Zombie Fix
        "author": ibis['name'],
        "body": text,
        "content": text, # Zombie Fix
        "tag": "Architecture",
        "category": "Culture",
        "image": f"/stock/{img}",
        "timestamp": datetime.now().isoformat()
    })
    
    return stories