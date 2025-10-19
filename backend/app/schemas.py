from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from .models import UserRole

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: Optional[str]

    class Config:
        orm_mode = True  # Important! Allows SQLAlchemy models to be converted to Pydantic


# Response model for login endpoint
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Role Enum must match the database model
class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"
    client = "client"


# Base schema shared by create & response schemas
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: UserRole = UserRole.client


# Schema used when creating a user (includes password)
class UserCreate(UserBase):
    password: str


# Schema returned in API responses (hides password)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True  # Allows conversion from SQLAlchemy models
