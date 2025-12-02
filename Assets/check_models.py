import google.generativeai as genai
import os

def list_available_models():
    print("\n🔑 GOOGLE API KEY CHECKER")
    print("--------------------------------------------------")
    # Ask for input instead of hardcoding
    api_key = input("👉 Paste your Google API Key here and hit Enter: ").strip()

    if not api_key.startswith("AIza"):
        print("\n⚠️ WARNING: That doesn't look like a standard Google API key.")
        print("   It should start with 'AIza'.")
        print("   Please check you copied the whole string.\n")

    try:
        genai.configure(api_key=api_key)
        
        print("\n🔍 CONTACTING GOOGLE MOTHERSHIP...")
        
        # Iterate through models and filter for those that can generate text
        found = False
        print("\n✅ SUCCESS! CONNECTED.")
        print("--------------------------------------------------")
        print(f"{'INTERNAL NAME (Use this)':<35} | {'DISPLAY NAME'}")
        print("--------------------------------------------------")
        
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"{m.name:<35} | {m.display_name}")
                found = True
                
        if not found:
            print("⚠️ Connected, but no text-generation models were found.")
            print("   (This is rare. Check permissions in Google Cloud Console).")
            
        print("--------------------------------------------------")

    except Exception as e:
        print(f"\n❌ CONNECTION FAILED: {e}")
        print("\nTroubleshooting:")
        print("1. Go to https://aistudio.google.com/app/apikey")
        print("2. Create a NEW key in a new project.")
        print("3. Ensure 'Generative Language API' is enabled for that project.")

if __name__ == "__main__":
    list_available_models()
    input("\nPress Enter to exit...")