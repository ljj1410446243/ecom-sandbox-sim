# app/schemas/shop.py
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from app.models.shop import ShopStatus


class CreateShopInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    initial_balance: Optional[Decimal] = None  # 可选初始资金，默认为 0


class UpdateShopInput(BaseModel):
    # 两者至少提供其一；在路由中做“至少一个字段”校验
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    status: Optional[ShopStatus] = None


class ShopOut(BaseModel):
    id: int
    owner_user_id: int
    name: str
    status: str
    cash_balance: Decimal
