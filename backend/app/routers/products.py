# app/routers/products.py
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.db import get_session
from app.models.product import Product
from app.schemas.product import CreateProductInput, UpdateProductInput, ProductOut
from app.utils.deps import get_current_user  # 任何已登录用户可用；如需只允许admin，后续加校验

router = APIRouter(prefix="/products", tags=["products"])


def _to_out(p: Product) -> ProductOut:
    return ProductOut(
        id=p.id,
        product_code=p.product_code,
        name=p.name,
        category=p.category,
        base_cost=Decimal(str(p.base_cost)),
    )


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    body: CreateProductInput,
    session: Session = Depends(get_session),
    _=Depends(get_current_user),
):
    exists = session.exec(select(Product).where(Product.product_code == body.product_code)).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product_code already exists")

    p = Product(
        product_code=body.product_code,
        name=body.name,
        category=body.category,
        base_cost=float(body.base_cost),
    )
    session.add(p)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product_code already exists")
    session.refresh(p)
    return _to_out(p)


@router.get("", response_model=List[ProductOut])
def list_products(
    q: Optional[str] = Query(default=None, description="按 name 或 product_code 模糊搜索"),
    category: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
    _=Depends(get_current_user),
):
    stmt = select(Product)
    if q:
        like = f"%{q}%"
        stmt = stmt.where((Product.name.ilike(like)) | (Product.product_code.ilike(like)))
    if category:
        stmt = stmt.where(Product.category == category)

    stmt = stmt.order_by(Product.id.desc()).offset((page - 1) * page_size).limit(page_size)
    rows = session.exec(stmt).all()
    return [_to_out(p) for p in rows]


# 获取所有商品（不分页、仅用于管理或测试）
@router.get("/", response_model=List[ProductOut])
def get_all_products(
    session: Session = Depends(get_session),
    _=Depends(get_current_user),
):
    rows = session.exec(select(Product).order_by(Product.id.asc())).all()
    return [
        ProductOut(
            id=p.id,
            product_code=p.product_code,
            name=p.name,
            category=p.category,
            base_cost=p.base_cost,
        )
        for p in rows
    ]

@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    session: Session = Depends(get_session),
    _=Depends(get_current_user),
):
    p = session.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return _to_out(p)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    body: UpdateProductInput,
    session: Session = Depends(get_session),
    _=Depends(get_current_user),
):
    p = session.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if body.product_code and body.product_code != p.product_code:
        exists = session.exec(select(Product).where(Product.product_code == body.product_code)).first()
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product_code already exists")
        p.product_code = body.product_code

    if body.name is not None:
        p.name = body.name
    if body.category is not None:
        p.category = body.category
    if body.base_cost is not None:
        p.base_cost = float(body.base_cost)

    session.add(p)
    session.commit()
    session.refresh(p)
    return _to_out(p)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    _=Depends(get_current_user),
):
    p = session.get(Product, product_id)
    if not p:
        return

    # 注意：若有 listings 关联，DB 外键会阻止删除；这里捕获并提示
    try:
        session.delete(p)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is used by listings and cannot be deleted",
        )
    return


