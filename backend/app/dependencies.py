"""FastAPI dependencies"""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from .database import get_db
from . import models, auth
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> models.User:
    """Get current authenticated user from JWT token"""
    
    # Get Authorization header from request
    authorization = request.headers.get('Authorization') or request.headers.get('authorization')
    
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Authorization header: {authorization[:50] if authorization else 'NONE'}")
    
    # Extract token from Authorization header
    if not authorization:
        logger.error("No Authorization header found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Remove 'Bearer ' prefix
    token = authorization.replace('Bearer ', '').strip() if authorization.startswith('Bearer ') else authorization
    
    logger.info(f"Validating token: {token[:20]}...")
    
    username = auth.decode_access_token(token)
    
    if username is None:
        logger.error("Invalid token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(models.User).filter(models.User.username == username).first()
    
    if user is None:
        logger.error(f"User not found: {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"Auth successful for user: {username}")
    return user

