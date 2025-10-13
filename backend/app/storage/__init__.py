"""Storage utilities for managing video/audio files"""
import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Storage directories - will be initialized later
STORAGE_ROOT = None
VIDEOS_DIR = None
AUDIO_DIR = None
BACKGROUNDS_DIR = None


def init_storage():
    """Initialize storage directories"""
    global STORAGE_ROOT, VIDEOS_DIR, AUDIO_DIR, BACKGROUNDS_DIR
    
    from ..config import settings
    
    STORAGE_ROOT = Path(settings.STORAGE_PATH)
    VIDEOS_DIR = STORAGE_ROOT / "videos"
    AUDIO_DIR = STORAGE_ROOT / "audio"
    BACKGROUNDS_DIR = STORAGE_ROOT / "backgrounds"
    
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    BACKGROUNDS_DIR.mkdir(parents=True, exist_ok=True)


def get_video_path(video_id: int) -> str:
    """Get path for video file"""
    return str(VIDEOS_DIR / f"video_{video_id}.mp4")


def get_audio_path(video_id: int) -> str:
    """Get path for audio file"""
    return str(AUDIO_DIR / f"audio_{video_id}.mp3")


def cleanup_old_files(days: int = 30):
    """Delete files older than specified days"""
    if not VIDEOS_DIR or not AUDIO_DIR:
        return
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    for directory in [VIDEOS_DIR, AUDIO_DIR]:
        for file_path in directory.glob("*"):
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    try:
                        file_path.unlink()
                        print(f"Deleted old file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")


# Don't initialize on import - will be called by startup_event
# init_storage()

