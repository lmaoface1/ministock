from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- Product schemas ---

class ProductCreate(BaseModel):
    name: str
    category: str
    stock_qty: int
    cost_per_unit: float

class ProductUpdate(BaseModel):
    stock_qty: int

class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    stock_qty: int
    cost_per_unit: float

    class Config:
        from_attributes = True

# --- Sale schemas ---

class SaleCreate(BaseModel):
    product_id: int
    qty_sold: int

class SaleOut(BaseModel):
    id: int
    product_id: int
    qty_sold: int
    created_at: datetime

    class Config:
        from_attributes = True