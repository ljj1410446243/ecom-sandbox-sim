# app/schemas/inventory.py
from pydantic import BaseModel, Field, ConfigDict


class InventoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    on_hand_qty: int


class InventorySetInput(BaseModel):
    """将库存设置为一个绝对值（不存在则创建）"""
    on_hand_qty: int = Field(ge=0)


class InventoryAdjustInput(BaseModel):
    """增减库存（可正可负），最终不得小于 0"""
    delta: int
