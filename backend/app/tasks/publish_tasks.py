"""Celery tasks for publishing videos"""
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from .celery_app import celery_app
from ..database import SessionLocal
from .. import models
from ..services import publisher

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def publish_video_task(self, video_id: int, platforms: list):
    """Publish video to selected platforms asynchronously"""
    db = SessionLocal()
    
    try:
        # Get video
        video = db.query(models.Video).filter(models.Video.id == video_id).first()
        
        if not video:
            raise ValueError(f"Video {video_id} not found")
        
        # Get script for caption
        caption = ""
        if video.script:
            caption = video.script.caption or video.script.hook or ""
        
        results = {}
        
        # Publish to each platform
        for platform in platforms:
            try:
                # Create publication record
                pub = models.Publication(
                    video_id=video_id,
                    platform=platform,
                    status="pending"
                )
                db.add(pub)
                db.commit()
                db.refresh(pub)
                
                # Publish based on platform
                if platform == "telegram":
                    publisher._post_telegram(video.video_path, caption)
                elif platform == "instagram":
                    publisher._post_instagram_reel(video.video_path, caption)
                elif platform == "youtube":
                    publisher._post_youtube_short(video.video_path, caption)
                elif platform == "tiktok":
                    publisher._post_tiktok(video.video_path, caption)
                else:
                    raise ValueError(f"Unknown platform: {platform}")
                
                # Update publication status
                pub.status = "published"
                pub.published_at = datetime.utcnow()
                db.commit()
                
                results[platform] = "success"
                logger.info(f"Published video {video_id} to {platform}")
            
            except Exception as e:
                logger.error(f"Error publishing to {platform}: {e}")
                
                # Update publication with error
                if 'pub' in locals():
                    pub.status = "failed"
                    pub.error_message = str(e)
                    db.commit()
                
                results[platform] = f"error: {str(e)}"
        
        return {
            "video_id": video_id,
            "results": results
        }
    
    finally:
        db.close()

