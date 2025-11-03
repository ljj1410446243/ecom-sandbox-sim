# app/schemas/listing.py
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.listing import ListingStatus


class CreateListingInput(BaseModel):
    shop_id: int
    product_id: int
    price: Decimal = Field(ge=0)
    marketing_budget: Decimal = Field(ge=0)
    status: Optional[ListingStatus] = ListingStatus.active


class UpdateListingInput(BaseModel):
    price: Optional[Decimal] = Field(default=None, ge=0)
    marketing_budget: Optional[Decimal] = Field(default=None, ge=0)
    status: Optional[ListingStatus] = None


class ListingOut(BaseModel):
    id: int
    shop_id: int
    product_id: int
    price: Decimal
    marketing_budget: Decimal
    status: str
