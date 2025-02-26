from pydantic import BaseModel, Field
from typing import Optional

# User Schema (for registration)
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username must be between 3 and 50 characters.")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")
    role: Optional[str] = "user"

class UserLogin(BaseModel):  
    username: str
    password: str

# User Response Schema
class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None
    
# Habit Schema
class HabitBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Title must be between 3 and 100 characters.")
    description: str = Field(..., min_length=5, description="Description must be at least 5 characters long.")

class HabitCreate(HabitBase):
    frequency: Optional[str] = Field(default="daily", description="How often the habit is performed (e.g., daily, weekly).")

class HabitUpdate(BaseModel):  
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=5)
    frequency: Optional[str] = Field(None, description="Update the habit frequency.")

class HabitResponse(HabitBase):
    id: int
    user_id: int
    frequency: str

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str
