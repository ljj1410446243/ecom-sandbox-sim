# app/routers/inventory.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.db import get_session
from app.models.inventory import Inventory
from app.models.shop import Shop
from app.models.user import User, RoleEnum
# ↓↓↓ 这里改：不再导入 InventoryCreate
from app.schemas.inventory import InventoryOut, InventorySetInput, InventoryAdjustInput
from app.utils.deps import get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"])


def _assert_owner_or_admin(user: User, shop: Shop):
    if user.role != RoleEnum.admin and shop.owner_user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


def _get_or_404(session: Session, shop_id: int, product_id: int) -> Inventory:
    inv = session.exec(
        select(Inventory).where(Inventory.shop_id == shop_id, Inventory.product_id == product_id)
    ).first()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return inv


@router.get("/{shop_id}/{product_id}", response_model=InventoryOut)
def get_inventory(
    shop_id: int,
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")
    _assert_owner_or_admin(current_user, shop)

    inv = _get_or_404(session, shop_id, product_id)
    return inv


@router.put("/{shop_id}/{product_id}", response_model=InventoryOut)
def set_inventory(
    shop_id: int,
    product_id: int,
    body: InventorySetInput,  # ← 这里用 InventorySetInput
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")
    _assert_owner_or_admin(current_user, shop)

    inv = session.exec(
        select(Inventory).where(Inventory.shop_id == shop_id, Inventory.product_id == product_id)
    ).first()

    if inv is None:
        inv = Inventory(shop_id=shop_id, product_id=product_id, on_hand_qty=body.on_hand_qty)
        session.add(inv)
    else:
        inv.on_hand_qty = body.on_hand_qty

    session.commit()
    session.refresh(inv)
    return inv


@router.patch("/{shop_id}/{product_id}", response_model=InventoryOut)
def adjust_inventory(
    shop_id: int,
    product_id: int,
    body: InventoryAdjustInput,  # ← 这里用 InventoryAdjustInput
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")
    _assert_owner_or_admin(current_user, shop)

    inv = _get_or_404(session, shop_id, product_id)
    new_qty = inv.on_hand_qty + body.delta
    if new_qty < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resulting quantity cannot be negative")

    inv.on_hand_qty = new_qty
    session.add(inv)
    session.commit()
    session.refresh(inv)
    return inv


@router.delete("/{shop_id}/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory(
    shop_id: int,
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    shop = session.get(Shop, shop_id)
    if not shop:
        return  # 幂等

    _assert_owner_or_admin(current_user, shop)

    inv = session.exec(
        select(Inventory).where(Inventory.shop_id == shop_id, Inventory.product_id == product_id)
    ).first()
    if not inv:
        return  # 幂等

    session.delete(inv)
    session.commit()
    return
