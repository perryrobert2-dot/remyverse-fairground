import os
from PIL import Image

# Configuration
IMAGE_DIR = os.path.join("images")

def process_images():
    print(f"[*] The Darkroom: Scanning {IMAGE_DIR} for PNGs...")
    
    if not os.path.exists(IMAGE_DIR):
        print(f"[!] Error: Image directory not found at {IMAGE_DIR}")
        return

    # Scan for PNG files
    files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith('.png')]
    
    if not files:
        print("[-] No PNG files found. carrying on.")
        return

    for filename in files:
        png_path = os.path.join(IMAGE_DIR, filename)
        jpg_filename = os.path.splitext(filename)[0] + ".jpg"
        jpg_path = os.path.join(IMAGE_DIR, jpg_filename)

        try:
            # Open the image
            with Image.open(png_path) as img:
                # Convert RGBA (Transparency) to RGB (White background)
                # This prevents errors if your PNG has a transparent background
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
                    background.paste(img, img.split()[-1])
                    img = background
                
                # Convert to RGB and Save as JPG
                rgb_img = img.convert('RGB')
                rgb_img.save(jpg_path, "JPEG", quality=90)
                
            print(f"[+] Developed: {filename} -> {jpg_filename}")
            
            # Optional: Delete the original PNG to keep folder clean?
            # os.remove(png_path) 
            
        except Exception as e:
            print(f"[!] Failed to convert {filename}: {e}")

if __name__ == "__main__":
    process_images()