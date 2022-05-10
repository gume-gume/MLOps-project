import numpy as np

import redisai as rai
from fastapi import APIRouter
from schemas.request import IncomeBody
from utils import load_model, predict

client = None
router = APIRouter(prefix="/rai", tags=["RAI"])


@router.on_event("startup")
def start_up():
    global client
    client = rai.Client(host="localhost", port=6379)


@router.post("/income/predict")
def predict_income(item: IncomeBody):
    if not client.exists("rf_income"):
        load_model(client, "rf_income")

    result = predict(client, "rf_income", item)

    return result.tolist()
