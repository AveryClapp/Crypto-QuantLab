from fastapi import APIRouter

processing_router = APIRouter()

@processing_router.get("/process-data")
async def process_data():
    return {"data": "Process Data!"}