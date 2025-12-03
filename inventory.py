import os
from google.cloud import storage

# --- CONFIGURATION ---
BUCKET_NAME = "remys-digest-public-assets"
PREFIX = "static/"

def load_credentials():
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("⚠️  WARNING: No credentials found. Run: set GOOGLE_APPLICATION_CREDENTIALS=remy-key.json")
    return storage.Client()

def generate_inventory():
    print(f"📋 Scanning '{BUCKET_NAME}/{PREFIX}'...")
    
    client = load_credentials()
    bucket = client.bucket(BUCKET_NAME)
    
    # List all blobs in the static folder
    blobs = bucket.list_blobs(prefix=PREFIX)
    
    manifest_lines = []
    count = 0

    print("   -> Writing manifest...")

    for blob in blobs:
        # Skip the folder itself if it appears
        if blob.name == PREFIX:
            continue
            
        filename = os.path.basename(blob.name)
        # remove extension for the tag name (e.g., 'toad.png' -> 'TOAD')
        tag_name = filename.rsplit('.', 1)[0].upper()
        
        # Clean up filename (remove spaces, special chars for the tag)
        tag_name = "".join(c for c in tag_name if c.isalnum() or c == '_')

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob.name}"
        
        # Format: [TAG]: "URL"
        line = f"[{tag_name}]: \"{public_url}\""
        manifest_lines.append(line)
        count += 1

    # Write to a file
    output_file = "asset_manifest.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("--- PASTE THIS INTO YOUR AI STUDIO SYSTEM PROMPT ---\n\n")
        f.write("\n".join(manifest_lines))

    print(f"✅ Inventory complete! Found {count} assets.")
    print(f"📄 Saved list to: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    generate_inventory()