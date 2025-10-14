"""Database configuration and session management"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

# Prepare database URL with SSL if needed
database_url = settings.DATABASE_URL

# Railway PostgreSQL requires SSL
if "railway" in database_url.lower() and "sslmode" not in database_url:
    # Add SSL requirement for Railway
    separator = "&" if "?" in database_url else "?"
    database_url = f"{database_url}{separator}sslmode=require"
    print(f"🔒 Added SSL requirement for Railway PostgreSQL")

# Create engine
engine = create_engine(
    database_url,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

