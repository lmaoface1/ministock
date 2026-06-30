from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.schemas import SaleCreate, SaleOut
from app.services import sale_service

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/", response_model=SaleOut, status_code=201)
def create_sale(data: SaleCreate, db: Session = Depends(get_db)):
    return sale_service.create_sale(db, data)