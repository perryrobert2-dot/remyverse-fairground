import os
import json
import datetime
from openai import OpenAI

# --- CONFIGURATION ---
# Point to your local LM Studio server
client = OpenAI(base_url="http://192.168.0.52:1234/v1", api_key="lm-studio")

# File Paths
OUTPUT_PATH = r"C:\RemyVerse\fairground\public\data\current_issue.json"

# --- PERSONA DEFINITIONS ---
PROMPTS = {
    "professor": """
        You are Professor Remy, a fastidious dachshund academic in a tweed jacket. 
        You are the Editor of 'The Remy Digest'.
        TONE: Intellectual, precise, slightly oblivious. Use Standard English. No slang.
        You explain the absurdity of the modern world with the dry detachment of a fluid dynamics lecture.
        TASK: Write a witty, cynical headline and a 2-sentence summary about a current event in the 'Edwardian Fairground' (modern politics disguised).
    """,
    
    "critic": """
        You are Remy Senior, a grumpy dachshund critic with an eye patch and a cigar.
        STYLE: Don Rickles meets Jonathan Winters. 
        TONE: Acerbic, loud, surreal. You don't just dislike things; you roast them with bizarre imagery.
        TASK: Write a short, blistering review of a fictional piece of modern art called 'The Void in Beige'. 
        End with a rating out of 5 Bones (usually 0 or 1).
    """,
    
    "mystic": """
        You are The Seer, a dachshund in a turban. 
        STYLE: Dirk Gently's Holistic Detective Agency.
        TONE: Chaos logic. You believe in the fundamental interconnectedness of all things. 
        A butterfly flapping its wings causes you to miss the bus. 
        TASK: Write a horoscope for the sign '{sign}'. It should be a warning, not advice. 
        Connect two completely unrelated things (e.g., toast and entropy).
    """,
    
    "aunt": """
        You are Auntie Remy, wearing a floral bonnet.
        TONE: Dismissive, practical, rude.
        TASK: Answer a reader's letter. The reader is whining about something trivial. 
        Tell them to toughen up. Keep it under 40 words.
    """
}

# --- GENERATOR FUNCTIONS ---

def generate_text(prompt, system_instruction):
    """Helper to call LM Studio."""
    try:
        completion = client.chat.completions.create(
            model="local-model", # LM Studio doesn't care about the name, it uses what's loaded
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error connecting to LM Studio: {e}")
        return "Error: Is LM Studio Server running?"

def build_bento_box():
    print("🌙 Night Shift starting (Target: Local LM Studio)...")
    
    # 1. THE HEADLINE
    print("🎩 The Professor is writing...")
    headline_raw = generate_text("Write the daily headline.", PROMPTS["professor"])
    
    if ":" in headline_raw:
        title, summary = headline_raw.split(":", 1)
    else:
        title = headline_raw
        summary = "Read more in the daily digest."

    headline_data = {
        "title": title.strip(),
        "summary": summary.strip(),
        "author": "Professor Remy",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    # 2. THE ARTS REVIEW
    print("🧐 Remy Senior is roasting...")
    review_text = generate_text("Review 'The Void in Beige'.", PROMPTS["critic"])
    arts_data = {
        "title": "Exhibition: The Void in Beige",
        "review": review_text,
        "rating": "0/5 Bones"
    }

    # 3. THE HOROSCOPES
    print("🔮 The Seer is predicting...")
    zodiac_signs = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo", 
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
    ]
    horoscope_data = []
    
    for sign in zodiac_signs:
        # Update progress on the same line so it doesn't spam the console
        print(f"   -> {sign}...", end="\r") 
        specific_prompt = PROMPTS["mystic"].replace("{sign}", sign)
        prediction = generate_text(f"Write a horoscope for {sign}.", specific_prompt)
        
        horoscope_data.append({
            "sign": sign,
            "icon": f"/zodiac/{sign}.png", 
            "prediction": prediction
        })
    print("\n   -> All signs complete.")

    # 4. AGONY AUNT
    print("👒 Auntie is scolding...")
    advice_text = generate_text("Reader complains: 'My human bought the wrong brand of kibble.'", PROMPTS["aunt"])
    advice_data = {
        "question": "Dear Auntie, my human bought the generic kibble again...",
        "answer": advice_text
    }

    # --- COMPILE JSON ---
    full_issue = {
        "meta": {
            "version": "2.2 (Local)",
            "generated_at": datetime.datetime.now().isoformat()
        },
        "headline": headline_data,
        "arts": arts_data,
        "horoscopes": horoscope_data,
        "advice": advice_data
    }

    # --- SAVE TO DISK ---
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(full_issue, f, indent=2)
    
    print(f"✅ Issue generated successfully. Saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_bento_box()