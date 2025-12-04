import os
import sys
from newsroom import staff

# --- Configuration ---
OUTPUT_DIR = "content"
TEMPLATE_FILE = "layout.html"
FINAL_FILE = "index.html"

def main():
    print("[*] POWERING UP NEWSROOM V10.2...")
    
    # 1. Instantiate the Writers
    writers = {
        "lead": staff.PuddlesLead(),
        "roast": staff.RoastMaster(),
        "spray": staff.SprayPolice(),
        "arts": staff.ArtsCornelius(),
        "zoomies": staff.ZoomiesMenace(),
        "pitd": staff.ComicPITD(),
        "soliloquy": staff.SoliloquySoul(),
        "letters": staff.LettersSpit(),
        "mystic": staff.MysticFifi()
    }
    
    # 2. Commission Content (The Build Loop)
    content_map = {}
    for name, writer in writers.items():
        print(f"    -> Commissioning {name.upper()}...")
        try:
            content_map[name] = writer.write()
        except Exception as e:
            print(f"    [!] Error from {name}: {e}")
            content_map[name] = f"<p>Error in {name} module.</p>"

    # 3. Stitch the Edition (The Layout Order)
    # Order: Lead -> Roast -> Spray -> Arts -> Zoomies -> PITD -> Soliloquy -> Back Page (Letters/Mystic)
    
    full_body = f"""
    <div class="edition-wrapper">
        <section id="lead-story">
            {content_map['lead']}
        </section>
        
        <hr class="divider">
        
        <div class="row">
            <div class="col-left">
                {content_map['roast']}
                {content_map['spray']}
                {content_map['arts']}
            </div>
            <div class="col-right">
                {content_map['pitd']}
                {content_map['zoomies']}
                {content_map['soliloquy']}
            </div>
        </div>
        
        <hr class="divider">
        
        <section id="back-page">
            {content_map['letters']}
            {content_map['mystic']}
        </section>
    </div>
    """

    # 4. Merge into Layout
    if not os.path.exists(TEMPLATE_FILE):
        print(f"[!] Template {TEMPLATE_FILE} not found. Creating basic wrapper.")
        final_html = f"<html><body>{full_body}</body></html>"
    else:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template = f.read()
        
        if "{{CONTENT_GOES_HERE}}" in template:
            final_html = template.replace("{{CONTENT_GOES_HERE}}", full_body)
        else:
            print("[!] Placeholder not found, appending content.")
            final_html = template + full_body

    # 5. Publish
    with open(FINAL_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"[+] EDITION PUBLISHED to {FINAL_FILE}")

if __name__ == "__main__":
    main()