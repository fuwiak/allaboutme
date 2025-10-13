"""Settings endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/")
def get_settings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> Dict[str, str]:
    """Get all settings as key-value dict"""
    settings = db.query(models.Setting).all()
    return {s.key: s.value for s in settings}


@router.put("/")
def update_settings(
    request: schemas.SettingsUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update multiple settings"""
    for key, value in request.settings.items():
        setting = db.query(models.Setting).filter(models.Setting.key == key).first()
        
        if setting:
            setting.value = str(value)
        else:
            setting = models.Setting(key=key, value=str(value))
            db.add(setting)
    
    db.commit()
    
    return {"message": "Settings updated", "count": len(request.settings)}


@router.get("/{key}")
def get_setting(
    key: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get single setting by key"""
    setting = db.query(models.Setting).filter(models.Setting.key == key).first()
    
    if not setting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
    
    return {"key": setting.key, "value": setting.value}

