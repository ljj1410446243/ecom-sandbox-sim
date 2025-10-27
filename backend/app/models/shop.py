# app/models/shop.py
from typing import Optional
from enum import Enum

from sqlalchemy import Column, String, Enum as SAEnum, Numeric
from sqlmodel import SQLModel, Field


class ShopStatus(str, Enum):
    active = "active"
    closed = "closed"


class Shop(SQLModel, table=True):
    __tablename__ = "shops"  # 与建表 SQL 保持一致

    id: Optional[int] = Field(default=None, primary_key=True)

    owner_user_id: int = Field(nullable=False, index=True)

    name: str = Field(
        sa_column=Column("name", String(100), nullable=False)
    )

    status: ShopStatus = Field(
        default=ShopStatus.active,
        sa_column=Column(SAEnum(ShopStatus, name="shop_status_enum"), nullable=False)
    )

    # DECIMAL(12,2)
    cash_balance: float = Field(
        sa_column=Column("cash_balance", Numeric(12, 2), nullable=False, default=0)
    )
