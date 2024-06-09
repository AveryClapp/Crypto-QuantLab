from fastapi import APIRouter
from app.services import data_ingestion, data_processing, ai_report

router = APIRouter()

@router.get("/tester")
async def test():
    return {"message": "Test Successful"}

