"""Generator endpoints for async script/video generation"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user
from ..tasks.video_tasks import generate_scripts_task, generate_post_text_task, generate_video_task
from ..services import generator

router = APIRouter(prefix="/api/generate", tags=["generator"])


@router.post("/scripts", response_model=schemas.GenerateVideoResponse)
def generate_scripts(
    request: schemas.GenerateScriptsRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Generate new scripts asynchronously"""
    task = generate_scripts_task.delay(request.count)
    
    return {
        "task_id": task.id,
        "message": f"Generating {request.count} script(s)"
    }


@router.post("/post-text/{script_id}")
def generate_post_text(
    script_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Generate clean post text from script"""
    # Check if script exists
    script = db.query(models.Script).filter(models.Script.id == script_id).first()
    
    if not script:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")
    
    # Generate synchronously (fast operation)
    try:
        post_text = generator.generate_clean_post(script.script, script.theme, db)
        
        # Update script
        script.post_text = post_text
        db.commit()
        
        return {"script_id": script_id, "post_text": post_text}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating post text: {str(e)}"
        )


@router.post("/video", response_model=schemas.GenerateVideoResponse)
def generate_video(
    request: schemas.GenerateVideoRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Generate video from script asynchronously"""
    # Check if script exists
    script = db.query(models.Script).filter(models.Script.id == request.script_id).first()
    
    if not script:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")
    
    # Start async task with all settings
    task = generate_video_task.delay(
        request.script_id,
        request.text_position,
        request.custom_background,
        request.voice_id
    )
    
    return {
        "task_id": task.id,
        "message": f"Generating video for script {request.script_id} with voice {request.voice_id or 'default'}"
    }

