import os
from google.cloud import storage
from datetime import datetime, timedelta

# --- CONFIGURATION ---
BUCKET_NAME = "remys-digest-public-assets"

def load_credentials():
    # Credentials must be set via environment variable before running (GOOGLE_APPLICATION_CREDENTIALS)
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("FATAL: GOOGLE_APPLICATION_CREDENTIALS not set.")
        return None
    return storage.Client()

def update_live_pointer():
    print("⏰ Starting daily pointer update...")
    
    # We want yesterday's date, as the publishing script usually runs before midnight, 
    # but the paper is for TODAY. Let's use today's date for simplicity.
    today_date = datetime.now().strftime("%Y-%m-%d")

    client = load_credentials()
    if not client:
        return

    bucket = client.bucket(BUCKET_NAME)
    
    live_source_path = f"content/{today_date}/index.html"
    live_destination_path = "content/current_edition.html"
    
    # 1. Verify the source file exists
    source_blob = bucket.blob(live_source_path)
    if not source_blob.exists():
        # This will fail if the AI hasn't been run yet for the day.
        print(f"🛑 Error: Source file for {today_date} does not exist at {live_source_path}")
        print("   -> The daily edition must be generated and archived first.")
        return

    # 2. Copy the file to the live pointer path
    destination_blob = bucket.blob(live_destination_path)
    
    # Copy operation (atomic update for the live site)
    bucket.copy_blob(source_blob, bucket, live_destination_path)
    
    print(f"✅ Success! Live site pointer set to edition: {today_date}")

if __name__ == "__main__":
    update_live_pointer()