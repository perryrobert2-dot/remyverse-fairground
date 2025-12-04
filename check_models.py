import google.generativeai as genai
import os
import json

# 1. Load the existing key from your vault
KEY_FILE = os.path.join("newsroom", "keys.json")

print(f"[*] Reading credentials from {KEY_FILE}...")

try:
    with open(KEY_FILE, "r") as f:
        secrets = json.load(f)
        api_key = secrets.get("gemini")
except FileNotFoundError:
    print("[!] CRITICAL: Key file not found. Create newsroom/keys.json first.")
    exit()

if not api_key or "PASTE_YOUR" in api_key:
    print("[!] CRITICAL: Invalid API Key in file.")
    exit()

# 2. Connect to Google
print("[*] Authenticating with Google Gemini...")
genai.configure(api_key=api_key)

# 3. List available models
print("\n[+] SUCCESS. Here are the models available to you:\n")
print(f"{'MODEL NAME':<30} | {'CAPABILITIES'}")
print("-" * 50)

try:
    found_any = False
    for m in genai.list_models():
        # We only care about models that can write text (generateContent)
        if 'generateContent' in m.supported_generation_methods:
            print(f"{m.name:<30} | Text Generation")
            found_any = True
    
    if not found_any:
        print("[!] No text generation models found. Check your API access.")

except Exception as e:
    print(f"[!] Error fetching models: {e}")
    print("    (This usually means the Key is wrong or the API is down)")

print("\n[*] INSTRUCTION: Update 'newsroom/staff.py' with one of the names above.")
input("\nPress Enter to exit...")