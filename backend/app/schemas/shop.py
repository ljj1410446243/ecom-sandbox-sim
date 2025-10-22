# app/schemas/shop.py
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class CreateShopInput(BaseModel):
    name: str
    initial_balance: Optional[Decimal] = None  # 可选初始资金，默认为 0


class ShopOut(BaseModel):
    id: int
    owner_user_id: int
    name: str
    status: str
    cash_balance: Decimal
