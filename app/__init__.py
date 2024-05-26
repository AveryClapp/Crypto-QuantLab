from fastapi import FastAPI
from app.api.routes.data_ingestion import ingestion_router
from app.api.routes.data_processing import processing_router
from app.api.routes.ml_models import model_router


# Create a FastAPI instance
app = FastAPI(
    title="AI Trading",
    description="This is a simple AI trading API",
    version="0.1"
)


# Include the routers (API routes) in the FastAPI instance
# The prefix parameter is used to define the base URL for the routes, so the actual endpoint would be {prefix}/{endpoint}
app.include_router(ingestion_router, prefix="/api/ingestion", tags=["Data Ingestion"]) 
app.include_router(processing_router, prefix="/api/processing", tags=["Data Processing"])
app.include_router(model_router, prefix="/api/model", tags=["ML Models"])