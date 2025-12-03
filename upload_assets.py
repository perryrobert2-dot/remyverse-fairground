import os
import glob
from google.cloud import storage

# --- CONFIGURATION ---
BUCKET_NAME = "remys-digest-public-assets"
DESTINATION_FOLDER = "static"
LOCAL_ART_FOLDER = "ArtAssets" 

def load_credentials():
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("⚠️  WARNING: No credentials found. Run: set GOOGLE_APPLICATION_CREDENTIALS=remy-key.json")
    return storage.Client()

def upload_static_assets():
    print(f"🎨 Preparing to populate '{DESTINATION_FOLDER}' in {BUCKET_NAME}...")
    
    # 1. Find the images
    extensions = ['*.png', '*.jpg', '*.jpeg', '*.webp']
    files_to_upload = []
    
    # Check if folder exists
    if not os.path.exists(LOCAL_ART_FOLDER):
        print(f"❌ Error: Could not find folder '{LOCAL_ART_FOLDER}'.")
        print(f"   -> Please create a folder named '{LOCAL_ART_FOLDER}' inside C:\\RemyVerse")
        print(f"   -> And put your images (toads, rats, etc.) inside it.")
        return

    for ext in extensions:
        files_to_upload.extend(glob.glob(os.path.join(LOCAL_ART_FOLDER, ext)))
    
    if not files_to_upload:
        print(f"❌ No images found in '{LOCAL_ART_FOLDER}'.")
        return

    print("☁️  Connecting to Google Cloud...")
    try:
        client = load_credentials()
        bucket = client.bucket(BUCKET_NAME)

        print(f"🚀 Uploading {len(files_to_upload)} files...")
        
        url_list = []

        for local_path in files_to_upload:
            filename = os.path.basename(local_path)
            blob_path = f"{DESTINATION_FOLDER}/{filename}"
            blob = bucket.blob(blob_path)
            
            print(f"   -> Uploading {filename}...")
            blob.upload_from_filename(local_path)
            
            # Calculate the public URL
            public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{DESTINATION_FOLDER}/{filename}"
            # Format nicely for the prompt map
            url_list.append(f"[{filename.split('.')[0].upper()}]: \"{public_url}\"")

        print("\n✅ Upload Complete!")
        print("\n--- COPY THESE URLS FOR YOUR AI STUDIO PROMPT ---")
        for url in url_list:
            print(url)

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Check that 'remy-key.json' is in the folder.")

if __name__ == "__main__":
    upload_static_assets()