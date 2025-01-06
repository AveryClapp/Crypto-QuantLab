from fastapi import APIRouter
from app.database import get_db
from app.models import PostData
from app.schemas import PostCreate, PostResponse, PostUpdate
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

db = next(get_db())
router = APIRouter()
current_time = datetime.now().time()

# Get the most recent {span} hours of sentiment data
@router.get("/sentiment/{span}")
async def get_sentiment(span: int):
    span = int(span)
    start_time = datetime.now() - timedelta(hours=span) 
    relevant_posts = db.query(PostData).filter(PostData.created_at >= start_time).all()
    try:
        avg_sentiment = sum(post.sentiment for post in relevant_posts) / len(relevant_posts)
    except Exception as e:
        print(e)
        avg_sentiment = "Average Sentiment Not Available for this time frame"
    return round(avg_sentiment, 2) 

# Get the most popular article in the last 24 hours
@router.get("/hot_article/{limit}")
async def get_hottest_article(limit: int):
    start_time = datetime.now() - timedelta(days=1)
    return db.query(PostData).filter(PostData.created_at >= start_time).order_by(PostData.upvotes.desc()).limit(limit).all()

@router.get("/positive_articles")
async def get_positive_articles():
    start_time = datetime.now() - timedelta(days=1)
    return db.query(PostData).filter(PostData.created_at >= start_time, PostData.sentiment > 0.2).all()

@router.get("/negative_articles")
async def get_negative_articles():
    start_time = datetime.now() - timedelta(days=1)
    return db.query(PostData).filter(PostData.created_at >= start_time, PostData.sentiment < -0.2).all()

@router.get("/neutral_articles")
async def get_neutral_articles():
    start_time = datetime.now() - timedelta(days=1)
    return db.query(PostData).filter(PostData.created_at >= start_time, -0.2 <= PostData.sentiment, PostData.sentiment <= 0.2).all()
