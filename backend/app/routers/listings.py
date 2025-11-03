# app/routers/listings.py
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.db import get_session
from app.models.listing import Listing, ListingStatus
from app.models.product import Product
from app.models.shop import Shop
from app.models.user import User, RoleEnum
from app.schemas.listing import CreateListingInput, UpdateListingInput, ListingOut
from app.utils.deps import get_current_user

router = APIRouter(prefix="/listings", tags=["listings"])


def _assert_owner_or_admin(current_user: User, shop: Shop):
    if current_user.role != RoleEnum.admin and shop.owner_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


def _to_out(x: Listing) -> ListingOut:
    return ListingOut(
        id=x.id,
        shop_id=x.shop_id,
        product_id=x.product_id,
        price=Decimal(str(x.price)),
        marketing_budget=Decimal(str(x.marketing_budget)),
        status=x.status.value if hasattr(x.status, "value") else str(x.status),
    )


@router.post("", response_model=ListingOut, status_code=status.HTTP_201_CREATED)
def create_listing(
    body: CreateListingInput,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    shop = session.get(Shop, body.shop_id)
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")
    _assert_owner_or_admin(current_user, shop)

    product = session.get(Product, body.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # 唯一约束：同店同商品只能一条
    exists = session.exec(
        select(Listing).where(Listing.shop_id == body.shop_id, Listing.product_id == body.product_id)
    ).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This product is already listed in this shop")

    x = Listing(
        shop_id=body.shop_id,
        product_id=body.product_id,
        price=float(body.price),
        marketing_budget=float(body.marketing_budget),
        status=body.status or ListingStatus.active,
    )
    session.add(x)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate listing")
    session.refresh(x)
    return _to_out(x)


@router.get("", response_model=List[ListingOut])
def list_listings(
    shop_id: Optional[int] = Query(default=None),
    product_id: Optional[int] = Query(default=None),
    status: Optional[ListingStatus] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Listing)

    if current_user.role != RoleEnum.admin:
        user_shop_ids = [s.id for s in session.exec(select(Shop.id).where(Shop.owner_user_id == current_user.id)).all()]
        if not user_shop_ids:
            return []
        stmt = stmt.where(Listing.shop_id.in_(user_shop_ids))

    if shop_id is not None:
        stmt = stmt.where(Listing.shop_id == shop_id)
    if product_id is not None:
        stmt = stmt.where(Listing.product_id == product_id)
    if status is not None:
        stmt = stmt.where(Listing.status == status)

    stmt = stmt.order_by(Listing.id.desc()).offset((page - 1) * page_size).limit(page_size)
    rows = session.exec(stmt).all()
    return [_to_out(x) for x in rows]


@router.get("/{listing_id}", response_model=ListingOut)
def get_listing(
    listing_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    x = session.get(Listing, listing_id)
    if not x:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    shop = session.get(Shop, x.shop_id)
    _assert_owner_or_admin(current_user, shop)
    return _to_out(x)


@router.patch("/{listing_id}", response_model=ListingOut)
def update_listing(
    listing_id: int,
    body: UpdateListingInput,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    x = session.get(Listing, listing_id)
    if not x:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    shop = session.get(Shop, x.shop_id)
    _assert_owner_or_admin(current_user, shop)

    if body.price is not None:
        x.price = float(body.price)
    if body.marketing_budget is not None:
        x.marketing_budget = float(body.marketing_budget)
    if body.status is not None:
        x.status = body.status

    session.add(x)
    session.commit()
    session.refresh(x)
    return _to_out(x)


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(
    listing_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    x = session.get(Listing, listing_id)
    if not x:
        return

    shop = session.get(Shop, x.shop_id)
    _assert_owner_or_admin(current_user, shop)

    session.delete(x)
    session.commit()
    return
