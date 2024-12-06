from fastapi import APIRouter



router = APIRouter()

@router.get("/sentiment")
async def get_sentiment():


