# app/models/product.py
from typing import Optional
from sqlalchemy import Column, String, Numeric, Text
from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)

    # 唯一、可读的商品编码
    product_code: str = Field(sa_column=Column("product_code", String(64), nullable=False, unique=True, index=True))

    name: str = Field(sa_column=Column("name", String(200), nullable=False))

    category: Optional[str] = Field(default=None, sa_column=Column("category", String(100), nullable=True))

    # 采购/基准成本
    base_cost: float = Field(sa_column=Column("base_cost", Numeric(12, 2), nullable=False, default=0))
