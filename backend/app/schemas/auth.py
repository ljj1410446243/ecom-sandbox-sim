# app/schemas/auth.py
from typing import Optional
from pydantic import BaseModel, Field

# 简单 email 正则
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class LoginInput(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    display_name: str
    role: str
    status: str
    email: Optional[str] = Field(default=None, pattern=EMAIL_PATTERN)


class RegisterInput(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6, max_length=30)
    display_name: str = Field(min_length=2, max_length=10)
    email: Optional[str] = Field(default=None, pattern=EMAIL_PATTERN)
