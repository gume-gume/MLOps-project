import sys

sys.path.append("/home/tjsrb63/project")
from app.db.database import SessionLocal
from fastapi import APIRouter
from app.schemas.request import IncomeBody, ModelName
from app.schemas.response import Item, TrainDone
import redisai as rai
import pyupbit
from app.service.app_service import TrainService, PredictService
from app.utils.service_result import handle_result
from app.config import settings
from coin.coin_predict import predict_coin


router = APIRouter()

db = SessionLocal()

client = None


@router.on_event("startup")
def start_up():
    global client
    client = rai.Client(
        host=settings.REDIS_ADDRESS,
        port=settings.REDIS_PORT,
        health_check_interval=settings.REDIS_health_check_interval,
    )


@router.post("/production", response_model=TrainDone)
def produce_model(n_trial: int, n_split: int, scoring: str, model_key: str):
    result = TrainService().train(
        n_trial=n_trial, n_split=n_split, scoring=scoring, model_key=model_key
    )
    return handle_result(result)


@router.post("/income/predict", response_model=Item)
def predict_income(item: IncomeBody, model_key: str):
    result = PredictService(client, model_key).predict(item)
    return handle_result(result)


@router.post("/coin/predict")
def predict_coin(ticker: ModelName):
    coin_df = pyupbit.get_ohlcv(ticker, interval="minute240", count=20)
    result = predict_coin(ticker, coin_df)
    return result
