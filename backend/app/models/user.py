# app/models/user.py
from typing import Optional
from enum import Enum

from sqlalchemy import Column, String, Enum as SAEnum
from sqlmodel import SQLModel, Field


class RoleEnum(str, Enum):
    teacher = "teacher"
    student = "student"
    admin = "admin"


class StatusEnum(str, Enum):
    active = "active"
    disabled = "disabled"


class User(SQLModel, table=True):
    __tablename__ = "users"  # 与建表 SQL 对齐

    id: Optional[int] = Field(default=None, primary_key=True)

    # 用 sa_column 明确 Length/Unique/Nullable 等
    username: str = Field(
        sa_column=Column("username", String(50), unique=True, nullable=False, index=True)
    )
    password_hash: str = Field(
        sa_column=Column("password_hash", String(255), nullable=False)
    )
    email: Optional[str] = Field(
        default=None, sa_column=Column("email", String(255), unique=True, nullable=True)
    )
    display_name: str = Field(
        sa_column=Column("display_name", String(100), nullable=False)
    )

    # ✅ 使用真正的 Enum 类型
    role: RoleEnum = Field(
        default=RoleEnum.student,
        sa_column=Column(SAEnum(RoleEnum, name="role_enum"), nullable=False)
    )
    status: StatusEnum = Field(
        default=StatusEnum.active,
        sa_column=Column(SAEnum(StatusEnum, name="status_enum"), nullable=False)
    )
