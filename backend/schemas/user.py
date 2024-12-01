from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    role: str

class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str