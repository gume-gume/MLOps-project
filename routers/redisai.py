from fastapi import APIRouter,FastAPI
from db.database import SessionLocal
import psycopg2
import pandas as pd
import numpy as np

from schemas.request import IncomeBody
from schemas.response import Item

import redisai as rai
from utils.utils import *
from service.service_result import handle_result

client = None

app = FastAPI()
router = APIRouter()

db = SessionLocal()

@router.on_event("startup")
def start_up():
    global client
    client = rai.Client(host="localhost", port=6379, health_check_interval=30)

@router.post('/production')
def produce_model(n_trial: int, n_split:int, scoring : str):
    conn_string = "host = 'localhost' dbname = 'income_db' user = 'postgres' password = '1234'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute('SELECT * FROM people_income;')
    result = np.array(cur.fetchall())
    income_df = pd.DataFrame(result)
    income_df.columns = [desc[0] for desc in cur.description]

    income_df = preprocessing(income_df)
    X_train, X_test, y_train, y_test = data_split(income_df)
    X_train, X_test = labeling(X_train, X_test)
    params = rf_optimization(X_train, y_train, n_trials={n_trial},  n_splits={n_split}, measure={scoring})
    pred = model_predict(params, X_train,y_train)
    params = rf_optimization(X_train, y_train, n_trials=3,  n_splits=2, measure='accuracy')
    pred = model_predict(params, X_train,y_train)
    return model_save(pred)

@router.post("/income/predict",response_model=Item)
def predict_income(item: IncomeBody, name : str, model_key : str):
    if not client.exists("model"):
        load_model(client,"model",name)
    result = predict(client, f"{model_key}", item)
    item.target = handle_result(result)
    if item.target == 1:
        item.context = "소득이 10만달러 이상"
    else:
        item.context = "소득이 10만달러 미만"
    return item


#프로파일링
import cProfile
import re
cProfile.run('re.compile("produce_model|predict_income")')
