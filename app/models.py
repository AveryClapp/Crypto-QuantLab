from sqlalchemy import Column, Integer, Float, DateTime, DECIMAL, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FinancialData(Base):
    __tablename__ = "Crypto_Financials"
    
    # Create table fields
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, default=datetime.utcnow, index=True)
    price = Column(DECIMAL(20, 2), nullable=False)
    daily_volume = Column(DECIMAL(20, 2), nullable=False)
    daily_volume_change = Column(DECIMAL(20, 2), nullable=False)
    market_cap = Column(DECIMAL(20, 2), nullable=False)
    daily_delta = Column(DECIMAL(20, 2), nullable=False)
    weekly_delta = Column(DECIMAL(20, 2), nullable=False)
    fear_and_greed = Column(Integer, nullable=False)
    btc_dominance = Column(DECIMAL(20, 2), nullable=False)
    stablecoin_volume = Column(DECIMAL(20, 2), nullable=False)
    total_market_cap = Column(DECIMAL(20, 2), nullable=False)

class PostData(Base):
    __tablename__ = "Posts"

    # Create table fields 
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    subreddit = Column(String(100), nullable=False)
    description = Column(String(400))
    url = Column(String(100))
    sentiment = Column(Float)
    upvotes = Column(Integer)
    created_at = Column(DateTime)
