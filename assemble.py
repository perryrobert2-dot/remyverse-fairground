import os
import json
import datetime
import newsroom.staff as staff # Import the consolidated staff module

# --- CONFIGURATION ---
LAYOUT_FILE = "layout.html"
INDEX_FILE = "index.html" # Defines the name of the front page file
OUTPUT_FILE = INDEX_FILE  # Target for the final live site

# Subpage Definitions
BACKPAGE_FILE = "backpage.html"
ARTS_FILE = "arts.html"
SPORTS_FILE = "sports.html" # Placeholder for future links

# Data Files (Relative to Root)
WIRE_FILE = "wire_copy.json"
FIGHT_FILE = "fight_card.json"
SAGA_FILE = "saga.json"
RULES_FILE = "council_rules.json"

def load_data(filename):
    """Loads JSON data safely."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"[!] ERROR: Invalid JSON syntax in {filename}. Check for trailing commas or missing quotes.")
                return {}
    return {}

def print_subpage(filename, content_html):
    """Merges content into layout.html and saves as a subpage."""
    if not os.path.exists(LAYOUT_FILE):
        print(f"[!] CRITICAL: Layout file '{LAYOUT_FILE}' missing. Cannot print subpage.")
        return

    with open(LAYOUT_FILE, "r", encoding="utf-8") as f:
        template = f.read()
    
    # Inject Content
    final_html = template.replace("{{CONTENT_GOES_HERE}}", content_html)

    # Save to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print(f"    -> [Archived] Subpage generated: {filename}")


def main():
    print("[*] POWERING UP NEWSROOM V10.3 (Tiered Content)...")

    # 1. Load All Data Sources
    wire_data = load_data(WIRE_FILE)
    fight_data = load_data(FIGHT_FILE)
    saga_data = load_data(SAGA_FILE)
    rules_data = load_data(RULES_FILE)

    # 2. Instantiate Staff (Using Correct Class Names)
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

    # --- 3. PASS 1: BUILD SUBPAGES (FULL CONTENT) ---
    print("\n[+] PASS 1: Building Full Columns...")
    
    # A. LETTERS, SEANCE, HOROSCOPES (The Back Page)
    letters_full_html = arthur.write_full_letters(saga_data, rules_data)
    seance_full_html = fifi.write_full_seance()
    
    backpage_body = (
        f"<h2>{arthur.name}'s Mailbag</h2>" + letters_full_html +
        f"<h2>{fifi.name}'s Seance</h2>" + seance_full_html
        # Horoscopes would also go here
    )
    print("    -> Building BACKPAGE...")
    print_subpage(BACKPAGE_FILE, backpage_body)
    
    # B. ARTS SECTION
    arts_full_html = cornelius.write_full_arts(saga_data)
    print("    -> Building ARTS PAGE...")
    print_subpage(ARTS_FILE, arts_full_html)
    
    # --- 4. PASS 2: BUILD FRONT PAGE (TEASERS & LEAD) ---
    print("\n[+] PASS 2: Assembling Front Page Teasers...")
    
    # Generate the Lead Story (Always Full Content on Front Page)
    lead_html = puddles.write_full_lead(fight_data)
    
    # Generate Teasers (These rely on the existence of the subpages created above)
    teaser_arts = cornelius.write_teaser(link_to=ARTS_FILE)
    teaser_letters = arthur.write_teaser(link_to=BACKPAGE_FILE)
    
    # Embed Images
    roast_embed = staff.embed_image_section("roast_current.jpg", "Remy Roasts History")
    soliloquy_embed = puddles.write_soliloquy("soliloquy_current.jpg")
    pitd_embed = staff.embed_image_section("pitd_current.jpg", "Philosophers Ironic Throw Down")

    # Stitch the Front Page Body
    front_page_body = (
        lead_html +
        roast_embed +
        "<div class='border-2 border-dashed border-red-700 p-4 my-8'>" +
        "<h2 class='text-red-700 uppercase'>Also in Today's Digest:</h2>" +
        teaser_arts +
        teaser_letters +
        "</div>" +
        soliloquy_embed +
        pitd_embed
    )

    # 5. Final Print (INDEX.HTML)
    print(f"    -> Printing Live Site to {OUTPUT_FILE}...")
    
    if not os.path.exists(LAYOUT_FILE):
        print(f"[!] CRITICAL: {LAYOUT_FILE} missing! Cannot print.")
        return

    with open(LAYOUT_FILE, "r", encoding="utf-8") as f:
        template = f.read()
    
    # Inject Content
    if "{{CONTENT_GOES_HERE}}" in template:
        final_html = template.replace("{{CONTENT_GOES_HERE}}", front_page_body)
    else:
        # Fallback if tag is missing
        final_html = template + front_page_body

    # 6. Save Live Site
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"[+] SUCCESS: Edition published to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()