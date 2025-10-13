"""Scripts CRUD router"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/scripts", tags=["scripts"])


@router.get("/", response_model=List[schemas.Script])
def list_scripts(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all scripts with optional filtering"""
    query = db.query(models.Script)
    
    if status_filter:
        query = query.filter(models.Script.status == status_filter)
    
    scripts = query.order_by(models.Script.created_at.desc()).offset(skip).limit(limit).all()
    return scripts


@router.get("/{script_id}", response_model=schemas.Script)
def get_script(
    script_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get script by ID"""
    script = db.query(models.Script).filter(models.Script.id == script_id).first()
    
    if not script:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")
    
    return script


@router.post("/", response_model=schemas.Script, status_code=status.HTTP_201_CREATED)
def create_script(
    script: schemas.ScriptCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create new script manually"""
    db_script = models.Script(**script.dict())
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    return db_script


@router.put("/{script_id}", response_model=schemas.Script)
def update_script(
    script_id: int,
    script_update: schemas.ScriptUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update existing script"""
    db_script = db.query(models.Script).filter(models.Script.id == script_id).first()
    
    if not db_script:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")
    
    # Update only provided fields
    for key, value in script_update.dict(exclude_unset=True).items():
        setattr(db_script, key, value)
    
    db.commit()
    db.refresh(db_script)
    return db_script


@router.delete("/{script_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_script(
    script_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete script"""
    db_script = db.query(models.Script).filter(models.Script.id == script_id).first()
    
    if not db_script:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")
    
    db.delete(db_script)
    db.commit()
    return None

