import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from config import settings
print('-----------',settings.DB_ID)

engine = create_engine(f"postgresql://{settings.DB_ID}:{settings.DB_PASSWORD}@{settings.DB_ADDRESS}/{settings.DB_NAME}" ,echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind = engine)
conn = psycopg2.connect(host =settings.DB_ADDRESS ,
                        database = settings.DB_NAME,
                        user = settings.DB_ID,
                        password =settings.DB_PASSWORD)
conn.autocommit = True
cursor = conn.cursor()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_data():
    _file='train.csv'
    df=pd.read_csv(_file)
    df.columns=[i.replace('.','_')for i in df.columns]
    df.to_sql(name = settings.DB_TABLE,
            con = engine,
            schema = 'public',
            if_exists = settings.DB_TABLE_OPTION,
            index = False,
            dtype ={
                'id' :sqlalchemy.types.INTEGER(),
                'age' :sqlalchemy.types.INTEGER(),
                'workclass': sqlalchemy.types.VARCHAR(40),
                'fnlwgt': sqlalchemy.types.INTEGER(),
                'education':sqlalchemy.types.VARCHAR(40),
                'education_num': sqlalchemy.types.INTEGER(),
                'marital_status':sqlalchemy.types.VARCHAR(80),
                'occupation': sqlalchemy.types.VARCHAR(40),
                'relationship':sqlalchemy.types.VARCHAR(40),
                'race': sqlalchemy.types.VARCHAR(40),
                'sex': sqlalchemy.types.VARCHAR(10),
                'capital_gain': sqlalchemy.types.INTEGER(),
                'capital_loss':sqlalchemy.types.INTEGER(),
                'hours_per_week':sqlalchemy.types.INTEGER(),
                'native_country': sqlalchemy.types.VARCHAR(40),
                'target': sqlalchemy.types.INTEGER()
            }
            )
