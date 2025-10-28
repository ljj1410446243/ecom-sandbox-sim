# app/routers/shops.py
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select

from app.core.db import get_session
from app.models.shop import Shop, ShopStatus
from app.models.user import User, RoleEnum
from app.schemas.shop import CreateShopInput, UpdateShopInput, ShopOut
from app.utils.deps import get_current_user

router = APIRouter(prefix="/shops", tags=["shops"])


def _to_out(s: Shop) -> ShopOut:
    return ShopOut(
        id=s.id,
        owner_user_id=s.owner_user_id,
        name=s.name,
        status=s.status.value if hasattr(s.status, "value") else str(s.status),
        cash_balance=Decimal(str(s.cash_balance)),
    )


def _assert_owner_or_admin(user: User, shop: Shop) -> None:
    if user.role != RoleEnum.admin and shop.owner_user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.post("", response_model=ShopOut)
def create_shop(
    body: CreateShopInput,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    创建店铺：允许一个用户创建多个店铺。
    """
    initial = Decimal("0.00") if body.initial_balance is None else body.initial_balance
    shop = Shop(
        owner_user_id=current_user.id,
        name=body.name,
        status=ShopStatus.active,
        cash_balance=float(initial),
    )
    session.add(shop)
    session.commit()
    session.refresh(shop)
    return _to_out(shop)


@router.get("/mine", response_model=List[ShopOut])
def get_my_shops(
    status: Optional[ShopStatus] = None,  # 可选：按状态过滤
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    查询当前用户的所有店铺列表（可选按状态过滤）。
    """
    stmt = select(Shop).where(Shop.owner_user_id == current_user.id)
    if status is not None:
        stmt = stmt.where(Shop.status == status)
    stmt = stmt.order_by(Shop.id.asc())
    rows = session.exec(stmt).all()
    return [_to_out(s) for s in rows]


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
    _assert_owner_or_admin(current_user, shop)
    return _to_out(shop)


@router.patch("/{shop_id}", response_model=ShopOut)
def update_shop(
    shop_id: int,
    body: UpdateShopInput,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    修改店铺：支持更新 name 与/或 status（active/closed），
    两者至少提供其一。仅管理员或店主可修改。
    """
    if body.name is None and body.status is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")

    _assert_owner_or_admin(current_user, shop)

    if body.name is not None:
        shop.name = body.name

    if body.status is not None:
        # 如需额外业务规则（例如 closed 后不可再 active），可在这里加入校验
        shop.status = body.status

    session.add(shop)
    session.commit()
    session.refresh(shop)
    return _to_out(shop)


@router.delete("/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(
    shop_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    删除店铺（硬删除）：仅管理员或店主可删除。
    注意：后续若有外键关联（listings、inventory、orders 等），
    建议改为“软删除”或添加级联规则。
    """
    shop = session.get(Shop, shop_id)
    if not shop:
        # 幂等：删除不存在资源也返回 204
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    _assert_owner_or_admin(current_user, shop)

    session.delete(shop)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
