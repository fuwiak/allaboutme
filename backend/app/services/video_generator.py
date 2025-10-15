"""
Simple video generator - uses ONLY frontend settings
No HeyGen, no auto-detection, no defaults
"""

import logging
from pathlib import Path
import tempfile
import requests

logger = logging.getLogger(__name__)

TEMP_DIR = Path(tempfile.gettempdir()) / "allaboutme_videos"
TEMP_DIR.mkdir(exist_ok=True)


def generate_audio_elevenlabs(text: str, voice_id: str) -> Path:
    """
    Generate audio using ElevenLabs API - NO FALLBACKS
    
    Args:
        text: Text to speak
        voice_id: ElevenLabs voice ID from frontend (REQUIRED)
    
    Returns:
        Path to generated audio file
    
    Raises:
        ValueError: If ELEVENLABS_API_KEY not configured
        requests.HTTPError: If API call fails
    """
    import os
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        error_msg = "❌ ELEVENLABS_API_KEY not configured! Add it to .env or Railway variables."
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info(f"🎤 Generating audio with ElevenLabs")
    logger.info(f"   Voice ID: {voice_id}")
    logger.info(f"   Text length: {len(text)} chars")
    
    # Call ElevenLabs API directly
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }
    
    logger.info(f"📡 Calling ElevenLabs API...")
    response = requests.post(url, json=data, headers=headers, timeout=60)
    
    if response.status_code != 200:
        error_msg = f"ElevenLabs API error: {response.status_code} - {response.text}"
        logger.error(f"❌ {error_msg}")
        raise requests.HTTPError(error_msg)
    
    # Save audio
    audio_file = TEMP_DIR / f"audio_elevenlabs_{voice_id[:8]}_{hash(text)}.mp3"
    with open(audio_file, "wb") as f:
        f.write(response.content)
    
    audio_size_mb = audio_file.stat().st_size / 1024 / 1024
    logger.info(f"✅ Audio generated successfully!")
    logger.info(f"   File: {audio_file.name}")
    logger.info(f"   Size: {audio_size_mb:.2f} MB")
    
    return audio_file


