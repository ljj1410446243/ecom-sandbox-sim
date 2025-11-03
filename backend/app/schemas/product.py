# app/schemas/product.py
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


class CreateProductInput(BaseModel):
    product_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    category: Optional[str] = Field(default=None, max_length=100)
    base_cost: Decimal = Field(ge=0)


class UpdateProductInput(BaseModel):
    product_code: Optional[str] = Field(default=None, min_length=1, max_length=64)
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    category: Optional[str] = Field(default=None, max_length=100)
    base_cost: Optional[Decimal] = Field(default=None, ge=0)


class ProductOut(BaseModel):
    id: int
    product_code: str
    name: str
    category: Optional[str]
    base_cost: Decimal
