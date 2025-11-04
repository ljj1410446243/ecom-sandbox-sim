# app/models/inventory.py
from typing import Optional
from sqlalchemy import Column, Integer, UniqueConstraint
from sqlmodel import SQLModel, Field


class Inventory(SQLModel, table=True):
    __tablename__ = "inventory"
    __table_args__ = (UniqueConstraint("product_id", name="uk_inventory_product"),)

    id: Optional[int] = Field(default=None, primary_key=True)

    # 全局库存对应的商品
    product_id: int = Field(sa_column=Column("product_id", Integer, nullable=False, index=True, unique=True))

    # 全局现有可用库存
    on_hand_qty: int = Field(sa_column=Column("on_hand_qty", Integer, nullable=False, default=0))
