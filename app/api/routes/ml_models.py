from fastapi import APIRouter

model_router = APIRouter()

@model_router.get("/model-predict")
async def model_predict():
    return {"data": "Model Predict!"}