from typing import Optional
from pydantic import BaseModel


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
    email: Optional[str] = None
