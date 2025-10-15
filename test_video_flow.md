# VIDEO GENERATION FLOW - Complete Trace

## 1. Frontend (ScriptCard.svelte)
```javascript
const settings = $videoSettings;
// What's in settings?
console.log('FRONTEND:', settings);

api.generateVideo(
  script_id,
  settings.textPosition,
  settings.backgroundUrl,  // ← IS THIS SET?
  settings.voiceId         // ← IS THIS SET?
)
```

## 2. API Client (api.ts)
```typescript
async generateVideo(scriptId, textPosition, customBackground, voiceId) {
  console.log('API CALL:', { textPosition, customBackground, voiceId });
  
  fetch('/api/generate/video', {
    body: JSON.stringify({
      script_id: scriptId,
      text_position: textPosition,
      custom_background: customBackground,  // ← IS THIS SENT?
      voice_id: voiceId                     // ← IS THIS SENT?
    })
  })
}
```

## 3. Backend API (generator.py)
```python
@router.post("/video")
def generate_video(request: GenerateVideoRequest):
    logger.info(f"RECEIVED: {request.custom_background}")  # ← IS THIS RECEIVED?
    logger.info(f"RECEIVED: {request.voice_id}")           # ← IS THIS RECEIVED?
    
    generate_video_task.delay(
        script_id,
        text_position,
        request.custom_background,  # ← IS THIS PASSED?
        request.voice_id            # ← IS THIS PASSED?
    )
```

## 4. Celery Task (video_tasks.py)
```python
def generate_video_task(script_id, text_position, custom_background, voice_id):
    logger.info(f"TASK RECEIVED: bg={custom_background}")  # ← IS THIS RECEIVED?
    logger.info(f"TASK RECEIVED: voice={voice_id}")        # ← IS THIS RECEIVED?
    
    generate_video_simple(
        text,
        voice_id,           # ← IS THIS PASSED?
        custom_background,  # ← IS THIS PASSED?
        text_position
    )
```

## 5. Video Generator (video_generator.py)
```python
def generate_video_simple(text, voice_id, background_url, text_position):
    logger.info(f"GENERATOR RECEIVED: bg={background_url}")  # ← FINAL CHECK
    logger.info(f"GENERATOR RECEIVED: voice={voice_id}")     # ← FINAL CHECK
    
    # Convert & use
    bg_path = convert_url_to_path(background_url)
    audio = generate_audio_elevenlabs(text, voice_id)
    video = create_video(text, bg_path, audio, text_position)
```

## EXPECTED OUTPUT (when working):
```
[Frontend] Store: { backgroundUrl: "/storage/...", voiceId: "EXA..." }
[API] Sending: { custom_background: "/storage/...", voice_id: "EXA..." }
[Backend API] Received: custom_background=/storage/..., voice_id=EXA...
[Celery Task] Task params: bg=/storage/..., voice=EXA...
[Generator] Final params: bg=/storage/..., voice=EXA...
🔄 Converted URL to path: /Users/user/.allaboutme/storage/...
✅ Using custom background!
🎤 Generating with ElevenLabs voice!
```

## If ANY of these is missing/None - WE KNOW WHERE THE PROBLEM IS!
