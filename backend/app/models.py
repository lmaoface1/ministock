from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(100), nullable=False)
    category       = Column(String(50))
    stock_qty      = Column(Integer, default=0)
    cost_per_unit  = Column(Numeric(10, 2), nullable=False)

    sales           = relationship("Sale", back_populates="product")
    frozen_results  = relationship("FrozenResult", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"

    id          = Column(Integer, primary_key=True, index=True)
    product_id  = Column(Integer, ForeignKey("products.id"), nullable=False)
    qty_sold    = Column(Integer, nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="sales")


class FrozenResult(Base):
    __tablename__ = "frozen_results"

    id           = Column(Integer, primary_key=True, index=True)
    product_id   = Column(Integer, ForeignKey("products.id"), nullable=False)
    is_frozen    = Column(SmallInteger, nullable=False)  # 1 = frozen, 0 = not frozen
    capital_tied = Column(Numeric(10, 2), nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="frozen_results")