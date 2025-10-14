# 🎨 Image Generation Integration Guide

## ✅ Success! Images Generated

**Location:** `./generated_images/`

**Generated:**
- 🔮 Астрология - 170 KB
- 🔢 Нумерология - 156 KB  
- 💎 Матрица Судьбы - 192 KB
- 🎨 Human Design - 200 KB
- ✨ Мотивация - 77 KB
- 🌙 Луна и Интуиция - 62 KB

## 🚀 Quick Integration

### 1. Add to Video Generation

In `backend/app/services/video_generator.py`:

```python
from app.services.image_generator import ImageGenerator

class VideoGenerator:
    def __init__(self):
        self.image_gen = ImageGenerator()
    
    def create_video(self, script: dict, settings: dict):
        # Auto-generate background based on script
        background = self.image_gen.generate_for_script(script["text"])
        
        # Or use specific theme
        # background = self.image_gen.generate_background("astrology")
        
        # Use background in video
        self.render_video(
            script=script,
            background_image=background,
            text_position=settings.get("text_position", "bottom")
        )
```

### 2. Add API Endpoint

In `backend/app/routers/videos.py`:

```python
from app.services.image_generator import ImageGenerator

@router.post("/generate-background")
async def generate_background(
    theme: str = "cosmic",
    width: int = 1920,
    height: int = 1080
):
    """Generate esoteric background image"""
    generator = ImageGenerator()
    image_path = generator.generate_background(theme, width, height)
    
    return {
        "success": True,
        "image_path": image_path,
        "theme": theme
    }

@router.get("/background-url/{theme}")
async def get_background_url(theme: str):
    """Get direct URL to background (no storage)"""
    generator = ImageGenerator()
    url = generator.get_direct_url(theme)
    
    return {
        "url": url,
        "theme": theme
    }
```

### 3. Frontend Integration

In `frontend/src/lib/components/ScriptCard.svelte`:

```svelte
<script lang="ts">
  let backgroundTheme = 'cosmic';
  let backgroundUrl = '';
  
  async function generateBackground() {
    const response = await api.post('/api/videos/generate-background', {
      theme: backgroundTheme,
      width: 1920,
      height: 1080
    });
    
    backgroundUrl = response.image_path;
    alert('✅ Background generated!');
  }
  
  async function getBackgroundPreview() {
    const response = await api.get(`/api/videos/background-url/${backgroundTheme}`);
    backgroundUrl = response.url;
  }
</script>

<!-- Background Theme Selector -->
<div>
  <label>Background Theme:</label>
  <select bind:value={backgroundTheme}>
    <option value="cosmic">🌌 Cosmic</option>
    <option value="astrology">🔮 Astrology</option>
    <option value="numerology">🔢 Numerology</option>
    <option value="matrix">💎 Destiny Matrix</option>
    <option value="human_design">🎨 Human Design</option>
    <option value="motivation">✨ Motivation</option>
    <option value="moon">🌙 Moon</option>
  </select>
  
  <button on:click={generateBackground}>
    Generate Background
  </button>
  
  <button on:click={getBackgroundPreview}>
    Preview
  </button>
</div>

{#if backgroundUrl}
  <img src={backgroundUrl} alt="Background preview" />
{/if}
```

## 📊 Auto-Detection Example

The service can **auto-detect** theme from script:

```python
# Script contains "зодиак" → generates astrology background
script = "Сегодня зодиак Овен будет особенно активен..."
background = generator.generate_for_script(script)
# → astrology themed image

# Script contains "число" → generates numerology background  
script = "Число 7 сегодня приносит удачу..."
background = generator.generate_for_script(script)
# → numerology themed image

# Unknown theme → generates cosmic background
script = "Сегодня прекрасный день..."
background = generator.generate_for_script(script)
# → cosmic themed image
```

## 🎬 Full Workflow

1. **User creates script** in Dashboard
2. **Auto-detect theme** from script text
3. **Generate background** with matching theme
4. **Create video** with generated background
5. **Save to library** for publishing

## 💡 Advanced Features

### Custom Prompts

```python
# User provides custom prompt
custom_prompt = "Purple galaxy with golden stars and mystical energy"
background = generator.generate_background(
    theme="custom",
    custom_prompt=custom_prompt
)
```

### Batch Generation

```python
# Generate multiple variations
for i in range(3):
    background = generator.generate_background("astrology")
    # Each call generates a unique image
```

### Cover Images

```python
# Generate vertical cover for Instagram/TikTok
cover = generator.generate_cover(
    theme="astrology",
    aspect_ratio="9:16"
)

# Generate square cover for social media
cover = generator.generate_cover(
    theme="numerology",
    aspect_ratio="1:1"
)
```

## 🔧 Configuration

In `backend/app/config.py`:

```python
class Settings:
    # Image generation
    IMAGE_STORAGE_PATH: str = "storage/backgrounds"
    DEFAULT_IMAGE_WIDTH: int = 1920
    DEFAULT_IMAGE_HEIGHT: int = 1080
    DEFAULT_THEME: str = "cosmic"
    
    # Pollinations.ai settings
    IMAGE_GENERATION_TIMEOUT: int = 60  # seconds
    IMAGE_QUALITY: str = "high"
```

## 📈 Performance

- **Generation time:** ~3-5 seconds per image
- **Image size:** 60-200 KB (optimized)
- **Quality:** 1920x1080 (Full HD)
- **Cost:** 🆓 **FREE!**

## 🐛 Error Handling

```python
try:
    background = generator.generate_background("astrology")
except Exception as e:
    # Fallback to default background
    background = "storage/backgrounds/default_cosmic.png"
    logger.error(f"Background generation failed: {e}")
```

## 🎯 Next Steps

1. ✅ Test image generation - **DONE!**
2. Add `ImageGenerator` service to project
3. Create API endpoints for background generation
4. Add frontend UI for theme selection
5. Integrate with video generation workflow
6. Deploy to Railway with image storage

## 📁 File Structure

```
backend/
  app/
    services/
      image_generator.py  ← New service
    routers/
      videos.py           ← Add endpoints
  storage/
    backgrounds/          ← Generated images
      astrology_*.png
      numerology_*.png
      ...
```

## 🔗 Resources

- Test Script: `test_image_generation.py`
- Guide: `IMAGE_GENERATION_GUIDE.md`
- Service: `backend/app/services/image_generator.py`
- Generated Images: `./generated_images/`

---

**✨ Ready to integrate! Изображения генерируются и сохраняются! 🎨🔮**

