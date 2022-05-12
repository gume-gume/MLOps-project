from fastapi import APIRouter
from DB.database import SessionLocal
import psycopg2
import pandas as pd
import numpy as np

router = APIRouter()

db = SessionLocal()

@router.get('/incomes')
def get_all_incomes():
    conn_string = "host = 'localhost' dbname = 'income_db' user = 'postgres' password = '1234'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute('SELECT * FROM people_income;')
    result = np.array(cur.fetchall())
    my_df = pd.DataFrame(result)
    my_df.columns = [desc[0] for desc in cur.description]   
    print(my_df)
    return my_df
