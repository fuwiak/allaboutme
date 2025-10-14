# 🎨 Image Generation for Esoteric Themes

## 🎯 What This Does

**Generates images** (not analyzes!) for esoteric content:
- 🔮 **Astrology** - zodiac wheels, cosmic backgrounds
- 🔢 **Numerology** - sacred numbers, mystical symbols  
- 💎 **Destiny Matrix** - energy maps, chakra diagrams
- 🎨 **Human Design** - body graphs, type visualizations
- ✨ **Motivation** - cosmic energy, spiritual vibes
- 🌙 **Moon & Intuition** - lunar phases, celestial magic

## 🆓 FREE Option: Pollinations.ai

**NO API KEY NEEDED!** Just run and get images instantly!

### Quick Test:

```bash
python3 test_image_generation.py
```

Images saved to: `./generated_images/`

## 🚀 How It Works

### 1. Pollinations.ai (FREE!)
- ✅ No registration required
- ✅ No API key needed
- ✅ Unlimited generations
- ✅ High quality 1024x1024
- ✅ No watermarks

**Usage:**
```python
from urllib.parse import quote

prompt = "Mystical zodiac wheel, cosmic background, spiritual art"
encoded = quote(prompt)
url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"

# Download the image
import requests
response = requests.get(url)
with open("image.png", "wb") as f:
    f.write(response.content)
```

### 2. Stability AI (Paid, Optional)
- 💰 Requires API key from https://platform.stability.ai/
- ✨ SDXL 1.0 model
- 🎨 Higher quality & control
- 💸 ~$0.002 per image

**Setup:**
```bash
export STABILITY_API_KEY='sk-...'
```

### 3. Other Options (Future)
- **DALL-E 3** (OpenAI) - $0.04-0.08 per image
- **Midjourney** (Discord bot) - Subscription based
- **Replicate FLUX** - $0.003 per image

## 📋 Test Scenarios

The script tests **6 esoteric themes**:

### 1. 🔮 Astrology
```
Mystical zodiac wheel with all 12 signs, cosmic background, 
stars, planets, ethereal glow, spiritual art, high quality
```

### 2. 🔢 Numerology
```
Sacred numerology symbols, golden numbers 1-9 in mystical circle, 
divine geometry, spiritual energy, cosmic background
```

### 3. 💎 Destiny Matrix
```
Destiny matrix energy map, sacred geometry, chakra colors, 
spiritual pathways, mystical symbols, glowing mandala
```

### 4. 🎨 Human Design
```
Human Design body graph, energy centers, spiritual diagram, 
colorful chakras, cosmic consciousness, mystical blueprint
```

### 5. ✨ Motivation
```
Inspiring cosmic energy, spiritual awakening, golden light, 
universe connection, meditation vibes, peaceful atmosphere
```

### 6. 🌙 Moon & Intuition
```
Mystical moon phases, intuitive wisdom, celestial magic, 
spiritual feminine energy, night sky, stars, ethereal glow
```

## 🎬 Integration with AllAboutMe

### Option 1: Auto-generate backgrounds for scripts

```python
# backend/app/services/image_generator.py

import requests
from urllib.parse import quote

class ImageGenerator:
    @staticmethod
    def generate_esoteric_background(theme: str) -> str:
        """Generate background image for esoteric theme"""
        
        prompts = {
            "astrology": "Mystical zodiac cosmic background, ethereal stars",
            "numerology": "Sacred numbers geometric patterns, golden glow",
            "matrix": "Destiny matrix energy mandala, chakra colors",
            "human_design": "Human Design spiritual blueprint, cosmic energy"
        }
        
        prompt = prompts.get(theme, "Spiritual cosmic background")
        encoded = quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&nologo=true"
        
        # Download and save
        response = requests.get(url, timeout=30)
        filename = f"backgrounds/{theme}_{datetime.now().timestamp()}.png"
        
        with open(filename, "wb") as f:
            f.write(response.content)
        
        return filename
```

### Option 2: Generate from script content

```python
def generate_from_script(script_text: str) -> str:
    """Generate image based on script content"""
    
    # Extract theme from script
    if "зодиак" in script_text.lower():
        prompt = "zodiac signs cosmic art"
    elif "число" in script_text.lower():
        prompt = "mystical numbers sacred geometry"
    else:
        prompt = "spiritual esoteric background"
    
    # Generate
    return generate_image(prompt)
```

### Option 3: User-customizable backgrounds

