from fastapi import APIRouter
from app.services import data_ingestion, data_processing, ai_report

router = APIRouter()

@router.get("/{ticker}")
async def setup_data(ticker: str):
    response = data_ingestion.setup(ticker)
    return response