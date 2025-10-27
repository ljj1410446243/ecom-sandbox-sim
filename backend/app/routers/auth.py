# app/routers/auth.py
from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.db import get_session
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.user import User, RoleEnum, StatusEnum
from app.schemas.auth import Token, UserOut, LoginInput, RegisterInput
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

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
    body: RegisterInput,
    session: Session = Depends(get_session),
):
    # 显式唯一性检查（避免直接撞库抛 500）
    existed = session.exec(select(User).where(User.username == body.username)).first()
    if existed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    if body.email:
        existed_email = session.exec(select(User).where(User.email == body.email)).first()
        if existed_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user = User(
        username=body.username,
        display_name=body.display_name,
        email=body.email,
        role=RoleEnum.student,          # 默认学生角色
        status=StatusEnum.active,       # 默认激活
        password_hash=get_password_hash(body.password),
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        # 双重保险：数据库层唯一约束冲突
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")

    session.refresh(user)
    return UserOut(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        role=user.role.value if hasattr(user.role, "value") else str(user.role),
        status=user.status.value if hasattr(user.status, "value") else str(user.status),
        email=user.email,
    )

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return UserOut(
        id=current_user.id,
        username=current_user.username,
        display_name=current_user.display_name,
        role=current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role),
        status=current_user.status.value if hasattr(current_user.status, "value") else str(current_user.status),
        email=current_user.email,
    )
