# 🎤 ElevenLabs Russian TTS - Test Guide

## ✅ What This Does

Tests **3 beautiful Russian voices** with **8-second text limit** for esoteric content.

## 🎯 Features

- 🇷🇺 **Russian language** optimized
- 🎭 **3 fallback voices** (male + female)
- ⏱️ **~8 seconds** audio duration
- 🔮 **Esoteric themes** (astrology, numerology, matrix, HD)
- 💾 **Auto-save** to `./generated_audio/`
- 🆓 **Free tier** available

## 🚀 Quick Start

### 1. Set API Key

The script automatically loads from `backend/.env` file.

**Check if key exists:**
```bash
cat backend/.env | grep ELEVEN
```

**If not found, add to `backend/.env`:**
```bash
echo 'ELEVENLABS_API_KEY=your-key-here' >> backend/.env
```

**Get your key from:**
https://elevenlabs.io/app/settings/api-keys

### 2. Run Test

```bash
cd /Users/user/allaboutme
python3 test_elevenlabs_russian.py
```

## 🎭 3 Russian Voices (Fallback Order)

### 1️⃣ **Adam** (Primary)
- 🎙️ **Type**: Deep male voice
- 🎨 **Style**: Warm, narrative, professional
- 🎯 **Best for**: Serious topics, horoscopes, forecasts
- ✨ **Why**: Rich tone, authoritative, engaging

### 2️⃣ **Bella** (Fallback #1)
- 🎙️ **Type**: Female, conversational
- 🎨 **Style**: Soft, friendly, gentle
- 🎯 **Best for**: Motivation, affirmations, soft advice
- ✨ **Why**: Warm, approachable, calming

### 3️⃣ **Josh** (Fallback #2)
- 🎙️ **Type**: Young male voice
- 🎨 **Style**: Energetic, clear, modern
- 🎯 **Best for**: Fun content, quick tips, dynamic posts
- ✨ **Why**: Fresh, engaging, upbeat

## 📝 Test Texts (5 Themes)

All texts are **optimized for ~7-8 seconds**:

### 1. 🔮 Astrology
```
Сегодня звёзды обещают удивительный день! 
Луна в Раке дарит вам интуицию и глубокое понимание. 
Доверяйте своим чувствам!
```

### 2. 🔢 Numerology
```
Число семь несёт в себе магию и мудрость. 
Это день для духовного роста и новых открытий. 
Слушайте свой внутренний голос!
```

### 3. 💎 Destiny Matrix
```
Ваша энергетическая матрица сегодня активна! 
Раскройте свои таланты и идите к своему предназначению. 
Вселенная на вашей стороне!
```

### 4. 🎨 Human Design
```
Генераторы сегодня полны энергии! 
Следуйте своему отклику и делайте то, что приносит радость. 
Ваша сила в действии!
```

### 5. ✨ Motivation
```
Вы - создатель своей реальности! 
Каждая мысль формирует ваше будущее. 
Верьте в себя и действуйте с любовью!
```

## 📊 Expected Output

```bash
🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤
🌟 ELEVENLABS RUSSIAN TTS TEST 🌟
🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤🎤

🎯 Testing 3 voices
📝 Testing 5 esoteric themes
⏱️  Target duration: ~8 seconds per audio

============================================================
🎤 Voice: Adam
📝 Theme: 🔮 Астрология
============================================================
💬 Text: Сегодня звёзды обещают удивительный день!...

⏳ Generating audio...

✅ Audio saved: generated_audio/Adam_🔮_20251014_235959.mp3
📏 Size: 45.3 KB
⏱️  Estimated duration: ~7.2 seconds

...

============================================================
📊 TEST SUMMARY
============================================================

✅ Successful: 3/3
❌ Failed: 0/3

📁 Audio files saved in: ./generated_audio/

✨ SUCCESS! ElevenLabs Russian TTS works!

🎧 Listen to the audio files to choose the best voice!

💡 Recommended voice order (fallback):
   1. ✅ Adam - Deep, warm, narrative voice
   2. ✅ Bella - Soft, friendly, engaging
   3. ✅ Josh - Young, energetic, clear
```

## 🔧 Integration with AllAboutMe

### Option 1: Update `renderer.py`

```python
import os
import requests

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# 3 fallback voices
RUSSIAN_VOICES = [
    "pNInz6obpgDQGcFmaJgB",  # Adam (primary)
    "EXAVITQu4vr4xnSDxMaL",  # Bella (fallback 1)
    "TxGEqnHWrfWFTfGW9XjX"   # Josh (fallback 2)
]

def generate_audio_elevenlabs(text: str, output_path: str):
    """Generate audio with 3 fallback voices"""
    
    for i, voice_id in enumerate(RUSSIAN_VOICES):
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            response = requests.post(
                url,
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75,
                        "style": 0.5,
                        "use_speaker_boost": True
                    }
                },
                headers={
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
            response.raise_for_status()
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ Audio generated with voice {i+1}/3")
            return output_path
            
        except Exception as e:
            print(f"⚠️  Voice {i+1} failed: {e}")
            if i < len(RUSSIAN_VOICES) - 1:
                print(f"   Trying fallback voice {i+2}...")
            continue
    
    raise Exception("All 3 voices failed!")
```

### Option 2: Create TTS Service

```python
# backend/app/services/tts_service.py

class TTSService:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voices = [
            "pNInz6obpgDQGcFmaJgB",  # Adam
            "EXAVITQu4vr4xnSDxMaL",  # Bella
            "TxGEqnHWrfWFTfGW9XjX"   # Josh
        ]
    
    def generate(self, text: str, output_path: str) -> str:
        """Generate audio with automatic fallback"""
        
        for voice_id in self.voices:
            try:
                return self._generate_with_voice(text, voice_id, output_path)
            except:
                continue
        
        raise Exception("All voices failed")
```

## ⏱️ Text Duration Guide

To keep audio **~8 seconds**, use these limits:

| Language | Characters | Words | Example |
|----------|-----------|-------|---------|
| Russian | ~180-220 chars | ~25-30 words | 2-3 sentences |
| English | ~200-250 chars | ~35-40 words | 3-4 sentences |

**Our test texts:** 140-180 chars = 7-8 seconds ✅

## 💰 Pricing (ElevenLabs)

- **Free Tier**: 10,000 characters/month
- **Starter**: $5/month - 30,000 chars
- **Creator**: $22/month - 100,000 chars

**Cost per 8-sec audio:** ~$0.0001 (basically free!)

## 📈 Quality Settings

```python
voice_settings = {
    "stability": 0.5,          # 0-1, lower = more expressive
    "similarity_boost": 0.75,  # 0-1, higher = more similar to original
    "style": 0.5,              # 0-1, style exaggeration
    "use_speaker_boost": True  # Better for short-form content
}
```

**For Russian:**
- ✅ Use `eleven_multilingual_v2` model
- ✅ Stability: 0.5 (natural expression)
- ✅ Similarity: 0.75 (consistent voice)
- ✅ Speaker boost: True (clarity)

## 🐛 Troubleshooting

### Error: "Invalid API key"
```bash
# Check .env
cat backend/.env | grep ELEVEN

# Set manually
export ELEVENLABS_API_KEY='your-key-here'
```

### Error: "Quota exceeded"
- Free tier: 10k chars/month
- Check usage: https://elevenlabs.io/app/usage
- Upgrade or wait for reset

### Audio too fast/slow
- Adjust `stability` (lower = slower)
- Reduce text length
- Use different voice

### Poor pronunciation
- Use Cyrillic (not transliteration)
- Add spaces after punctuation
- Avoid complex words

## 📚 Resources

- ElevenLabs Dashboard: https://elevenlabs.io/app
- API Docs: https://elevenlabs.io/docs
- Voice Library: https://elevenlabs.io/voice-library
- Pricing: https://elevenlabs.io/pricing

## 🎯 Integration Example

```python
# In video_tasks.py

from app.services.tts_service import TTSService

@shared_task(bind=True)
def generate_video_task(self, script_id: int):
    # Get script
    script = get_script(script_id)
    
    # Limit text to 8 seconds (~180 chars)
    text = script.post_text[:180]
    
    # Generate audio with ElevenLabs (3 fallbacks)
    tts = TTSService()
    audio_path = tts.generate(text, "output/audio.mp3")
    
    # Continue with video generation...
```

---

**✨ Ready to test Russian TTS with 3 fallback voices! 🎤🇷🇺**

