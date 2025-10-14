# 🔮 Qwen Vision API Test - Esoteric Themes

## 📋 Description

This test script demonstrates how to use **Qwen 2.5 Vision AI** to generate content for esoteric themes:
- 🔮 **Астрология** - horoscopes, zodiac compatibility
- 🔢 **Нумерология** - numerology forecasts, life path numbers  
- 💎 **Матрица Судьбы** - destiny matrix, karmic tasks
- 🎨 **Human Design** - personality types, life strategy
- ✨ **Мотивация** - daily affirmations, insights

## 🚀 Quick Start

### 1. Get OpenRouter API Key

1. Go to https://openrouter.ai/
2. Sign up / Log in
3. Go to **Keys** section
4. Create a new API key
5. Copy your key

### 2. Set Environment Variable

```bash
export OPENROUTER_API_KEY='your-key-here'
```

Or add to `.env` file:
```bash
OPENROUTER_API_KEY=your-key-here
```

### 3. Run Test

```bash
cd /Users/user/allaboutme
python3 test_qwen_vision.py
```

## 🎯 What It Does

The script tests **5 scenarios**:

1. **🔮 Astrology** - Analyzes cosmic images for zodiac compatibility
2. **🔢 Numerology** - Generates numerology forecasts from abstract patterns
3. **💎 Destiny Matrix** - Interprets energy patterns and karmic tasks
4. **🎨 Human Design** - Determines personality type from images
5. **✨ Motivation** - Creates daily affirmations from nature scenes

Each scenario:
- ✅ Sends an image URL to Qwen Vision AI
- ✅ Provides a Russian prompt for esoteric interpretation
- ✅ Gets a 2-3 sentence response in Russian
- ✅ Shows token usage and success rate

## 📊 Expected Output

```
🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮
🌟 QWEN VISION API TEST - ESOTERIC THEMES 🌟
🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮🔮

📡 API: OpenRouter
🤖 Model: qwen/qwen2.5-vl-32b-instruct:free
🎯 Purpose: Generate astrology/numerology/matrix/HD content

============================================================
📝 🔮 Астрология - Совместимость знаков
============================================================
🖼️  Image: https://images.unsplash.com/photo-1532968961962...
💬 Prompt: Проанализируй это изображение с точки зрения...

⏳ Generating response...

✅ Response:
[AI-generated astrological insight in Russian]

📊 Tokens used: 85
...
```

## 🔧 Integration with AllAboutMe

After successful test, you can integrate this into the video generator:

### Option 1: Add to `generator.py`

```python
from openai import OpenAI

def generate_with_vision(theme: str, image_url: str):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    completion = client.chat.completions.create(
        model="qwen/qwen2.5-vl-32b-instruct:free",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": f"Generate {theme} content..."},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }]
    )
    
    return completion.choices[0].message.content
```

### Option 2: Create Image Analysis Service

```python
# backend/app/services/vision_service.py
class VisionService:
    def analyze_for_astrology(self, image_url: str) -> str:
        """Generate astrology content from image"""
        
    def analyze_for_numerology(self, image_url: str) -> str:
        """Generate numerology content from image"""
        
    def analyze_for_matrix(self, image_url: str) -> str:
        """Generate destiny matrix content from image"""
```

## 💡 Use Cases

1. **Auto-generate content from user photos**
   - User uploads selfie → Get Human Design type
   - User uploads sky photo → Get astrological forecast

2. **Theme-based script generation**
   - Daily horoscope with cosmic images
   - Numerology insights from number patterns
   - Matrix readings from sacred geometry

3. **Visual content enhancement**
   - Analyze video backgrounds for deeper meaning
   - Generate captions based on visual symbols

## 🔒 Security Notes

- ⚠️ **Never commit API keys to Git**
- ✅ Use environment variables
- ✅ Add to `.gitignore`: `test_qwen_vision.py` (if it contains keys)
- ✅ Use OpenRouter for cost control and API rotation

## 📈 Model Info

**Model**: `qwen/qwen2.5-vl-32b-instruct:free`
- 🆓 **Free tier available**
- 🖼️ **Vision + Text** capabilities
- 🌍 **Multilingual** (supports Russian)
- ⚡ **Fast** response times
- 🎯 **Specialized** in visual reasoning

## 🐛 Troubleshooting

### Error: "OPENROUTER_API_KEY not set"
```bash
export OPENROUTER_API_KEY='sk-or-v1-...'
```

### Error: "Rate limit exceeded"
- Wait a few seconds
- Use OpenRouter's free tier limits
- Consider upgrading for higher rates

### Error: "Invalid image URL"
- Check image URL is accessible
- Use direct image links (not pages)
- Try different image hosting

## 📚 Resources

- OpenRouter Docs: https://openrouter.ai/docs
- Qwen VL Model: https://openrouter.ai/models/qwen/qwen2.5-vl-32b-instruct
- AllAboutMe Docs: `I18N_IMPLEMENTATION.md`

---

**✨ Ready to generate mystical content from images! 🔮**

