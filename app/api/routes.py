from fastapi import APIRouter
from app.services import data_ingestion, data_processing, ml_models

router = APIRouter()

@router.get("/{ticker}")
async def setup_data(ticker: str):
    return f"Geting data on {ticker}"