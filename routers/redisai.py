from fastapi import APIRouter
from DB.database import SessionLocal
import psycopg2
import pandas as pd
import numpy as np

from schemas.request import IncomeBody
import redisai as rai
from utils import *

client = None

router = APIRouter()

db = SessionLocal()

@router.on_event("startup")
def start_up():
    global client
    client = rai.Client(host="localhost", port=6379)

# connection 재사용하는 방법 connection pool setting
# get->post
@router.post('/production')
def produce_model():
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
    print(X_train.info())
    params = rf_optimization(X_train, y_train, n_trials=10,  n_splits=5, measure='accuracy')
    pred = model_predict(params, X_train,y_train)
    
    return model_save(pred)



@router.post("/income/predict")
def predict_income(item: IncomeBody):
    if not client.exists("model"):
        load_model(client, "model")

    result = predict(client, "model", item)

    return result.tolist()
