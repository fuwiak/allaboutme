"""
Migration script: config.yaml → PostgreSQL settings table
Run this once after initial deployment to import existing settings
"""
import yaml
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import SessionLocal
from app.models import Setting


def migrate_config():
    """Migrate config.yaml to database settings"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return
    
    # Load config
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    db = SessionLocal()
    try:
        # Migrate each setting
        settings_map = {
            "daily_videos": str(config.get("daily_videos", 2)),
            "caption_template": config.get("caption_template", ""),
            "system_prompt": config.get("system_prompt", ""),
            "themes": ",".join(config.get("themes", [])),
            "video_generator": config.get("video_generator", "heygen"),
            "video_duration": str(config.get("video_duration", 15)),
            "heygen_use_avatar": str(config.get("heygen_use_avatar", False)),
            "heygen_voice": config.get("heygen_voice", "en-US-Neural2-F"),
            "heygen_background_url": config.get("heygen_background_url", ""),
            "opensource_background": config.get("opensource_background", "space"),
            "opensource_add_subtitles": str(config.get("opensource_add_subtitles", True)),
        }
        
        for key, value in settings_map.items():
            setting = db.query(Setting).filter(Setting.key == key).first()
            
            if setting:
                setting.value = value
                print(f"✅ Updated: {key} = {value[:50]}...")
            else:
                setting = Setting(key=key, value=value)
                db.add(setting)
                print(f"➕ Created: {key} = {value[:50]}...")
        
        db.commit()
        print(f"\n✅ Successfully migrated {len(settings_map)} settings to database")
    
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        db.rollback()
    
    finally:
        db.close()


if __name__ == "__main__":
    migrate_config()

