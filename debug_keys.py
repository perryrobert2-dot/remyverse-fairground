import os
import json

# Define where the keys SHOULD be
KEY_FILE_PATH = os.path.join("newsroom", "keys.json")

print(f"[*] AUDIT: Checking for key file at: {KEY_FILE_PATH}")

# 1. Check if file exists
if not os.path.exists(KEY_FILE_PATH):
    print(f"[!] FAIL: File not found!")
    print(f"    Please make sure you saved 'keys.json' inside the 'newsroom' folder.")
    print(f"    Current location: {os.path.abspath(KEY_FILE_PATH)}")
    exit()
else:
    print(f"[+] PASS: File exists.")

# 2. Check content format
try:
    with open(KEY_FILE_PATH, "r") as f:
        content = f.read()
        print(f"[*] File Content (First 20 chars): {content[:20]}...")
        
        # Reset read head
        f.seek(0)
        data = json.load(f)
        print(f"[+] PASS: Valid JSON format.")

        # 3. Check for specific keys
        gemini_key = data.get("gemini")
        if not gemini_key:
            print("[!] FAIL: JSON is missing the 'gemini' field.")
        elif gemini_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
            print("[!] FAIL: You haven't pasted your key yet! It still has the placeholder text.")
        elif str(gemini_key).startswith("{"):
            print("[!] FAIL: It looks like you pasted the contents of 'remy-key.json' here.")
            print("    The 'gemini' key must be the short string starting with 'AIza...', not the full JSON object.")
        elif not str(gemini_key).startswith("AIza"):
            print("[!] WARNING: The key doesn't look like a standard Google API Key (usually starts with 'AIza').")
            print(f"    Current value starts with: {str(gemini_key)[:5]}...")
        else:
            print("[+] PASS: Gemini Key looks valid (starts with AIza).")

except json.JSONDecodeError:
    print("[!] FAIL: The file contains invalid JSON. Check for missing quotes or commas.")
except Exception as e:
    print(f"[!] FAIL: Unexpected error: {e}")

input("\nPress Enter to exit...")