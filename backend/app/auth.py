from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# bycrypt password hasing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    """hash plain text password, store only the hash."""
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """compare plain password against stored hash, returns true if matched"""
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: int, email: str, is_admin: bool) -> str:
    """create a signed JWT token"""
    secret_key = os.environ["SECRET_KEY"]
    expire_minutes = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    payload ={
        "sub": str(user_id), # subject of the token
        "email": email,
        "is_admin": is_admin,
        "iat": datetime.now(timezone.utc), # issued at time
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

def decode_token(token: str) -> dict:
    """decode and verify JWT"""
    secret_key = os.environ["SECRET_KEY"]
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}")