"""Celery tasks for automation"""
import logging
from datetime import datetime
from celery import group
from celery.schedules import crontab
from .celery_app import celery_app
from ..database import SessionLocal
from ..models_extended import ScheduledPost, AutomationLog
from ..services import scheduler_service
from .video_tasks import generate_scripts_task, generate_video_task
from .publish_tasks import publish_video_task

logger = logging.getLogger(__name__)


@celery_app.task
def create_daily_schedule_task():
    """
    Создание расписания на день
    Запускается в 00:01 каждый день
    """
    db = SessionLocal()
    try:
        result = scheduler_service.create_daily_schedule(db)
        logger.info(f"Daily schedule created: {result}")
        return result
    except Exception as e:
        logger.error(f"Error creating daily schedule: {e}")
        scheduler_service.log_automation_error(
            db,
            "Ошибка создания расписания",
            str(e)
        )
        raise
    finally:
        db.close()


@celery_app.task
def process_pending_posts_task():
    """
    Обработка pending постов
    Запускается каждые 5 минут
    
    Для каждого поста:
    1. Генерирует script (если нет)
    2. Генерирует video (если нет)
    3. Публикует (когда готово)
    """
    db = SessionLocal()
    try:
        pending_posts = scheduler_service.get_pending_posts(db)
        
        if not pending_posts:
            logger.info("No pending posts to process")
            return {"processed": 0}
        
        logger.info(f"Processing {len(pending_posts)} pending posts...")
        
        for post in pending_posts:
            try:
                # 1. Generate script if not exists
                if not post.script_id:
                    logger.info(f"Generating script for post {post.id}")
                    result = generate_scripts_task.delay(1)
                    # Mark as in progress
                    post.status = "generating_script"
                    db.commit()
                    continue
                
                # 2. Generate video if not exists
                if not post.video_id:
                    logger.info(f"Generating video for post {post.id}, script {post.script_id}")
                    result = generate_video_task.delay(post.script_id)
                    post.status = "generating_video"
                    db.commit()
                    continue
                
                # 3. Publish video
                logger.info(f"Publishing video {post.video_id} for post {post.id}")
                platforms = []
                if post.publish_to_telegram:
                    platforms.append("telegram")
                if post.publish_to_youtube:
                    platforms.append("youtube")
                if post.publish_to_tiktok:
                    platforms.append("tiktok")
                if post.publish_to_instagram:
                    platforms.append("instagram")
                
                if platforms:
                    publish_video_task.delay(post.video_id, platforms)
                    post.status = "published"
                    post.published_at = datetime.utcnow()
                    db.commit()
                    logger.info(f"Post {post.id} published to {', '.join(platforms)}")
            
            except Exception as e:
                logger.error(f"Error processing post {post.id}: {e}")
                post.status = "failed"
                post.error_message = str(e)
                db.commit()
                
                scheduler_service.log_automation_error(
                    db,
                    f"Ошибка обработки поста {post.id}",
                    str(e)
                )
        
        return {"processed": len(pending_posts)}
    
    finally:
        db.close()


@celery_app.task
def check_and_notify_errors_task():
    """
    Проверяет unnotified errors и отправляет уведомления
    Запускается каждый час
    """
    db = SessionLocal()
    try:
        unnotified_errors = db.query(AutomationLog).filter(
            AutomationLog.level == "ERROR",
            AutomationLog.notified == False
        ).limit(10).all()
        
        if not unnotified_errors:
            return {"notified": 0}
        
        # Группируем ошибки и отправляем одним сообщением
        error_messages = []
        for log in unnotified_errors:
            error_messages.append(f"• {log.message}")
            if log.details:
                error_messages.append(f"  └─ {log.details[:200]}")
        
        # Отправить в Telegram
        try:
            from ..services.telegram_bot import send_error_notification
            import asyncio
            
            notification = f"🚨 Ошибки автоматизации ({len(unnotified_errors)}):\n\n" + "\n".join(error_messages[:10])
            asyncio.run(send_error_notification(notification))
            
            # Пометить как отправленные
            for log in unnotified_errors:
                log.notified = True
            db.commit()
            
            logger.info(f"Sent {len(unnotified_errors)} error notifications")
            return {"notified": len(unnotified_errors)}
        
        except Exception as e:
            logger.error(f"Failed to send notifications: {e}")
            return {"notified": 0, "error": str(e)}
    
    finally:
        db.close()


# Configure Celery Beat schedule
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Setup periodic tasks for automation"""
    
    # Create daily schedule at 00:01
    sender.add_periodic_task(
        crontab(hour=0, minute=1),
        create_daily_schedule_task.s(),
        name='create-daily-schedule'
    )
    
    # Process pending posts every 5 minutes
    sender.add_periodic_task(
        60.0 * 5,  # 5 minutes
        process_pending_posts_task.s(),
        name='process-pending-posts'
    )
    
    # Check and notify errors every hour
    sender.add_periodic_task(
        60.0 * 60,  # 1 hour
        check_and_notify_errors_task.s(),
        name='check-notify-errors'
    )

