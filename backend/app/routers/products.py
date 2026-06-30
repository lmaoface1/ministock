from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.schemas import ProductCreate, ProductUpdate, ProductOut
from app.services import product_service
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, data)

@router.get("/", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, product_id)

@router.patch("/{product_id}/stock", response_model=ProductOut)
def update_stock(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    return product_service.update_stock(db, product_id, data)