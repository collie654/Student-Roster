from typing import cast
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..auth import verify_password, create_access_token
from ..schemas import TokenResponse
from .. import models

# creates /auth router endpoint
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
): 
    """
    authenticate a user and return access token
    email -> username
    """
    # look up user by email
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    # using same error for no user found and wrong password so emails can't be enumerated until the correct one is found
    if not user or not verify_password(form_data.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.is_active is False:
        raise HTTPException(status_code=400, detail="Account is disabled")
    
    token = create_access_token(
        user_id=cast(int, user.id),
        email=cast(str, user.email),
        is_admin=cast(bool, user.is_admin),
    )
    return TokenResponse(access_token=token)