def create_video(
    text: str,
    background_path: Path,
    audio_path: Path,
    text_position: str = "center"
) -> tuple[Path, Path]:
    """
    Create video from components
    
    Args:
        text: Script text for subtitles
        background_path: Path to background image
        audio_path: Path to audio file
        text_position: "top", "center", or "bottom"
    
    Returns:
        tuple: (video_path, audio_path)
    """
    logger.info(f"🎬 Creating video...")
    logger.info(f"   Background: {background_path.name}")
    logger.info(f"   Audio: {audio_path.name}")
    logger.info(f"   Text position: {text_position}")
    
    try:
        # Import MoviePy components (correct structure for v2.x)
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        from moviepy.video.VideoClip import ImageClip, TextClip
        from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
        
        # Load audio to get duration
        audio_clip = AudioFileClip(str(audio_path))
        duration = audio_clip.duration
        logger.info(f"   Duration: {duration:.1f}s")
        
        # Create video from background image
        video_clip = ImageClip(str(background_path)).with_duration(duration)
        
        # Resize to 1080x1920 (vertical format)
        video_clip = video_clip.resized(height=1920)
        w, h = video_clip.size
        if w > 1080:
            # Crop center
            x_center = w / 2
            x1 = int(x_center - 540)
            x2 = int(x_center + 540)
            video_clip = video_clip.cropped(x1=x1, x2=x2, y1=0, y2=1920)
        
        # Add text overlay
        clips = [video_clip]
        
        # Determine text vertical position
        if text_position == "top":
            y_pos = 100
        elif text_position == "bottom":
            y_pos = 1920 - 200
        else:  # center
            y_pos = 1920 / 2 - 100
        
        # Split text into chunks for subtitles
        words = text.split()
        words_per_line = 3
        lines = [' '.join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
        
        # Create text clips
        for i, line in enumerate(lines):
            start_time = (i / len(lines)) * duration
            txt_duration = duration / len(lines)
            
            txt_clip = TextClip(
                text=line,
                font_size=50,
                color='white',
                font='Arial',
                stroke_color='black',
                stroke_width=3,
                size=(980, None),
                method='caption'
            ).with_position(('center', y_pos)).with_start(start_time).with_duration(txt_duration)
            
            clips.append(txt_clip)
        
        logger.info(f"✅ Added {len(lines)} text overlays at position: {text_position}")
        
        # Composite
        final_clip = CompositeVideoClip(clips, size=(1080, 1920))
        final_clip = final_clip.with_audio(audio_clip)
        
        # Save
        output_path = TEMP_DIR / f"video_{hash(text)}_{hash(str(background_path))}.mp4"
        
        logger.info(f"💾 Saving video to: {output_path}")
        final_clip.write_videofile(
            str(output_path),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=str(TEMP_DIR / "temp_audio.m4a"),
            remove_temp=True,
            logger=None
        )
        
        # Cleanup
        audio_clip.close()
        final_clip.close()
        
        logger.info(f"✅ Video created: {output_path}")
        logger.info(f"   Size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        return (output_path, audio_path)
        
    except Exception as e:
        logger.error(f"❌ Error creating video: {e}")
        raise


def generate_video_simple(
    text: str,
    voice_id: str,
    background_url: str,
    text_position: str = "center",
    progress_callback=None
) -> tuple[str, str]:
    """
    Main video generation function - uses ONLY frontend settings
    
    Args:
        text: Script text
        voice_id: ElevenLabs voice ID from frontend
        background_url: Background image URL from frontend (/storage/backgrounds/...)
        text_position: Text position from frontend
        progress_callback: Optional callback for progress updates
    
    Returns:
        tuple: (video_url, audio_url)
    """
    logger.info(f"🎬 ========================================")
    logger.info(f"🎬 SIMPLE VIDEO GENERATION (Frontend Settings Only)")
    logger.info(f"🎬 ========================================")
    logger.info(f"📝 Text: {len(text)} chars")
    logger.info(f"🎤 Voice ID: {voice_id}")
    logger.info(f"🖼️  Background URL: {background_url}")
    logger.info(f"📐 Text Position: {text_position}")
    
    try:
        if progress_callback:
            progress_callback("processing", 10)
        
        # 1. Convert background URL to filesystem path
        from .. import storage as storage_module
        
        # Ensure storage is initialized
        if not storage_module.STORAGE_ROOT:
            logger.error("❌ STORAGE_ROOT is None! Initializing...")
            storage_module.init_storage()
            
        if not storage_module.STORAGE_ROOT:
            raise ValueError("STORAGE_ROOT not initialized!")
        
        logger.info(f"✅ STORAGE_ROOT: {storage_module.STORAGE_ROOT}")
        
        if background_url and background_url.startswith('/storage/'):
            relative_path = background_url.replace('/storage/', '')
            background_path = storage_module.STORAGE_ROOT / relative_path
            logger.info(f"🔄 Background URL → Path: {background_path}")
        else:
            raise ValueError(f"Invalid background URL: {background_url}")
        
        if not background_path.exists():
            raise FileNotFoundError(f"Background not found: {background_path}")
        
        logger.info(f"✅ Background found: {background_path.name}")
        
        if progress_callback:
            progress_callback("processing", 30)
        
        # 2. Generate audio with selected voice (NO FALLBACK - must use ElevenLabs)
        logger.info(f"🎤 Generating audio with voice: {voice_id}")
        audio_path = generate_audio_elevenlabs(text, voice_id)
        # If ElevenLabs fails → exception raised → video generation fails
        # NO fallback to gTTS!
        
        if progress_callback:
            progress_callback("processing", 60)
        
        # 3. Create video
        video_path, audio_path = create_video(
            text=text,
            background_path=background_path,
            audio_path=audio_path,
            text_position=text_position
        )
        
        if progress_callback:
            progress_callback("completed", 100)
        
        # Return as file:// URLs
        video_url = f"file://{video_path.absolute()}"
        audio_url = str(audio_path.absolute())
        
        logger.info(f"✅ Video generation complete!")
        logger.info(f"   Video: {video_path}")
        logger.info(f"   Audio: {audio_path}")
        
        return (video_url, audio_url)
        
    except Exception as e:
        logger.error(f"❌ Video generation failed: {e}")
        if progress_callback:
            progress_callback("failed", 0)
        raise

