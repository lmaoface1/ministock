from sqlalchemy.orm import Session
from app.models import Sale, Product
from app.schemas import SaleCreate
from fastapi import HTTPException

def create_sale(db: Session, data: SaleCreate):
    product = db.query(Product).filter(Product.id == data.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock_qty < data.qty_sold:
        raise HTTPException(status_code=400, detail="Not enough stock")

    # deduct stock
    product.stock_qty -= data.qty_sold

    sale = Sale(
        product_id=data.product_id,
        qty_sold=data.qty_sold
    )

    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale 