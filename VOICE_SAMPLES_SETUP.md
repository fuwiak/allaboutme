# 🎤 Voice Samples Setup Guide

## ✅ Co Zostało Zrobione

Wygenerowano **prawdziwe próbki głosów ElevenLabs** dla frontendu!

## 📁 Generated Files

```
frontend/static/voice-samples/
  ├── adam.mp3   (43 KB) - Deep male voice
  ├── bella.mp3  (42 KB) - Soft female voice
  └── josh.mp3   (33 KB) - Young male voice
```

## 🚀 How It Works

### 1. Generate Samples (One Time Setup)

```bash
# Generate real ElevenLabs samples
python3 generate_voice_samples.py
```

**Output:**
- ✅ `frontend/static/voice-samples/adam.mp3`
- ✅ `frontend/static/voice-samples/bella.mp3`
- ✅ `frontend/static/voice-samples/josh.mp3`

### 2. Frontend Uses Static Files

```svelte
const voices = [
  {
    id: 'pNInz6obpgDQGcFmaJgB',
    name: 'Adam',
    sampleFile: '/voice-samples/adam.mp3'  // ← Static file
  }
];

// Play sample
currentAudio = new Audio(voice.sampleFile);
await currentAudio.play();
```

### 3. Build & Deploy

```bash
cd frontend
npm run build

cd ..
rm -rf backend/app/static
cp -r frontend/build backend/app/static
```

Voice samples are included in build → served as static files!

## 🎯 Voice Configuration

### Current Voices (3)

| Voice | ID | File | Description |
|-------|-----|------|-------------|
| 🎙️ Adam | `pNInz6obpgDQGcFmaJgB` | `adam.mp3` | Deep male - warm, narrative |
| 🎤 Bella | `EXAVITQu4vr4xnSDxMaL` | `bella.mp3` | Female - soft, friendly |
| 🔊 Josh | `TxGEqnHWrfWFTfGW9XjX` | `josh.mp3` | Young male - energetic |

### Add More Voices

Edit `generate_voice_samples.py`:

```python
VOICES = [
    # ... existing voices ...
    {
        "id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "name": "rachel",
        "label": "Rachel - Calm Female",
        "text": "Новый голос для тестирования!"
    }
]
```

Run:
```bash
python3 generate_voice_samples.py
```

Update frontend `ScriptCard.svelte`:
```javascript
const voices = [
  // ... existing voices ...
  {
    id: '21m00Tcm4TlvDq8ikWAM',
    name: 'Rachel',
    sampleFile: '/voice-samples/rachel.mp3'
  }
];
```

## 💡 Advantages

✅ **Real ElevenLabs voices** - not browser TTS  
✅ **No CORS issues** - served as static files  
✅ **Fast loading** - cached by browser  
✅ **Offline preview** - works without backend  
✅ **Production quality** - actual voice you'll use  
✅ **One-time generation** - reuse same samples  

## 🔄 Regenerate Samples

If you change voices or text:

```bash
# 1. Update generate_voice_samples.py
# 2. Run generator
python3 generate_voice_samples.py

# 3. Rebuild frontend
cd frontend && npm run build

# 4. Deploy
cd .. && rm -rf backend/app/static && cp -r frontend/build backend/app/static
```

## 🎬 Integration with Video Generation

When user selects a voice and generates video, pass the voice ID:

```javascript
// In ScriptCard.svelte
async function startVideoGeneration() {
  const result = await api.generateVideo(
    script.id,
    textPosition,
    selectedVoice  // ← Pass voice ID
  );
}
```

Backend uses this ID with ElevenLabs:
```python
# In video_tasks.py
def generate_video(script_id, text_position, voice_id):
    # Use voice_id with ElevenLabs API
    audio = generate_audio_elevenlabs(text, voice_id)
```

## 📋 File Structure

```
frontend/
  static/
    voice-samples/
      adam.mp3    ← Generated samples
      bella.mp3
      josh.mp3
  src/
    lib/
      components/
        ScriptCard.svelte  ← Uses samples

backend/
  app/
    static/  ← After build, contains voice-samples/
```

## 🐛 Troubleshooting

### Samples not playing

1. Check files exist:
```bash
ls -lh frontend/static/voice-samples/
```

2. Regenerate:
```bash
python3 generate_voice_samples.py
```

3. Rebuild frontend:
```bash
cd frontend && npm run build
```

### API quota exceeded

- Free tier: 10,000 chars/month
- Each sample: ~50 chars = 150 chars total
- Can generate 60+ times per month

### Want different samples

Edit `generate_voice_samples.py` and change `text` field.

## 🎯 Next Steps

1. ✅ Samples generated
2. ✅ Frontend updated to use samples
3. Update backend to use `selectedVoice` in video generation
4. Add voice ID to database schema
5. Deploy to Railway

---

**✨ Prawdziwe głosy ElevenLabs w static files! 🎤**

