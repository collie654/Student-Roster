from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import SessionLocal
from .auth import decode_token
from . import models

# tells FastAPI where to find the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

def get_db():
    """
    yields database session for a request then ensures it's closed
    """
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
) -> models.User:
    """
    gets token and db session then validates the token. if valid it returns user, else it returns 401
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub", ""))
    except (ValueError, TypeError):
        raise credentials_exception
    
    user = db.get(models.User, user_id)
    if user is None or user.is_active is False:
        raise credentials_exception
    return user

def require_admin(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    gets current user and determines if they have admin role, if so returns current user, else returns 403
    """
    if current_user.is_admin is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user