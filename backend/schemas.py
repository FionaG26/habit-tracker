from pydantic import BaseModel
from typing import Optional

# User Schema (for registration)
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):  
    username: str
    password: str

# User Response Schema
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Habit Schema
class HabitBase(BaseModel):
    title: str
    description: str

class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):  
    name: Optional[str] = None
    description: Optional[str] = None

class HabitResponse(HabitBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

