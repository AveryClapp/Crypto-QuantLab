from fastapi import APIRouter
from app.services import data_ingestion, data_processing, ai_report

router = APIRouter()

@router.get("/{ticker}")
async def setup_data(ticker: str):
    extracted_data = data_ingestion.main(ticker)
    processed_data = data_processing.main(extracted_data)
    report = ai_report.main(processed_data)
    return report