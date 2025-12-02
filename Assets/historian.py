from openai import OpenAI
import time
import random

# LOCALHOST CONFIGURATION
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def get_historical_fact():
    print("📜 The Professor is dusting off the archives...")
    
    system_prompt = """
    You are Professor Remy, a canine historian.
    Task: State ONE historical fact about the Northern Beaches of Sydney.
    Style: Academic, slightly pompous, 100% serious tone (Kayfabe).
    Length: 1-2 sentences max. Keep it short.
    
    Constraint: Never admit this is a joke. Never use the word "Satire".
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="dolphin-llama3", 
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": "Fact please."}],
                temperature=0.8,
                timeout=30
            )
            fact = response.choices[0].message.content.strip()
            return fact.replace('"', '')

        except Exception as e:
            print(f"   ⚠️ Attempt {attempt+1} failed: {e}")
            time.sleep(2)

    return "The archives are currently closed due to an unexpected cat invasion."

if __name__ == "__main__":
    print(get_historical_fact())