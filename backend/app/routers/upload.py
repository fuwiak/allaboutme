"""File upload endpoints"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
import os
import shutil
from pathlib import Path
from .. import models
from ..database import get_db
from ..dependencies import get_current_user
from ..storage import BACKGROUNDS_DIR, init_storage

router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.post("/background")
async def upload_background(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Upload custom background image for videos"""
    
    # Import storage functions
    from ..storage import init_storage, BACKGROUNDS_DIR as bg_dir
    
    # Ensure storage is initialized
    init_storage()
    from ..storage import BACKGROUNDS_DIR
    
    if BACKGROUNDS_DIR is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Storage not initialized"
        )
    
    # Validate file type
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Generate unique filename
    filename = f"custom_{current_user.id}_{file.filename}"
    file_path = BACKGROUNDS_DIR / filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Save to settings
        setting = db.query(models.Setting).filter(
            models.Setting.key == "custom_background_path"
        ).first()
        
        if setting:
            setting.value = str(file_path)
        else:
            setting = models.Setting(
                key="custom_background_path",
                value=str(file_path)
            )
            db.add(setting)
        
        db.commit()
        
        return {
            "filename": filename,
            "path": str(file_path),
            "size": os.path.getsize(file_path),
            "message": "Background uploaded successfully"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )


@router.get("/backgrounds")
async def list_backgrounds(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """List all uploaded background images"""
    
    if BACKGROUNDS_DIR is None or not BACKGROUNDS_DIR.exists():
        return {"backgrounds": []}
    
    backgrounds = []
    for file_path in BACKGROUNDS_DIR.glob("*"):
        if file_path.is_file():
            backgrounds.append({
                "filename": file_path.name,
                "path": str(file_path),
                "size": file_path.stat().st_size
            })
    
    return {"backgrounds": backgrounds}

