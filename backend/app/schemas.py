"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Script schemas
class ScriptBase(BaseModel):
    theme: Optional[str] = None
    script: str
    post_text: Optional[str] = None
    hook: Optional[str] = None
    caption: Optional[str] = None
    status: Optional[str] = "draft"


class ScriptCreate(ScriptBase):
    pass


class ScriptUpdate(BaseModel):
    theme: Optional[str] = None
    script: Optional[str] = None
    post_text: Optional[str] = None
    hook: Optional[str] = None
    caption: Optional[str] = None
    status: Optional[str] = None


class Script(ScriptBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Video schemas
class VideoBase(BaseModel):
    script_id: Optional[int] = None
    video_path: Optional[str] = None
    audio_path: Optional[str] = None
    status: Optional[str] = "pending"
    generator: Optional[str] = None
    duration: Optional[int] = None


class VideoCreate(VideoBase):
    pass


class VideoUpdate(BaseModel):
    video_path: Optional[str] = None
    audio_path: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None


class Video(VideoBase):
    id: int
    error_message: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Publication schemas
class PublicationBase(BaseModel):
    video_id: int
    platform: str
    status: Optional[str] = "pending"


class PublicationCreate(PublicationBase):
    pass


class Publication(PublicationBase):
    id: int
    published_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# Settings schemas
class SettingBase(BaseModel):
    key: str
    value: str


class SettingCreate(SettingBase):
    pass


class Setting(SettingBase):
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SettingsUpdate(BaseModel):
    settings: dict


# Generator schemas
class GenerateScriptsRequest(BaseModel):
    count: Optional[int] = 1


class GeneratePostTextRequest(BaseModel):
    script_id: int


class GenerateVideoRequest(BaseModel):
    script_id: int
    text_position: Optional[str] = "center"  # top, center, bottom
    custom_background: Optional[str] = None  # path to custom background
    voice_id: Optional[str] = None  # ElevenLabs voice ID


class GenerateVideoResponse(BaseModel):
    task_id: str
    message: str


# Publisher schemas
class PublishRequest(BaseModel):
    platforms: List[str]  # ["telegram", "youtube", "tiktok", "instagram"]


class PublishResponse(BaseModel):
    task_id: str
    message: str

