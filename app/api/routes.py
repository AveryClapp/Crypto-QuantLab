from fastapi import APIRouter
from app.services import data_ingestion, data_processing, ai_report

router = APIRouter()

# Get the latest news on a token
@router.get("/articles/{token}")
async def hot_articles(token: str):
    return

# Get latest pricing and financial data on a token
@router.get("/prices")
async def get_prices():
    return

# Analyze twitter and other social media platforms and return hot posts
@router.get("/socials/{token}")
async def get_social_media(token: str):
    return

# Get the market trends with crypto
@router.get("/trends")
async def get_trends(token: str):
    return

# Get the market trends with specific token
@router.get("/trends/{token}")
async def get_token_trends(token: str):
    return


# This should realistically use all the other endpoints to generate a report
@router.get("/sentiments/{token}")
async def get_sentiments(token: str):
    return