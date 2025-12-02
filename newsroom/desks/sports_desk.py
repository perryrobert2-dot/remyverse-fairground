# newsroom/desks/sports_desk.py
from .. import brain
from ..personas import character_sheets
from .. import config
import random
from datetime import datetime

def get_the_circus():
    stories = []
    
    # 1. ZOOMIE
    reporter = character_sheets.ZOOMIE
    text = brain.think(f"You are {reporter['name']}. Sports report about chasing a ball. No markdown.", model_type="flash").replace("**", "")
    img = config.get_visual_filename(text, 'zoomie')
    
    stories.append({
        "id": f"sport-zoomie-{datetime.now().strftime('%Y%m%d')}",
        "title": "LIVE: The Chase",
        "headline": "LIVE: The Chase", # Zombie Fix
        "author": reporter['name'],
        "body": text,
        "content": text, # Zombie Fix
        "tag": "Live Action",
        "category": "Sports",
        "image": f"/stock/{img}",
        "timestamp": datetime.now().isoformat()
    })

    # 2. ADMIN
    admin = character_sheets.NETBALL_MUM
    text = brain.think(f"You are {admin['name']}. Notice about socks. No markdown.", model_type="flash").replace("**", "")
    img = config.get_visual_filename(text, 'netball')

    stories.append({
        "id": f"sport-admin-{datetime.now().strftime('%Y%m%d')}",
        "title": "NOTICE: Uniform Policy",
        "headline": "NOTICE: Uniform Policy", # Zombie Fix
        "author": admin['name'],
        "body": text,
        "content": text, # Zombie Fix
        "tag": "Notice",
        "category": "Sports",
        "image": f"/stock/{img}",
        "timestamp": datetime.now().isoformat()
    })
    
    return stories