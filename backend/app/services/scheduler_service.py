"""Automatic scheduling service"""
import logging
from datetime import datetime, timedelta, time as dt_time
from sqlalchemy.orm import Session
from .. import models
from ..models_extended import ScheduledPost, AutomationLog

logger = logging.getLogger(__name__)


def calculate_schedule(
    db: Session,
    daily_videos: int = 10,
    start_hour: int = 7,
    end_hour: int = 24  # 00:00 = 24
) -> list[datetime]:
    """
    Вычисляет равномерное расписание публикаций
    
    Args:
        daily_videos: Количество видео в день
        start_hour: Начало публикаций (07:00)
        end_hour: Конец публикаций (00:00 = 24)
    
    Returns:
        Список времён публикаций
    """
    today = datetime.now().date()
    
    # Рабочие часы (07:00 - 00:00 = 17 часов)
    working_hours = end_hour - start_hour
    working_minutes = working_hours * 60
    
    # Интервал между публикациями
    interval_minutes = working_minutes / daily_videos
    
    schedule = []
    current_time = datetime.combine(today, dt_time(hour=start_hour))
    
    for i in range(daily_videos):
        schedule.append(current_time)
        current_time += timedelta(minutes=interval_minutes)
    
    return schedule


def create_daily_schedule(db: Session):
    """
    Создаёт расписание на день
    Вызывается автоматически в 00:01 каждый день
    """
    try:
        # Получаем настройки
        daily_videos_setting = db.query(models.Setting).filter(
            models.Setting.key == "daily_videos"
        ).first()
        daily_videos = int(daily_videos_setting.value) if daily_videos_setting else 10
        
        # Вычисляем расписание
        schedule = calculate_schedule(db, daily_videos)
        
        # Создаём записи в БД
        for scheduled_time in schedule:
            scheduled_post = ScheduledPost(
                scheduled_time=scheduled_time,
                status="pending",
                publish_to_telegram=True,
                publish_to_youtube=True,
                publish_to_tiktok=True,
                publish_to_instagram=True
            )
            db.add(scheduled_post)
        
        db.commit()
        
        log_entry = AutomationLog(
            level="INFO",
            message=f"Создано расписание на {len(schedule)} публикаций",
            details=f"First: {schedule[0]}, Last: {schedule[-1]}"
        )
        db.add(log_entry)
        db.commit()
        
        logger.info(f"✅ Schedule created: {len(schedule)} posts")
        return {"created": len(schedule), "schedule": schedule}
    
    except Exception as e:
        logger.error(f"Ошибка создания расписания: {e}")
        
        log_entry = AutomationLog(
            level="ERROR",
            message="Ошибка создания расписания",
            details=str(e),
            notified=False
        )
        db.add(log_entry)
        db.commit()
        
        raise


def get_pending_posts(db: Session) -> list[ScheduledPost]:
    """
    Получить посты, готовые к обработке
    Выбирает посты где:
    - scheduled_time <= now
    - status = "pending"
    """
    now = datetime.now()
    
    return db.query(ScheduledPost).filter(
        ScheduledPost.scheduled_time <= now,
        ScheduledPost.status == "pending"
    ).order_by(ScheduledPost.scheduled_time).all()


def log_automation_error(db: Session, message: str, details: str = None):
    """
    Логирует ошибку автоматизации и отправляет уведомление
    """
    log_entry = AutomationLog(
        level="ERROR",
        message=message,
        details=details,
        notified=False
    )
    db.add(log_entry)
    db.commit()
    
    # Отправить уведомление в Telegram
    try:
        from .telegram_bot import send_error_notification
        import asyncio
        asyncio.run(send_error_notification(f"🚨 Автоматизация:\n{message}\n\n{details or ''}"))
        
        log_entry.notified = True
        db.commit()
    except Exception as e:
        logger.error(f"Не удалось отправить уведомление: {e}")

