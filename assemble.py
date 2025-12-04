import os
import json
import datetime
import newsroom.staff as staff

# --- CONFIGURATION ---
LAYOUT_FILE = "layout.html"
OUTPUT_FILE = "index.html"

# Data Files
WIRE_FILE = "wire_copy.json"
FIGHT_FILE = "fight_card.json"
SAGA_FILE = "saga.json"
RULES_FILE = "council_rules.json"

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def main():
    print("[*] POWERING UP NEWSROOM V10.3...")

    # 1. Load the Brains (Data)
    wire_data = load_data(WIRE_FILE)
    fight_data = load_data(FIGHT_FILE)
    saga_data = load_data(SAGA_FILE)
    rules_data = load_data(RULES_FILE)

    # 2. Instantiate the Staff (Using Correct Class Names)
    print("    -> Waking up Puddles...")
    puddles = staff.Puddles("Puddles", "Chief Tragedian")
    
    print("    -> Waking up Cornelius...")
    cornelius = staff.Cornelius("Cornelius", "Arts Critic")
    
    print("    -> Waking up Arthur Pumble...")
    arthur = staff.ArthurPumble("Arthur Pumble", "Concerned Citizen")
    
    print("    -> Waking up The Zoomies Kid...")
    zoomies = staff.ZoomiesKid("Zoomies Kid", "Local Menace")
    
    print("    -> Waking up Madame Fifi...")
    fifi = staff.MadameFifi("Madame Fifi", "Medium")

    # 3. Commission the Columns
    print("    -> Commissioning LEAD STORY...")
    lead_html = puddles.write_lead(fight_data)

    print("    -> Commissioning ROAST...")
    roast_html = staff.embed_image_section("roast_current.jpg", "Remy Roasts History")

    print("    -> Commissioning ARTS...")
    arts_html = cornelius.write_arts(saga_data)

    print("    -> Commissioning ZOOMIES...")
    zoomies_html = zoomies.write_rant(saga_data)

    print("    -> Commissioning PITD (Comic)...")
    pitd_html = staff.embed_image_section(
        "pitd_current.jpg", 
        "Philosophers Ironic Throw Down", 
        "Fig 1: The inevitable stalemate."
    )

    print("    -> Commissioning SOLILOQUY...")
    soliloquy_html = puddles.write_soliloquy("soliloquy_current.jpg")

    print("    -> Commissioning LETTERS...")
    letters_html = arthur.write_letters_column(saga_data, rules_data)

    print("    -> Commissioning THE SEANCE...")
    mystic_html = fifi.write_seance()

    # 4. Stitch the Body HTML
    # Order: Lead -> Roast -> Arts -> Zoomies -> PITD -> Soliloquy -> Letters -> Mystic
    full_body_html = (
        lead_html +
        roast_html +
        "<hr class='my-8 border-black'>" +
        arts_html +
        zoomies_html +
        "<hr class='my-8 border-black'>" +
        pitd_html +
        soliloquy_html +
        "<div class='bg-stone-100 p-6 mt-8 border-t-4 border-black'>" + # Back Page Wrapper
        letters_html +
        mystic_html +
        "</div>"
    )

    # 5. Merge into Layout (The Printing Press)
    print(f"    -> Printing to {OUTPUT_FILE}...")
    
    if not os.path.exists(LAYOUT_FILE):
        print(f"[!] CRITICAL: {LAYOUT_FILE} missing! Cannot print.")
        return

    with open(LAYOUT_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    # Inject Content
    if "{{CONTENT_GOES_HERE}}" in template:
        final_html = template.replace("{{CONTENT_GOES_HERE}}", full_body_html)
    else:
        # Fallback if tag is missing
        final_html = template + full_body_html

    # 6. Save Live Site
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"[+] SUCCESS: Edition published to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()