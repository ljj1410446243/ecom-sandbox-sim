# app/models/listing.py
from typing import Optional
from enum import Enum
from sqlalchemy import Column, String, Numeric, Integer, Enum as SAEnum
from sqlmodel import SQLModel, Field


class ListingStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class Listing(SQLModel, table=True):
    __tablename__ = "listings"

    id: Optional[int] = Field(default=None, primary_key=True)

    shop_id: int = Field(sa_column=Column("shop_id", Integer, nullable=False, index=True))

    product_id: int = Field(sa_column=Column("product_id", Integer, nullable=False, index=True))

    price: float = Field(sa_column=Column("price", Numeric(12, 2), nullable=False, default=0))

    marketing_budget: float = Field(sa_column=Column("marketing_budget", Numeric(12, 2), nullable=False, default=0))

    status: ListingStatus = Field(
        default=ListingStatus.active,
        sa_column=Column(SAEnum(ListingStatus, name="listing_status_enum"), nullable=False, default="active"),
    )
