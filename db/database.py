import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import psycopg2



engine = create_engine("postgresql://postgres:postgres@localhost/income_db",echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind = engine)
conn = psycopg2.connect(host = 'localhost', 
                        database = 'income_db',
                        user = 'postgres',
                        password = 'postgres')
conn.autocommit = True
cursor = conn.cursor()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


def creat_table():
    try:
        cursor.execute(f"""
        CREATE TABLE 'people_income'
            (id INT PRIMARY KEY NOT NULL,
            age INTEGER NOT NULL,
            workclass VARCHAR (20) NOT NULL,
            fnlwgt INTEGER NOT NULL,
            education VARCHAR (20) NOT NULL,
            education_num INTEGER NOT NULL,
            marital_status VARCHAR (40) NOT NULL,
            occupation VARCHAR (20) NOT NULL,
            relationship VARCHAR (40) NOT NULL,
            race VARCHAR (20) NOT NULL,
            sex VARCHAR (6) NOT NULL,
            capital_gain INTEGER NOT NULL,
            capital_loss INTEGER NOT NULL,
            hours_per_week INTEGER NOT NULL,
            native_country VARCHAR (40) NOT NULL,
            target INTEGER NOT NULL);
        """)
    except Exception as ex:
        print('creat_table:', ex)
        


def insert_data():
    try:
        _file='train.csv'
        df=pd.read_csv(_file)

        engine = create_engine("postgresql://postgres:postgres@localhost/income_db",echo=True)
        df.to_sql(name = 'people_income',
                con = engine,
                schema = 'public',
                if_exists = 'replace',
                index = False,
                dtype ={
                    'id' :sqlalchemy.types.INTEGER(),
                    'age' :sqlalchemy.types.INTEGER(),
                    'workclass': sqlalchemy.types.VARCHAR(20),
                    'fnlwgt': sqlalchemy.types.INTEGER(),
                    'education':sqlalchemy.types.VARCHAR(20),
                    'education_num': sqlalchemy.types.INTEGER(),
                    'marital_status':sqlalchemy.types.VARCHAR(40),
                    'occupation': sqlalchemy.types.VARCHAR(20),
                    'relationship':sqlalchemy.types.VARCHAR(20),
                    'race': sqlalchemy.types.VARCHAR(20),
                    'sex': sqlalchemy.types.VARCHAR(6),
                    'capital_gain': sqlalchemy.types.INTEGER(),
                    'capital_loss':sqlalchemy.types.INTEGER(),
                    'hours_per_week':sqlalchemy.types.INTEGER(),
                    'native_country': sqlalchemy.types.VARCHAR(20),
                    'target': sqlalchemy.types.INTEGER()
                }
                )
    except Exception as ex:
        print('insert_data:',ex)