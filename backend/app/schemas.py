from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

# Auth
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearers"

class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool
    model_config = {"from_attributes": True}

# Districts
class DistrictResponse(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}

# Students
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    grade_level: int
    district_id: int

class StudentUpdate(BaseModel):
    """all fields optional to support partial updates"""
    first_name:   Optional[str] = None
    last_name:    Optional[str] = None
    grade_level:  Optional[int] = None
    district_id:  Optional[int] = None


class StudentResponse(BaseModel):
    """
    intentionally excludes date_of_birth to minimize data to just what the client needs
    """
    id:           int
    first_name:   str
    last_name:    str
    grade_level:  int
    district_id:  int
    district:     Optional[DistrictResponse] = None
    model_config  = {"from_attributes": True}
