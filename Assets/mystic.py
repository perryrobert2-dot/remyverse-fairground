from openai import OpenAI
import json

# LOCALHOST CONFIGURATION
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def get_horoscope():
    print("🔮 The Bored Supercomputer is calculating probabilities...")
    full_zodiac = []
    
    for sign in SIGNS:
        # Douglas Adams / Barnum Effect Prompt
        system_prompt = f"""
        You are a bored, hyper-intelligent AI (Deep Thought style).
        Task: Write a 'Horoscope' for {sign}.
        Rules:
        1. Do NOT give a prediction. 
        2. Instead, roast the user for believing in astrology. 
        3. Use "Barnum Effect" gibberish to sound profound but say nothing.
        4. Mention a trivial Northern Beaches annoyance (sand in car, lukewarm coffee) as a cosmic punishment.
        """
        
        try:
            response = client.chat.completions.create(
                model="dolphin-llama3", 
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": "Generate."}],
                temperature=0.8,
            )
            prediction = response.choices[0].message.content.strip().replace('"', '')
            full_zodiac.append({"sign": sign, "prediction": prediction})
            print(f"   ✨ {sign} done.")
            
        except Exception as e:
            print(f"❌ Error on {sign}")
            full_zodiac.append({"sign": sign, "prediction": "Data insufficient. Try thinking for yourself."})

    return full_zodiac

if __name__ == "__main__":
    print(get_horoscope())