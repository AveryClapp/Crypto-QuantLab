from fastapi import APIRouter



router = APIRouter()

# Query the most recent sentiment calculation
@router.get("/sentiment")
async def get_sentiment():
    
