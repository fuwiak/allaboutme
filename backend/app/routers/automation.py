"""Automation control endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from .. import models
from ..models_extended import ScheduledPost, AutomationLog, Language
from ..database import get_db
from ..dependencies import get_current_user
from ..services import scheduler_service
from ..tasks.automation_tasks import create_daily_schedule_task, process_pending_posts_task

router = APIRouter(prefix="/api/automation", tags=["automation"])


@router.post("/schedule/create")
def create_schedule(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create today's publishing schedule"""
    result = scheduler_service.create_daily_schedule(db)
    return result


@router.get("/schedule")
def get_schedule(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all scheduled posts"""
    posts = db.query(ScheduledPost).order_by(ScheduledPost.scheduled_time).all()
    return {"schedule": [
        {
            "id": p.id,
            "scheduled_time": p.scheduled_time,
            "status": p.status,
            "video_id": p.video_id,
            "script_id": p.script_id
        } for p in posts
    ]}


@router.post("/enable")
def enable_automation(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Enable automatic mode"""
    setting = db.query(models.Setting).filter(models.Setting.key == "automation_enabled").first()
    
    if setting:
        setting.value = "true"
    else:
        setting = models.Setting(key="automation_enabled", value="true")
        db.add(setting)
    
    db.commit()
    
    # Trigger schedule creation
    create_daily_schedule_task.delay()
    
    return {"message": "Automation enabled", "status": "active"}


@router.post("/disable")
def disable_automation(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Disable automatic mode"""
    setting = db.query(models.Setting).filter(models.Setting.key == "automation_enabled").first()
    
    if setting:
        setting.value = "false"
    else:
        setting = models.Setting(key="automation_enabled", value="false")
        db.add(setting)
    
    db.commit()
    
    return {"message": "Automation disabled", "status": "inactive"}


@router.get("/logs")
def get_automation_logs(
    limit: int = 50,
    level: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get automation logs"""
    query = db.query(AutomationLog)
    
    if level:
        query = query.filter(AutomationLog.level == level)
    
    logs = query.order_by(AutomationLog.created_at.desc()).limit(limit).all()
    
    return {"logs": [
        {
            "id": log.id,
            "level": log.level,
            "message": log.message,
            "details": log.details,
            "created_at": log.created_at,
            "notified": log.notified
        } for log in logs
    ]}


@router.get("/status")
def get_automation_status(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get current automation status"""
    enabled_setting = db.query(models.Setting).filter(
        models.Setting.key == "automation_enabled"
    ).first()
    
    is_enabled = enabled_setting and enabled_setting.value == "true"
    
    # Count pending posts
    pending_count = db.query(ScheduledPost).filter(
        ScheduledPost.status == "pending"
    ).count()
    
    # Count today's published
    today_start = datetime.now().replace(hour=0, minute=0, second=0)
    published_today = db.query(ScheduledPost).filter(
        ScheduledPost.published_at >= today_start,
        ScheduledPost.status == "published"
    ).count()
    
    return {
        "enabled": is_enabled,
        "pending_posts": pending_count,
        "published_today": published_today
    }


@router.post("/languages/{code}/activate")
def activate_language(
    code: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Activate a language (ru or en)"""
    # Deactivate all
    db.query(Language).update({"is_active": False})
    
    # Activate selected
    lang = db.query(Language).filter(Language.code == code).first()
    
    if not lang:
        # Create if doesn't exist
        lang = Language(
            code=code,
            name="Russian" if code == "ru" else "English",
            is_active=True
        )
        db.add(lang)
    else:
        lang.is_active = True
    
    db.commit()
    
    return {"language": code, "status": "activated"}


@router.get("/languages")
def list_languages(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """List all languages"""
    languages = db.query(Language).all()
    
    # Ensure ru and en exist
    if not languages:
        ru = Language(code="ru", name="Русский", is_active=True)
        en = Language(code="en", name="English", is_active=False)
        db.add_all([ru, en])
        db.commit()
        languages = [ru, en]
    
    return {"languages": [
        {"code": l.code, "name": l.name, "is_active": l.is_active}
        for l in languages
    ]}

