from rembg import remove
from PIL import Image
import io
import os

# CONFIGURATION
INPUT_FILE = "waste_4.png"
OUTPUT_FILE = "sprite_waste_4.png"

def clean_image():
    print(f"Loading {INPUT_FILE}...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Could not find {INPUT_FILE}")
        return

    # 1. Open the image
    with open(INPUT_FILE, 'rb') as i:
        input_data = i.read()
        subject_image = Image.open(io.BytesIO(input_data))

    # 2. Remove Background (The heavy lifting)
    print("Removing background (this downloads a model on the first run)...")
    output_image = remove(subject_image)

    # 3. Auto-Crop (Trim the empty transparent space)
    print("Trimming empty space...")
    bbox = output_image.getbbox()
    if bbox:
        output_image = output_image.crop(bbox)

    # 4. Save
    output_image.save(OUTPUT_FILE)
    print(f"Success! Saved clean sprite to {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_image()