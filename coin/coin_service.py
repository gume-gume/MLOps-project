import pyupbit
import math
import time
import pandas as pd
import sqlalchemy

from sqlalchemy import create_engine
import psycopg2
from config import settings

conn = psycopg2.connect(
    host=settings.DB_ADDRESS,
    database=settings.DB_NAME,
    user=settings.DB_ID,
    password=settings.DB_PASSWORD,
)
conn.autocommit = True
cursor = conn.cursor()
engine = create_engine(
    f"postgresql://{settings.DB_ID}:{settings.DB_PASSWORD}@{settings.DB_ADDRESS}/{settings.DB_NAME}",
    echo=True,
)
# conn.close()


class Coin_service:
    def __init__(self):
        self.conn = conn
        self.conn.autocommit = True
        self.cursor = cursor
        self.engine = engine

    def update_ohlcv(self, ticker, interval):
        """
        db에 있는 가격데이터에 데이터를 추가하여 df 생성
        db에 테이블이 없으면 코인상장일부터의 데이터 수집
        """
        print("update_ohlcv.....")

        self.cursor.execute(
            """SELECT TABLE_NAME
        FROM   INFORMATION_SCHEMA.TABLES
        WHERE  TABLE_SCHEMA = 'public'
        ORDER BY TABLE_NAME ASC;"""
        )
        table_list = self.cursor.fetchall()

        if ticker in [t[0] for t in table_list]:
            try:
                print("table exist.....")
                temp = []
                coin_df = pyupbit.get_ohlcv(ticker, interval=interval)
                self.cursor.execute(f"""SELECT * FROM public."{ticker}";""")
                table = cursor.fetchall()
                repeat = math.ceil(
                    (coin_df.index[-1] - table[-1][0]).seconds / 60 / 60 / 4 / 200
                )
                for i in range(0, repeat):
                    time.sleep(0.2)
                    coin_df = pyupbit.get_ohlcv(
                        ticker, interval=interval, to=coin_df.index[0]
                    )
                    temp.append(coin_df)
                coin_dfs = pd.concat(temp)

                start_index = coin_dfs.index.get_loc(table[-1][0]) + 1
                coin_dfs[start_index:]
                print(coin_dfs.tail())
                return coin_dfs
            except Exception as ex:
                print("update_ohlcv error:", ex)
                pass
        else:
            print("table not exist....")
            coin_dfs = self.get_ohlcv(ticker, interval)
            return coin_dfs

    def get_ohlcv(self, ticker, interval):
        """
        작성자 : 이대형
        코인 전체데이터 가져오기
        """
        print("get total ohlcv.....")
        try:
            dfs = []
            df = pyupbit.get_ohlcv(ticker, interval=interval)
            dfs.append(df)

            while len(df) >= 200:
                try:
                    df = pyupbit.get_ohlcv(ticker, interval=interval, to=df.index[0])
                    dfs.append(df)
                    time.sleep(0.2)
                except Exception as ex:
                    print("get_ohlcv error:", ex)
                    pass
            df = pd.concat(dfs)
            df = df.sort_index()
            print(df.tail())
            return df
        except Exception as ex:
            print("get_ohlcv error:", ex)
            pass

    def insert_df(self, df, ticker, exists="replace"):
        """
        작성자 : 이대형
        csv data를 sql에 밀어 넣는 부분
        """

        #
        try:
            df.to_sql(
                name=ticker,
                con=self.engine,
                schema="public",
                if_exists=exists,
                index=True,
                dtype={
                    "open": sqlalchemy.types.FLOAT(),
                    "high": sqlalchemy.types.FLOAT(),
                    "low": sqlalchemy.types.FLOAT(),
                    "close": sqlalchemy.types.FLOAT(),
                    "volume": sqlalchemy.types.FLOAT(),
                    "value": sqlalchemy.types.FLOAT(),
                },
            )
            print("----------data inserted-----------")
        except Exception as ex:
            print("insert_df error :", ex)
            pass
