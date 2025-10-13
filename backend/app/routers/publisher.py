"""Publisher endpoints for social media publishing"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user
from ..tasks.publish_tasks import publish_video_task

router = APIRouter(prefix="/api/publish", tags=["publisher"])


@router.post("/{video_id}", response_model=schemas.PublishResponse)
def publish_video(
    video_id: int,
    request: schemas.PublishRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Publish video to selected platforms"""
    # Check if video exists
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    
    if video.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video is not ready for publishing"
        )
    
    # Start async publishing task
    task = publish_video_task.delay(video_id, request.platforms)
    
    return {
        "task_id": task.id,
        "message": f"Publishing video {video_id} to {', '.join(request.platforms)}"
    }

