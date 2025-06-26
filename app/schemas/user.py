from pydantic import BaseModel, EmailStr

# Input for signup
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Output schema (what we return after creating a user)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

from typing import Optional

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True  # For Pydantic v2

