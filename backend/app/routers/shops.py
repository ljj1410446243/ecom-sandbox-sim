# app/routers/shops.py
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.db import get_session
from app.models.shop import Shop, ShopStatus
from app.models.user import User, RoleEnum
from app.schemas.shop import CreateShopInput, ShopOut
from app.utils.deps import get_current_user

router = APIRouter(prefix="/shops", tags=["shops"])


@router.post("", response_model=ShopOut)
def create_shop(
    body: CreateShopInput,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    创建店铺（默认每个用户只允许一个“active”店铺；如需多店，删除这段检查即可）
    """
    existing = session.exec(
        select(Shop).where(Shop.owner_user_id == current_user.id, Shop.status == ShopStatus.active)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active shop."
        )

    initial_balance: Decimal = body.initial_balance if body.initial_balance is not None else Decimal("0.00")
    shop = Shop(
        owner_user_id=current_user.id,
        name=body.name,
        status=ShopStatus.active,
        cash_balance=float(initial_balance),
    )
    session.add(shop)
    session.commit()
    session.refresh(shop)

    return ShopOut(
        id=shop.id,
        owner_user_id=shop.owner_user_id,
        name=shop.name,
        status=shop.status.value if hasattr(shop.status, "value") else str(shop.status),
        cash_balance=Decimal(str(shop.cash_balance)),
    )


@router.get("/mine", response_model=Optional[ShopOut])
def get_my_shop(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    返回当前用户的 active 店铺；没有则返回 null（前端可据此引导创建）
    """
    shop = session.exec(
        select(Shop).where(Shop.owner_user_id == current_user.id, Shop.status == ShopStatus.active)
    ).first()
    if not shop:
        return None

    return ShopOut(
        id=shop.id,
        owner_user_id=shop.owner_user_id,
        name=shop.name,
        status=shop.status.value if hasattr(shop.status, "value") else str(shop.status),
        cash_balance=Decimal(str(shop.cash_balance)),
    )


@router.get("/{shop_id}", response_model=ShopOut)
def get_shop_by_id(
    shop_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    查看指定店铺：
      - 管理员可看任意店铺
      - 非管理员只能看自己的店铺
    """
    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")

    if current_user.role != RoleEnum.admin and shop.owner_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return ShopOut(
        id=shop.id,
        owner_user_id=shop.owner_user_id,
        name=shop.name,
        status=shop.status.value if hasattr(shop.status, "value") else str(shop.status),
        cash_balance=Decimal(str(shop.cash_balance)),
    )
