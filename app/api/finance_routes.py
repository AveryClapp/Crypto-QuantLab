from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FinancialData, PostData
from app.schemas import FinancialDataCreate, FinancialDataResponse, PostCreate, PostResponse, PostUpdate

router = APIRouter()
db = next(get_db())
# FinancialData Routes
@router.post("/financial_data/", response_model=FinancialDataResponse)
def create_financial_data(data: FinancialDataCreate): 
    new_data = FinancialData(**data.dict())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


@router.get("/financial_data/{limit}", response_model=list[FinancialDataResponse])
def list_financial_data(skip: int, limit: int):
    return db.query(FinancialData).offset(skip).limit(limit).all()

# What other endpoints would be good here?
