from fastapi import FastAPI
from app.api.routes.data_ingestion import data_ingestion_router
from app.api.routes.data_processing import data_processing_router
from app.api.routes.ml_models import ml_models_router


# Create a FastAPI instance
app = FastAPI(
    title="AI Trading",
    description="This is a simple AI trading API",
    version="0.1"
)


# Include the routers (API routes) in the FastAPI instance
# The prefix parameter is used to define the base URL for the routes, so the actual endpoint would be {prefix}/{endpoint}
app.include_router(data_ingestion_router, prefix="/api/data-ingestion", tags=["Data Ingestion"]) 
app.include_router(data_processing_router, prefix="/api/data-processing", tags=["Data Processing"])
app.include_router(ml_models_router, prefix="/api/ml-models", tags=["ML Models"])