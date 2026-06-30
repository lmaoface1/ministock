from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.deps import get_db
from app.schemas import FrozenResultOut
from app.services import frozen_service

router = APIRouter(prefix="/analytics/frozen-capital", tags=["Frozen Capital"])

@router.post("/run", response_model=List[FrozenResultOut])
def run_analysis(db: Session = Depends(get_db)):
    return frozen_service.run_frozen_capital_analysis(db)

@router.get("/", response_model=List[FrozenResultOut])
def latest_results(db: Session = Depends(get_db)):
    return frozen_service.get_latest_results(db)