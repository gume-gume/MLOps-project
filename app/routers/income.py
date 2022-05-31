from db.database import SessionLocal
from fastapi import APIRouter
from app.schemas.request import IncomeBody
from app.schemas.response import Item, TrainDone
import redisai as rai
from app.service.app_service import TrainService, PredictService
from app.utils.service_result import handle_result
from config import settings

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
def produce_model(n_trial: int, n_split: int, scoring: str, name: str):
    result = TrainService().train(
        n_trial=n_trial, n_split=n_split, scoring=scoring, name=name
    )
    return handle_result(result)


@router.post("/income/predict", response_model=Item)
def predict_income(item: IncomeBody, model_key: str, name: str):
    result = PredictService(client, model_key, name).predict(item)
    return handle_result(result)
