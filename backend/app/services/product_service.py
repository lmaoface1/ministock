from sqlalchemy.orm import Session
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException

def create_product(db: Session, data: ProductCreate):
    product = Product(
        name=data.name,
        category=data.category,
        stock_qty=data.stock_qty,
        cost_per_unit=data.cost_per_unit
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def update_stock(db: Session, product_id: int, data: ProductUpdate):
    product = get_product(db, product_id)
    product.stock_qty = data.stock_qty
    db.commit()
    db.refresh(product)
    return product