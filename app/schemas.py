from pydantic import BaseModel
from datetime import datetime

class FinancialDataBase(BaseModel):
    time: datetime
    price: float
    daily_volume: float
    daily_volume_change: float
    market_cap: float
    daily_delta: float
    weekly_delta: float
    fear_and_greed: int
    btc_dominance: float
    stablecoin_volume: float
    total_market_cap: float
    
    class Config:
        orm_mode = True  

class FinancialDataCreate(FinancialDataBase):
    pass

class FinancialDataResponse(FinancialDataBase):
    id: int

class PostBase(BaseModel):
    title: str
    subreddit: str
    description: Optional[str]
    url: Optional[str]
    sentiment: Optional[float]
    upvotes: Optional[int]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str]
    subreddit: Optional[str]
    description: Optional[str]
    url: Optional[str]
    sentiment: Optional[float]
    upvotes: Optional[int]

    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int

