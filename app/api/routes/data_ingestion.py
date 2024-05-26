from fastapi import APIRouter

ingestion_router = APIRouter()

@ingestion_router.get("/ingest-data")
async def ingest_data():
    return {"data": "Ingest Data!"}
