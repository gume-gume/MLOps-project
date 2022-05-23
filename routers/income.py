from fastapi import APIRouter,FastAPI,Depends
from db.database import SessionLocal, get_db

from schemas.request import IncomeBody
from schemas.response import Item
import redisai as rai

from service.app_service import *
from utils.service_result import handle_result

client = None

app = FastAPI()
router = APIRouter()

db = SessionLocal()

@router.on_event("startup")
def start_up():
    global client
    client = rai.Client(host="localhost", port=6379, health_check_interval=30)

@router.post('/production')
def produce_model(n_trial: int, n_split:int, scoring : str, db:get_db=Depends()):
    result= TrainService(db).train(n_trial=n_trial, n_split=n_split, scoring=scoring )
    return handle_result(result)


@router.post("/income/predict",response_model=Item)
def predict_income(item: IncomeBody, name : str, model_key : str):
    print('item',item)
    result= PredictService(client, model_key, name).predict(item)
    print('result',result)
    return handle_result(result)

# #프로파일링
# import cProfile
# import re
# cProfile.run('re.compile("produce_model|predict_income")')
