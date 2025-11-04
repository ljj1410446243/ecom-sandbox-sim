# app/routers/inventory.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.core.db import get_session
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.user import User, RoleEnum
from app.schemas.inventory import InventoryOut, InventorySetInput, InventoryAdjustInput
from app.utils.deps import get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"])


def _admin_only(user: User):
    if user.role != RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")


def _get_by_product_or_404(session: Session, product_id: int) -> Inventory:
    inv = session.exec(select(Inventory).where(Inventory.product_id == product_id)).first()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return inv


@router.get("", response_model=List[InventoryOut])
def list_inventory(
    q: Optional[str] = Query(default=None, description="按 product_code 或 name 模糊搜索"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    session: Session = Depends(get_session),
    _user: User = Depends(get_current_user),
):
    # 先选出符合条件的产品ID（若 q 为空则不限定）
    if q:
        like = f"%{q}%"
        p_stmt = select(Product.id).where(
            (Product.product_code.ilike(like)) | (Product.name.ilike(like))
        )
        # 注意：这里直接就是 List[int]
        product_ids: List[int] = session.exec(p_stmt).all()
        if not product_ids:
            return []
        i_stmt = select(Inventory).where(Inventory.product_id.in_(product_ids))
    else:
        i_stmt = select(Inventory)

    i_stmt = (
        i_stmt.order_by(Inventory.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    rows = session.exec(i_stmt).all()
    return rows


@router.get("/{product_id}", response_model=InventoryOut)
def get_inventory(
    product_id: int,
    session: Session = Depends(get_session),
    _user: User = Depends(get_current_user),
):
    inv = _get_by_product_or_404(session, product_id)
    return inv


@router.put("/{product_id}", response_model=InventoryOut)
def set_inventory(
    product_id: int,
    body: InventorySetInput,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    _admin_only(user)

    # 保证商品存在（可选但推荐）
    if not session.get(Product, product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    inv = session.exec(select(Inventory).where(Inventory.product_id == product_id)).first()
    if inv is None:
        inv = Inventory(product_id=product_id, on_hand_qty=body.on_hand_qty)
        session.add(inv)
    else:
        inv.on_hand_qty = body.on_hand_qty

    session.commit()
    session.refresh(inv)
    return inv


@router.patch("/{product_id}", response_model=InventoryOut)
def adjust_inventory(
    product_id: int,
    body: InventoryAdjustInput,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    _admin_only(user)

    inv = _get_by_product_or_404(session, product_id)
    new_qty = inv.on_hand_qty + body.delta
    if new_qty < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resulting quantity cannot be negative")

    inv.on_hand_qty = new_qty
    session.add(inv)
    session.commit()
    session.refresh(inv)
    return inv


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory(
    product_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    _admin_only(user)

    inv = session.exec(select(Inventory).where(Inventory.product_id == product_id)).first()
    if not inv:
        return  # 幂等
    session.delete(inv)
    session.commit()
    return
