"""Extended models for automation"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Time
from sqlalchemy.sql import func
from .database import Base


class ScheduledPost(Base):
    """Scheduled publication model"""
    __tablename__ = "scheduled_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer)  # Will be filled when video is generated
    script_id = Column(Integer)  # Link to script
    
    # Scheduling
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="pending")  # pending, generated, published, failed
    
    # Platform targets
    publish_to_telegram = Column(Boolean, default=True)
    publish_to_youtube = Column(Boolean, default=True)
    publish_to_tiktok = Column(Boolean, default=True)
    publish_to_instagram = Column(Boolean, default=True)
    
    # Generated content
    caption = Column(Text)
    hashtags = Column(Text)
    
    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    published_at = Column(DateTime(timezone=True))
    error_message = Column(Text)


class AutomationLog(Base):
    """Automation logs for monitoring"""
    __tablename__ = "automation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20))  # INFO, WARNING, ERROR
    message = Column(Text, nullable=False)
    details = Column(Text)
    notified = Column(Boolean, default=False)  # Whether Telegram notification was sent
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Language(Base):
    """Language settings"""
    __tablename__ = "languages"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(5), unique=True)  # ru, en
    name = Column(String(50))
    is_active = Column(Boolean, default=False)
    
    # Language-specific prompts
    system_prompt = Column(Text)
    caption_template = Column(Text)

