from openai import OpenAI
import json
import ast

# LOCALHOST CONFIGURATION
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def get_classifieds():
    print("📢 The Barker is shouting for attention...")
    
    system_prompt = """
    You are a JSON generator. 
    Task: Output a Python list of 3 satirical classified ads for the Northern Beaches.
    RULES: Do NOT use numbers. Output ONLY the list.
    Example: ["For Sale: Invisible Surfboard. $50", "Lost: Will to live. Last seen at B-Line."]
    """
    
    try:
        response = client.chat.completions.create(
            model="dolphin-llama3", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": "GENERATE_ADS"}],
            temperature=0.7,
        )
        content = response.choices[0].message.content.strip()
        if "```" in content:
            content = content.replace("```python", "").replace("```json", "").replace("```", "").strip()
        start = content.find('[')
        end = content.rfind(']') + 1
        
        if start != -1 and end != -1:
            return ast.literal_eval(content[start:end])
        else:
            return ["For Sale: AI Confusion.", "Lost: The JSON Format.", "Service: Manual Override."]
            
    except Exception as e:
        print(f"❌ Error asking The Barker: {e}")
        return ["Error: Barker Offline."]