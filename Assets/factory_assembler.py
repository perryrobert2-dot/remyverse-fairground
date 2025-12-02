import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# --- CONFIGURATION ---
ASSETS_DIR = r"C:\RemyVerse\Assets"
OUTPUT_DIR = r"C:\RemyVerse\Output"

TEMPLATE_MAP = {
    "neutral": "template_professor.png",
    "happy": "template_happy.png",
    "shocked": "template_shocked.png",
    "suspicious": "template_suspicious.png",
    "angry": "template_angry.png",
    "dottie": "agony_aunt.png"
}

# Font & Layout Settings
FONT_PATH = "arial.ttf"
HEADLINE_SIZE = 42  # Reduced from 48 to prevent cutoff
DATE_SIZE = 24
TOP_BANNER_HEIGHT = 140

def remove_white_bg(img):
    """
    HACK: Turns white pixels into transparent pixels.
    Useful for props generated with white backgrounds.
    """
    img = img.convert("RGBA")
    datas = img.getdata()
    
    newData = []
    for item in datas:
        # If pixel is very white (R>220, G>220, B>220), make it transparent
        if item[0] > 220 and item[1] > 220 and item[2] > 220:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    return img

def get_wrapped_text(text, font, max_width):
    # Reduced width to 40 characters to force wrapping sooner
    lines = textwrap.wrap(text, width=40)
    return lines

def create_daily_issue(headline, date_str, mood="neutral", prop_name=None, issue_number=1):
    print(f"--- Assembling Issue #{issue_number} ---")

    # 1. Load Base Image
    template_file = TEMPLATE_MAP.get(mood.lower(), "template_professor.png")
    template_path = os.path.join(ASSETS_DIR, template_file)
    
    if not os.path.exists(template_path):
        print(f"ERROR: Template not found at {template_path}")
        return

    base_img = Image.open(template_path).convert("RGBA")
    base_w, base_h = base_img.size

    # 2. Add Prop (Resized & Background Removed)
    if prop_name:
        prop_file = f"{prop_name}.png"
        prop_path = os.path.join(ASSETS_DIR, prop_file)
        if os.path.exists(prop_path):
            prop_img = Image.open(prop_path)
            
            # Clean the background
            prop_img = remove_white_bg(prop_img)
            
            # Resize
            target_w = int(base_w * 0.22)
            aspect_ratio = prop_img.height / prop_img.width
            target_h = int(target_w * aspect_ratio)
            prop_img = prop_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            
            # Position: Bottom Right with padding
            offset_x = base_w - target_w - 40
            offset_y = base_h - target_h - 40
            base_img.alpha_composite(prop_img, (offset_x, offset_y))

    # 3. GENERATE SOCIAL SQUARE (Clean)
    min_dim = min(base_w, base_h)
    left = (base_w - min_dim) / 2
    top = (base_h - min_dim) / 2
    right = (base_w + min_dim) / 2
    bottom = (base_h + min_dim) / 2
    
    img_square = base_img.crop((left, top, right, bottom))
    filename_square = f"issue_{issue_number}_{mood}_sq.jpg"
    save_path_square = os.path.join(OUTPUT_DIR, filename_square)
    img_square.convert('RGB').save(save_path_square, quality=95)
    print(f"Saved Clean Social Square: {save_path_square}")

    # 4. DRAW FULL-WIDTH TOP BANNER
    draw = ImageDraw.Draw(base_img)
    try:
        font_headline = ImageFont.truetype(FONT_PATH, HEADLINE_SIZE)
    except IOError:
        font_headline = ImageFont.load_default()

    # Draw Banner Box
    draw.rectangle(
        (0, 0, base_w, TOP_BANNER_HEIGHT), 
        fill="#FFFFFF", 
        outline="#000000", 
        width=4
    )

    # Calculate Text
    wrapped_lines = get_wrapped_text(headline, font_headline, base_w - 100)
    line_height = HEADLINE_SIZE + 8
    total_text_height = len(wrapped_lines) * line_height
    
    text_y_start = (TOP_BANNER_HEIGHT - total_text_height) / 2
    text_x_pad = 40

    # Draw Text
    current_y = text_y_start
    for line in wrapped_lines:
        draw.text((text_x_pad, current_y), line, font=font_headline, fill="#000000")
        current_y += line_height

    # 5. Save Final Banner
    filename_banner = f"issue_{issue_number}_{mood}.png"
    save_path_banner = os.path.join(OUTPUT_DIR, filename_banner)
    base_img.save(save_path_banner)
    print(f"Saved Final Banner: {save_path_banner}")

if __name__ == "__main__":
    create_daily_issue("COUNCIL APPROVES CONTROVERSIAL 'GIANT BIN CHICKEN' STATUE FUNDING", "27 Nov", "shocked", "ibis", 102)