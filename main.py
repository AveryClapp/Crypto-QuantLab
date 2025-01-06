from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.finance_routes import router as finance_router
from app.api.sentiment_routes import router as sentiment_router

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3001",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(finance_router, prefix="/api")
app.include_router(sentiment_router, prefix="/api")

@app.get("/")
async def main():
    return {"message": "Hello World"}
