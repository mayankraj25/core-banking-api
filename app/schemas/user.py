from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from ..models.user import UserStatus

class UserBase(BaseModel):
    email : EmailStr
    first_name : str
    last_name : str
    phone : Optional[str] = None

class UserCreate(UserBase):
    password : str

class UserUpdate(BaseModel):
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    phone : Optional[str] = None

class UserInDB(UserBase):
    id : int
    status : UserStatus
    is_verified : bool
    created_at : datetime

    class Config:
        from_attribute = True

class UserResponse(UserInDB):
    pass