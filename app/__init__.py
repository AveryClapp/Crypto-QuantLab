from fastapi import FastAPI
from app.api.routes import router



# Create a FastAPI instance
app = FastAPI(
    title="AI Trading",
    description="This is a simple AI trading API",
    version="0.1"
)

@app.get("/")
async def root():
    return "Welcome! This is the root endpoint of the AI Trading API. Please refer to the documentation for more details."


# Include the routers (API routes) in the FastAPI instance
# The prefix parameter is used to define the base URL for the routes, so the actual endpoint would be {prefix}/{endpoint}
app.include_router(router, prefix="/api", tags=["API"]) 