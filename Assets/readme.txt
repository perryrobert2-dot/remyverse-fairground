cd \RemyVerse\Assets
python factory_assembler.py

Here is the complete **Standard Operating Procedure (SOP)** for the RemyVerse Content Factory.

Save this text as `README.txt` inside your `C:\RemyVerse\` folder.

-----

# 🏭 The RemyVerse Content Factory: Manual

**Version:** 1.0 (Gold Master)
**Output:** Widescreen (1920x1080) Header Images
**Tech Stack:** Python + Pillow (PIL)

### 1\. File Structure

Ensure your folder looks exactly like this. The script relies on these specific filenames.

```text
C:\RemyVerse\Assets\
├── factory_assembler.py      <-- The Engine (Run this)
├── template_professor.png    <-- The Static Background (Professor at Desk)
├── font_bold.ttf             <-- Comic Neue Bold (Header)
├── font_reg.ttf              <-- Comic Neue Regular (Body)
├── prop.png                  <-- (Optional) Transparent PNG of daily item
└── daily_digest_widescreen.jpg <-- The Result (Generated Output)
```

[Image of digital image compositing layers]

### 2\. First Time Setup

If you move this to a new computer, you need to install the image processing library.
Open Command Prompt and run:

```cmd
pip install pillow
```

### 3\. The Gold Master Script (`factory_assembler.py`)

Copy this code into the python file. It handles:

  * **Widescreen Extension:** Extends the wall color to 16:9.
  * **Smart Shadows:** Adds diffuse "cloudy day" shadows under the prop and text box.
  * **Dynamic Layout:** Auto-centers the prop based on available white space.

<!-- end list -->

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# --- CONFIGURATION ---
TEMPLATE_PATH = "template_professor.png"
OUTPUT_PATH = "daily_digest_widescreen.jpg"
PROP_PATH = "prop.png" 

# CANVAS SETTINGS (16x9)
CANVAS_W, CANVAS_H = 1920, 1080
WALL_COLOR = (248, 245, 240) 

# TEXT SETTINGS (EDIT THESE DAILY)
HEADLINE = "Issue #1: The Hydrant"
SUBTEXT = "Why is the Council obsessed\nwith yellow paint?"

def create_digest():
    print("🏭 Starting the Content Factory...")

    # 1. Setup Canvas
    try:
        template = Image.open(TEMPLATE_PATH).convert("RGB")
    except FileNotFoundError:
        print("❌ Error: Missing template_professor.png")
        return

    final_img = Image.new('RGB', (CANVAS_W, CANVAS_H), WALL_COLOR)
    final_img.paste(template, (0, 0))

    # Create shadow layer
    shadow_layer = Image.new('RGBA', final_img.size, (0,0,0,0))
    shadow_draw = ImageDraw.Draw(shadow_layer)

    # --- COORDINATES ---
    box_x, box_y = 1100, 120
    box_w, box_h = 780, 300
    
    # --- LAYER 2: TEXT BOX SHADOW ---
    shadow_offset = 15 
    shadow_draw.rectangle(
        [(box_x + shadow_offset, box_y + shadow_offset), 
         (box_x + box_w + shadow_offset, box_y + box_h + shadow_offset)],
        fill=(200, 200, 190, 150)
    )
    # Blur text box shadow
    blurred_box_shadow = shadow_layer.crop((box_x, box_y, box_x+box_w+50, box_y+box_h+50)).filter(ImageFilter.GaussianBlur(radius=15))
    shadow_layer.paste(blurred_box_shadow, (box_x, box_y))


    # --- LAYER 3: THE PROP & SHADOW ---
    if os.path.exists(PROP_PATH):
        try:
            print("🦴 Adding Prop...")
            prop = Image.open(PROP_PATH).convert("RGBA")
            
            # Resize Logic
            base_width = 250
            w_percent = (base_width / float(prop.size[0]))
            h_size = int((float(prop.size[1]) * float(w_percent)))
            prop = prop.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            # Center Logic
            white_space_start_x = 1050
            white_space_end_x = 1920
            white_space_start_y = box_y + box_h + 50 
            white_space_end_y = 1080
            mid_x = white_space_start_x + (white_space_end_x - white_space_start_x) // 2
            mid_y = white_space_start_y + (white_space_end_y - white_space_start_y) // 2
            prop_x = mid_x - (prop.size[0] // 2)
            prop_y = mid_y - (prop.size[1] // 2)

            # Draw Diffuse Floor Shadow
            prop_blur_canvas = Image.new('RGBA', final_img.size, (0,0,0,0))
            prop_blur_draw = ImageDraw.Draw(prop_blur_canvas)
            
            oval_w = int(base_width * 1.0) 
            oval_h = int(base_width * 0.25)
            shadow_shift_x = 30 # Offset right
            oval_x = prop_x + (base_width - oval_w) // 2 + shadow_shift_x
            oval_y = prop_y + h_size - (oval_h // 2) - 10 

            prop_blur_draw.ellipse([(oval_x, oval_y), (oval_x + oval_w, oval_y + oval_h)], fill=(120, 120, 110, 220))
            blurred_prop_shadow = prop_blur_canvas.filter(ImageFilter.GaussianBlur(radius=25))

            shadow_layer.paste(blurred_prop_shadow, (0,0), blurred_prop_shadow)
            final_img.paste(shadow_layer, (0,0), shadow_layer)
            final_img.paste(prop, (prop_x, prop_y), prop)
            
        except Exception as e:
            print(f"⚠️ Error loading prop: {e}")
    else:
        final_img.paste(shadow_layer, (0,0), shadow_layer)

    draw = ImageDraw.Draw(final_img)

    # --- LAYER 4: MAIN TEXT BOX ---
    draw.rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], fill=(255, 255, 255), outline=(0, 0, 0), width=5)

    # --- TEXT ---
    font_header = None; font_sub = None
    possible_bold = ["font_bold.ttf", "font_bold.ttf.ttf", "ComicNeue-Bold.ttf", "font_bold"]
    possible_reg  = ["font_reg.ttf",  "font_reg.ttf.ttf",  "ComicNeue-Regular.ttf", "font_reg"]

    for name in possible_bold:
        try: font_header = ImageFont.truetype(name, 70); break
        except IOError: continue
    for name in possible_reg:
        try: font_sub = ImageFont.truetype(name, 40); break
        except IOError: continue

    if font_header is None: font_header = ImageFont.load_default(); font_sub = ImageFont.load_default()

    draw.text((box_x + 40, box_y + 30), HEADLINE, font=font_header, fill=(0,0,0))
    draw.text((box_x + 40, box_y + 130), SUBTEXT, font=font_sub, fill=(50,50,50))

    final_img.save(OUTPUT_PATH, quality=95)
    print(f"✅ Success! Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    create_digest()
```

### 4\. Daily Workflow

To create a new Digest header:

1.  **Find a Prop:** Download a transparent PNG (e.g., hydrant, bone, gavel). Rename it `prop.png` and overwrite the old one.
2.  **Edit Text:** Right-click `factory_assembler.py` and choose "Edit". Change the `HEADLINE` and `SUBTEXT` variables at the top.
3.  **Run:** Double-click the script (or run via command line).
4.  **Publish:** Upload `daily_digest_widescreen.jpg` to your website.

**Next step:** Since this is complete, would you like me to analyze the *text content* of your upcoming "Hydrant" issue to make sure the satire hits the mark?