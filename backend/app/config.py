"""Application configuration"""
import os
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Load .env file explicitly before Settings initialization
load_dotenv()


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # App
    APP_NAME: str = "AllAboutMe Video Generator"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost/allaboutme")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # JWT Authentication
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-this-secret-key-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # API Keys
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    HEYGEN_API_KEY: Optional[str] = os.getenv("HEYGEN_API_KEY")
    HEYGEN_TEMPLATE_ID: Optional[str] = os.getenv("HEYGEN_TEMPLATE_ID")
    HEYGEN_AVATAR_ID: Optional[str] = os.getenv("HEYGEN_AVATAR_ID")
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    
    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TG_MOD_CHAT_ID: Optional[str] = os.getenv("TG_MOD_CHAT_ID")
    TG_PUBLIC_CHAT_ID: Optional[str] = os.getenv("TG_PUBLIC_CHAT_ID")
    
    # Social Media
    FB_TOKEN: Optional[str] = os.getenv("FB_TOKEN")
    FB_PAGE_ID: Optional[str] = os.getenv("FB_PAGE_ID")
    IG_USER_ID: Optional[str] = os.getenv("IG_USER_ID")
    YOUTUBE_TOKEN: Optional[str] = os.getenv("YOUTUBE_TOKEN")
    TIKTOK_TOKEN: Optional[str] = os.getenv("TIKTOK_TOKEN")
    
    # Storage (use temp dir for local dev, /storage for production)
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", os.path.join(os.path.expanduser("~"), ".allaboutme", "storage"))
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env


settings = Settings()

