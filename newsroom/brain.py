import google.generativeai as genai
import time
import random
from newsroom.config import GOOGLE_API_KEY

# Configure once on import
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"   ⚠️ Brain Config Warning: {e}")

def think(prompt, model_type="flash"):
    """
    Centralized generation function.
    Updated to use the stable 2.5 model family to avoid Quota (429) errors.
    """
    
    # SELECTING THE MODEL
    if model_type == "pro":
        # The 'Smart' Brain (for Editorials & Deep Dives)
        # Using stable 2.5 Pro instead of experimental
        model_name = 'models/gemini-2.5-pro'
    else:
        # The 'Fast' Brain (for Blotters, Sports, Real Estate)
        # Using stable 2.5 Flash
        model_name = 'models/gemini-2.5-flash'
    
    try:
        model = genai.GenerativeModel(model_name)
        
        # A small "human" pause to prevent hammering the API too hard
        time.sleep(1.5) 
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        return "Thinking..."
        
    except Exception as e:
        print(f"   ❌ Brain Freeze ({model_name}): {e}")
        
        # FALLBACK: If Pro fails, try Flash (it's cheaper and often has higher limits)
        if model_type == "pro":
            print("   ... 🔄 Attempting fallback to Flash model...")
            return think(prompt, model_type="flash")
            
        return "Content Unavailable (The Writer is on strike)."