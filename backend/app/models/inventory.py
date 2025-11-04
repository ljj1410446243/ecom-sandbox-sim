# app/models/inventory.py
from typing import Optional
from sqlalchemy import Column, Integer
from sqlmodel import SQLModel, Field


class Inventory(SQLModel, table=True):
    __tablename__ = "inventory"

    id: Optional[int] = Field(default=None, primary_key=True)

    # 外键与索引
    shop_id: int = Field(sa_column=Column("shop_id", Integer, nullable=False, index=True))
    product_id: int = Field(sa_column=Column("product_id", Integer, nullable=False, index=True))

    # 现有可用库存
    on_hand_qty: int = Field(sa_column=Column("on_hand_qty", Integer, nullable=False, default=0))
