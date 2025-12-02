import os
import datetime
from jinja2 import Environment, FileSystemLoader

# --- MOCK DATA (Just to test the plumbing first) ---
def get_mock_stories():
    return [
        {
            "desk": "LIFESTYLE",
            "headline": "Holistic Horoscope: The 199 Bus",
            "content": "The universe suggests you stop waiting. The 199 is not a bus; it is a metaphor for your stalling career. Walk.",
            "image_keyword": "bus"
        },
        {
            "desk": "NEWS",
            "headline": "Bin Chicken Declared Mayor",
            "content": "In a shock landslide, a particularly aggressive ibis has seized control of the Council chambers.",
            "image_keyword": "ibis"
        },
        {
            "desk": "ARTS",
            "headline": "Abstract Sculpture or Pile of Rubbish?",
            "content": "Local critics are baffled by the new installation in Dee Why. Turns out it was just hard rubbish collection day.",
            "image_keyword": "rubbish"
        }
    ]

def build():
    print("🔥 Starting V10 Build Engine...")

    # 1. Setup Jinja2 (The Template Engine)
    # This looks for the 'templates' folder you just made
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    
    # 2. Get Data
    print("... Fetching stories")
    stories = get_mock_stories()
    
    # 3. Render HTML
    print("... Compiling HTML")
    output = template.render(
        stories=stories,
        build_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    
    # 4. Save to /dist
    # This creates a 'dist' folder automatically if it's missing
    os.makedirs('dist', exist_ok=True)
    
    with open('dist/index.html', 'w', encoding='utf-8') as f:
        f.write(output)
        
    print(f"✅ Build Complete! Generated {len(stories)} stories.")
    print("👉 Check the new 'dist' folder and open 'index.html'!")

if __name__ == "__main__":
    build()