from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import FinancialData

router = APIRouter()

@router.post("/financial_data/")
async def create_financial_data(data: FinancialData, db: Session = Depends(get_db)):
    """
    Create a new financial data entry in the database.
    """
    new_data = FinancialData(**data.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.get("/financial_data/{data_id}")
async def get_financial_data(data_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific financial data entry by its ID.
    """
    data = db.query(FinancialData).filter(FinancialData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@router.get("/financial_data/")
async def list_financial_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    List financial data entries with optional pagination.
    """
    data = db.query(FinancialData).offset(skip).limit(limit).all()
    return data

@router.put("/financial_data/{data_id}")
async def update_financial_data(data_id: int, updated_data: FinancialData, db: Session = Depends(get_db)):
    """
    Update a specific financial data entry by its ID.
    """
    updated_data = FinancialData(**data.dict())
    data = db.query(FinancialData).filter(FinancialData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(data, key, value)
    db.commit()
    db.refresh(data)
    return data

@router.delete("/financial_data/{data_id}")
async def delete_financial_data(data_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific financial data entry by its ID.
    """
    data = db.query(FinancialData).filter(FinancialData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    db.delete(data)
    db.commit()
    return {"detail": f"Data with ID {data_id} deleted successfully"}

