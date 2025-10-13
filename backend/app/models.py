"""SQLAlchemy database models"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Script(Base):
    """Script/Scenario model"""
    __tablename__ = "scripts"
    
    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String(100))
    script = Column(Text, nullable=False)
    post_text = Column(Text)  # Clean text for voiceover
    hook = Column(String(200))
    caption = Column(Text)
    status = Column(String(20), default="draft")  # draft, approved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    videos = relationship("Video", back_populates="script", cascade="all, delete-orphan")


class Video(Base):
    """Generated video model"""
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    script_id = Column(Integer, ForeignKey("scripts.id"), nullable=True)
    video_path = Column(String(500))
    audio_path = Column(String(500))
    status = Column(String(20), default="pending")  # pending, completed, failed
    generator = Column(String(20))  # heygen, opensource
    duration = Column(Integer)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    script = relationship("Script", back_populates="videos")
    publications = relationship("Publication", back_populates="video", cascade="all, delete-orphan")


class Publication(Base):
    """Publication tracking model"""
    __tablename__ = "publications"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    platform = Column(String(20), nullable=False)  # telegram, youtube, tiktok, instagram
    status = Column(String(20), default="pending")  # pending, published, failed
    published_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    
    # Relationships
    video = relationship("Video", back_populates="publications")


class Setting(Base):
    """Settings key-value store"""
    __tablename__ = "settings"
    
    key = Column(String(100), primary_key=True)
    value = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

