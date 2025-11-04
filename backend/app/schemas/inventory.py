# app/schemas/inventory.py
from pydantic import BaseModel, Field, ConfigDict

class InventoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # pydantic v2
    id: int
    shop_id: int
    product_id: int
    on_hand_qty: int

class InventorySetInput(BaseModel):
    on_hand_qty: int = Field(ge=0)  # 绝对设置（不存在则创建）

class InventoryAdjustInput(BaseModel):
    delta: int  # 增减（可负），最终不得 < 0
