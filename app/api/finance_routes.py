from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FinancialData, PostData
from app.schemas import FinancialDataCreate, FinancialDataResponse, PostCreate, PostResponse, PostUpdate

router = APIRouter()

# FinancialData Routes
@router.post("/financial_data/", response_model=FinancialDataResponse)
def create_financial_data(data: FinancialDataCreate, db: Session = Depends(get_db)):
    new_data = FinancialData(**data.dict())
    print("Here")
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


@router.get("/financial_data/{data_id}", response_model=FinancialDataResponse)
def get_financial_data(data_id: int, db: Session = Depends(get_db)):
    data = db.query(FinancialData).filter(FinancialData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Financial data not found")
    return data


@router.get("/financial_data/", response_model=list[FinancialDataResponse])
def list_financial_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(FinancialData).offset(skip).limit(limit).all()
