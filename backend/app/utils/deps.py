from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session, select
from app.core.config import settings
from app.core.db import get_session
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session),
) -> User:
    """
    获取当前认证用户信息

    通过解析JWT令牌获取当前用户的详细信息，并验证用户状态是否有效。

    参数:
        token (str): 从OAuth2密码流中获取的JWT访问令牌，默认通过oauth2_scheme依赖注入
        session (Session): 数据库会话对象，默认通过get_session依赖注入

    返回:
        User: 返回经过验证的用户对象

    异常:
        HTTPException: 当令牌无效、用户不存在或用户状态非活跃时抛出401未授权异常
    """
    # 解析 JWT
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码JWT令牌并提取用户名
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 查询用户并验证用户状态
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or user.status != "active":
        raise credentials_exception
    return user

