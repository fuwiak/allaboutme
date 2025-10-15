"""Celery tasks for video generation"""
import logging
import json
import redis
from sqlalchemy.orm import Session
from .celery_app import celery_app
from ..database import SessionLocal
from .. import models
from ..services import generator, renderer
from ..storage import get_video_path, get_audio_path
from ..config import settings

logger = logging.getLogger(__name__)

# Redis client for progress updates
redis_client = redis.from_url(settings.REDIS_URL)


@celery_app.task(bind=True)
def generate_scripts_task(self, count: int = 1):
    """Generate scripts asynchronously"""
    db = SessionLocal()
    try:
        # Publish start status
        redis_client.publish(
            f"progress:{self.request.id}",
            json.dumps({"status": "Generating scripts...", "elapsed": 0, "task_id": self.request.id})
        )
        
        scripts_data = generator.generate_scripts(db, count)
        
        # Save to database
        script_ids = []
        for i, script_data in enumerate(scripts_data):
            # Publish progress
            redis_client.publish(
                f"progress:{self.request.id}",
                json.dumps({
                    "status": f"Saving script {i+1}/{len(scripts_data)}...",
                    "elapsed": i * 0.5,
                    "task_id": self.request.id
                })
            )
            
            db_script = models.Script(
                theme=script_data["theme"],
                script=script_data["script"],
                hook=script_data["hook"],
                caption=script_data["caption"],
                status="draft"
            )
            db.add(db_script)
            db.commit()
            db.refresh(db_script)
            script_ids.append(db_script.id)
        
        # Publish completion
        redis_client.publish(
            f"progress:{self.request.id}",
            json.dumps({
                "status": "completed",
                "elapsed": len(scripts_data) * 0.5,
                "task_id": self.request.id,
                "script_ids": script_ids
            })
        )
        
        return {"script_ids": script_ids, "count": len(script_ids)}
    
    finally:
        db.close()


@celery_app.task(bind=True)
def generate_post_text_task(self, script_id: int):
    """Generate clean post text from script"""
    db = SessionLocal()
    try:
        script = db.query(models.Script).filter(models.Script.id == script_id).first()
        
        if not script:
            raise ValueError(f"Script {script_id} not found")
        
        # Generate clean text
        post_text = generator.generate_clean_post(script.script, script.theme, db)
        
        # Update script
        script.post_text = post_text
        db.commit()
        
        return {"script_id": script_id, "post_text": post_text}
    
    finally:
        db.close()


@celery_app.task(bind=True)
def generate_video_task(self, script_id: int, text_position: str = "center", custom_background: str = None, voice_id: str = None):
    """Generate video from script asynchronously with custom settings"""
    db = SessionLocal()
    
    logger.info(f"Generating video for script {script_id} with settings: position={text_position}, voice={voice_id}, bg={custom_background is not None}")
    
    try:
        # Get script
        script = db.query(models.Script).filter(models.Script.id == script_id).first()
        
        if not script:
            raise ValueError(f"Script {script_id} not found")
        
        # Create video record
        video = models.Video(
            script_id=script_id,
            status="pending"
        )
        db.add(video)
        db.commit()
        db.refresh(video)
        
        video_id = video.id
        
        # Progress callback
        def progress_callback(status, elapsed):
            # Publish progress to Redis
            progress_data = {
                "video_id": video_id,
                "status": status,
                "elapsed": elapsed,
                "task_id": self.request.id
            }
            redis_client.publish(
                f"progress:{self.request.id}",
                json.dumps(progress_data)
            )
        
        # Use post_text if available, otherwise use script
        text_for_video = script.post_text if script.post_text else script.script
        
        # Generate video
        try:
            # Determine generator from settings
            generator_type = db.query(models.Setting).filter(
                models.Setting.key == "video_generator"
            ).first()
            
            use_opensource = generator_type and generator_type.value == "opensource"
            
            if use_opensource:
                from ..services.opensource_video import render_video_opensource
                video_url, audio_url = render_video_opensource(
                    text_for_video,
                    progress_callback=progress_callback,
                    text_position=text_position,
                    custom_background=custom_background,
                    voice_id=voice_id
                )
                video.generator = "opensource"
            else:
                from ..services.renderer import render_video
                video_url = render_video(
                    text_for_video, 
                    progress_callback=progress_callback,
                    text_position=text_position,
                    custom_background=custom_background,
                    voice_id=voice_id
                )
                audio_url = None  # HeyGen doesn't provide separate audio
                video.generator = "heygen"
            
            # Save file paths
            video.video_path = video_url
            video.audio_path = audio_url
            video.status = "completed"
            db.commit()
            
            # Send Telegram notification
            try:
                from ..services.telegram_bot import send_video_notification
                import asyncio
                asyncio.run(send_video_notification(
                    video_url,
                    script.caption or script.hook,
                    script.script
                ))
            except Exception as e:
                logger.error(f"Error sending Telegram notification: {e}")
            
            return {
                "video_id": video_id,
                "video_url": video_url,
                "audio_url": audio_url,
                "status": "completed"
            }
        
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            video.status = "failed"
            video.error_message = str(e)
            db.commit()
            raise
    
    finally:
        db.close()

