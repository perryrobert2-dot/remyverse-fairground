from rembg import remove
from PIL import Image
import io
import os
import shutil

# --- CONFIGURATION ---
INPUT_DIR = "_Raw_Input"
DONE_DIR = "_Processed_Originals"
PROPS_BASE_DIR = "Props"

def process_batch():
    # 1. Check for files
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"📁 Created {INPUT_DIR}. Drop your images there!")
        return

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if not files:
        print(f"⚠️ No images found in {INPUT_DIR}. Drop some files in there first!")
        return

    print(f"found {len(files)} images to process.")
    
    # 2. Ask for the Category/Name
    print("\nWhat are these props? (This will be the filename prefix)")
    print("Examples: waste, corruption, infrastructure, bureaucracy")
    prefix = input("Enter name: ").strip().lower()
    
    # Auto-capitalized folder name (e.g. "waste" -> "Waste")
    target_folder_name = prefix.capitalize()
    target_dir = os.path.join(PROPS_BASE_DIR, target_folder_name)
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"📁 Created new prop category folder: {target_dir}")

    # 3. Process Loop
    for filename in files:
        input_path = os.path.join(INPUT_DIR, filename)
        
        print(f"⚙️ Processing {filename}...")
        
        try:
            # --- REMBG LOGIC ---
            with open(input_path, 'rb') as i:
                input_data = i.read()
                subject_image = Image.open(io.BytesIO(input_data))
                
            output_image = remove(subject_image)
            
            # Auto-Crop empty space
            bbox = output_image.getbbox()
            if bbox:
                output_image = output_image.crop(bbox)

            # --- SMART RENAMING ---
            # Find the next available number (e.g. waste_1, waste_2...)
            counter = 1
            while True:
                new_filename = f"{prefix}_{counter}.png"
                new_path = os.path.join(target_dir, new_filename)
                if not os.path.exists(new_path):
                    break # Found a free name!
                counter += 1
            
            # Save the clean PNG
            output_image.save(new_path)
            print(f"   ✅ Saved as: {new_filename}")

            # Move original to 'Done' folder so we don't process it again
            if not os.path.exists(DONE_DIR): os.makedirs(DONE_DIR)
            shutil.move(input_path, os.path.join(DONE_DIR, filename))

        except Exception as e:
            print(f"   ❌ Failed: {e}")

    print("\n✨ Batch Complete! Your props are ready in the Assets folder.")

if __name__ == "__main__":
    process_batch()