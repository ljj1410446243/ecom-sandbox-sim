# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.db import get_session
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import Token, UserOut, LoginInput
from app.utils.deps import get_current_user  # 用于 /auth/me

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    body: LoginInput,  # ✅ 现在接收 JSON：{ "username": "...", "password": "..." }
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.username == body.username)).first()
    if not user or user.status != "active" or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    token = create_access_token(subject=user.username)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return UserOut(
        id=current_user.id,
        username=current_user.username,
        display_name=current_user.display_name,
        role=current_user.role,
        status=current_user.status,
        email=current_user.email,
    )
