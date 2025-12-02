import os
from PIL import Image

# Point this to your new Zodiac folder
folder_path = r"C:\RemyVerse\fairground\public\zodiac"

print(f"Scanning {folder_path}...")

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
        
        # 1. Open the image
        full_path = os.path.join(folder_path, filename)
        img = Image.open(full_path)
        
        # 2. Create the new filename (replacing .jpg with .png)
        new_filename = os.path.splitext(filename)[0] + ".png"
        new_path = os.path.join(folder_path, new_filename)
        
        # 3. Save as PNG
        img.save(new_path)
        print(f"Converted: {filename} -> {new_filename}")
        
        # Optional: Delete the old JPG to keep it clean
        # os.remove(full_path) 

print("Done! All images are now PNG.")