```python
# In ScriptCard.svelte - Add "Generate Background" button

async function generateBackground() {
    const response = await api.post('/api/generate-background', {
        theme: selectedTheme,
        style: 'mystical'
    });
    
    backgroundUrl = response.image_url;
}
```

## 📊 Expected Output

```bash
$ python3 test_image_generation.py

🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨
🌟 IMAGE GENERATION TEST - ESOTERIC THEMES 🌟
🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨🎨

🎯 Testing image generation for:
   🔮 Астрология
   🔢 Нумерология
   💎 Матрица Судьбы
   🎨 Human Design
   ✨ Мотивация
   🌙 Луна и Интуиция

📡 Available APIs:
   🆓 Pollinations.ai - FREE, no API key needed!

🆓 🆓 🆓 🆓 🆓 🆓 🆓 🆓 🆓 🆓
TESTING POLLINATIONS.AI (FREE)
🆓 🆓 🆓 🆓 🆓 🆓 🆓 🆓 🆓 🆓

============================================================
📝 🔮 Астрология - Знаки Зодиака
============================================================
💬 Prompt: Mystical zodiac wheel with all 12 signs...

⏳ Generating with Pollinations.ai (FREE)...

🔗 Image URL: https://image.pollinations.ai/prompt/...
✅ Image saved: generated_images/🔮_20250114_223045.png
📏 Size: 342.5 KB

...

============================================================
📊 GENERATION SUMMARY
============================================================

✅ Successfully generated: 6/6 images
❌ Failed: 0/6

📁 Images saved in: ./generated_images/

✨ SUCCESS! You can generate esoteric images!

💡 Next steps:
   1. Check images in ./generated_images/
   2. Integrate into AllAboutMe video generator
   3. Generate backgrounds for scripts automatically
```

## 💡 Prompt Engineering Tips

### Good Prompts for Esoteric Themes:

**✅ DO:**
- Use mystical, spiritual, cosmic keywords
- Specify colors (golden, purple, ethereal)
- Mention sacred geometry, mandalas
- Add "high quality", "detailed", "ethereal"
- Use "spiritual art", "mystical background"

**❌ DON'T:**
- Include text/words in prompt (they distort)
- Use negative words ("dark", "ugly")
- Be too vague ("nice image")
- Forget to specify style

### Examples:

```python
# Astrology
"Cosmic zodiac wheel, 12 constellation symbols, ethereal stars, 
purple and gold gradient, mystical sacred geometry, spiritual art"

# Numerology  
"Sacred numbers 1-9 in golden circle, divine geometry patterns,
cosmic energy flow, mystical symbols, spiritual awakening"

# Destiny Matrix
"Energy chakra mandala, colorful spiritual pathways, 
sacred geometry blueprint, cosmic consciousness map"
```

## 🔧 Advanced: Batch Generation

```python
def batch_generate_backgrounds(themes: list, count: int = 3):
    """Generate multiple backgrounds for each theme"""
    
    for theme in themes:
        for i in range(count):
            prompt = get_prompt_for_theme(theme)
            image = generate_with_pollinations(prompt, f"{theme}_{i}")
            print(f"✅ Generated {theme} variation {i+1}")
```

## 📈 Cost Comparison

| Service | Cost per Image | Quality | Setup |
|---------|---------------|---------|-------|
| **Pollinations.ai** | 🆓 FREE | ⭐⭐⭐⭐ | None |
| Stability AI | $0.002 | ⭐⭐⭐⭐⭐ | API Key |
| DALL-E 3 | $0.04-0.08 | ⭐⭐⭐⭐⭐ | API Key |
| Midjourney | $10/mo | ⭐⭐⭐⭐⭐ | Discord |

**Recommendation:** Start with Pollinations.ai (FREE!), upgrade later if needed.

## 🐛 Troubleshooting

### Images look distorted
- Simplify prompt
- Remove text-related keywords
- Add "high quality, detailed"

### Generation too slow
- Use Pollinations.ai (fastest)
- Reduce image size to 512x512
- Check internet connection

### Getting watermarks
- Add `?nologo=true` to Pollinations URL
- Use Stability AI for commercial use

## 📚 Resources

- Pollinations.ai: https://pollinations.ai/
- Stability AI: https://platform.stability.ai/
- Prompt Guide: https://platform.stability.ai/docs/features/prompting
- AllAboutMe i18n: `I18N_IMPLEMENTATION.md`

---

**✨ Ready to generate mystical backgrounds! 🎨🔮🌙**

