"""Videos CRUD router"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user
from ..config import settings
from ..auth import decode_access_token

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("/", response_model=List[schemas.Video])
def list_videos(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all videos with optional filtering"""
    query = db.query(models.Video)
    
    if status_filter:
        query = query.filter(models.Video.status == status_filter)
    
    videos = query.order_by(models.Video.created_at.desc()).offset(skip).limit(limit).all()
    return videos


@router.get("/{video_id}", response_model=schemas.Video)
def get_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get video by ID"""
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    
    return video


@router.get("/{video_id}/download")
def download_video(
    video_id: int,
    token: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Download video file - requires token in query string"""
    # Validate token
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token required")
    
    try:
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    
    if not video.video_path or not os.path.exists(video.video_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video file not found")
    
    return FileResponse(
        video.video_path,
        media_type="video/mp4",
        filename=f"video_{video_id}.mp4"
    )


@router.get("/{video_id}/download-audio")
def download_audio(
    video_id: int,
    token: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Download audio file - requires token in query string"""
    # Validate token
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token required")
    
    try:
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    
    if not video.audio_path or not os.path.exists(video.audio_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio file not found")
    
    return FileResponse(
        video.audio_path,
        media_type="audio/mpeg",
        filename=f"audio_{video_id}.mp3"
    )


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete video and associated files"""
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    
    # Delete physical files
    if video.video_path and os.path.exists(video.video_path):
        os.remove(video.video_path)
    
    if video.audio_path and os.path.exists(video.audio_path):
        os.remove(video.audio_path)
    
    # Delete from database
    db.delete(video)
    db.commit()
    return None

