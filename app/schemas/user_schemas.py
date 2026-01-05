from typing import Optional
from pydantic import BaseModel, EmailStr , conint #import for data validation and settings management using python type annotations
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True