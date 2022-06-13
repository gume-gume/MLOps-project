import os
import math
import time

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_squared_log_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Conv1D
from tensorflow.keras.losses import Huber
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import metrics
import pandas as pd
import numpy as np
import pyupbit
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2

from coin.config import settings


conn = psycopg2.connect(
    host=settings.DB_ADDRESS,
    database=settings.DB_NAME,
    user=settings.DB_ID,
    password=settings.DB_PASSWORD,
)

cursor = conn.cursor()
engine = create_engine(
    f"postgresql://{settings.DB_ID}:{settings.DB_PASSWORD}@{settings.DB_ADDRESS}/{settings.DB_NAME}",
    echo=True,
)


class Coin_service:
    def __init__(self):
        self.conn = conn

        self.cursor = cursor
        self.engine = engine
        self.WINDOW_SIZE = 20
        self.BATCH_SIZE = 32

    def update_ohlcv(self, ticker, interval):
        """
        db에 있는 가격데이터에 데이터를 추가하여 df 생성
        db에 테이블이 없으면 코인상장일부터의 데이터 수집
        """
        print(f"{ticker} update_ohlcv.....")
        self.conn.autocommit = True
        self.cursor.execute(
            """SELECT TABLE_NAME
        FROM   INFORMATION_SCHEMA.TABLES
        WHERE  TABLE_SCHEMA = 'public'
        ORDER BY TABLE_NAME ASC;"""
        )
        table_list = self.cursor.fetchall()
        if ticker in [t[0] for t in table_list]:
            try:
                print(f"{ticker} table exist.....")
                temp = []
                coin_df = pyupbit.get_ohlcv(ticker, interval=interval)
                self.cursor.execute(f"""SELECT * FROM public."{ticker}";""")
                table = self.cursor.fetchall()
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
                return coin_dfs
            except Exception:
                pass
        else:

            coin_dfs = self.get_ohlcv(ticker, interval)
            return coin_dfs

    def get_ohlcv(self, ticker, interval):
        """
        작성자 : 이대형
        코인 전체데이터 가져오기
        """
        print(f"{ticker} get total ohlcv.....")
        try:
            dfs = []
            df = pyupbit.get_ohlcv(ticker, interval=interval)
            dfs.append(df)

            while len(df) >= 200:
                try:
                    df = pyupbit.get_ohlcv(ticker, interval=interval, to=df.index[0])
                    dfs.append(df)
                    time.sleep(0.2)
                except Exception:
                    pass
            df = pd.concat(dfs)
            df = df.sort_index()
            df.drop_duplicates(inplace=True)
            return df
        except Exception:
            pass

    def insert_df(self, df, ticker, exists="replace"):
        """
        작성자 : 이대형
        csv data를 sql에 밀어 넣는 부분
        """
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

    def data_load(self, ticker):

        cursor.execute(f"""SELECT * FROM public."{ticker}";""")
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        df.set_index(0, inplace=True)
        cols = ["open", "high", "low", "close", "volume", "value"]
        df.columns = cols
        return df

    def scaling(self, df):

        scaler = MinMaxScaler()
        scaler_y = MinMaxScaler()
        df[["open", "high", "low", "volume", "value"]] = scaler.fit_transform(
            df[["open", "high", "low", "volume", "value"]]
        )
        df["close"] = scaler_y.fit_transform(df["close"].values.reshape(-1, 1))
        return df, scaler_y

    def split(self, df):
        x_train, x_test, y_train, y_test = train_test_split(
            df.drop("close", 1),
            df["close"],
            test_size=0.2,
            random_state=0,
            shuffle=False,
        )
        return x_train, x_test, y_train, y_test

    def windowed_dataset(self, series, shuffle):
        series = tf.expand_dims(series, axis=-1)
        ds = tf.data.Dataset.from_tensor_slices(series)
        ds = ds.window(self.WINDOW_SIZE + 1, shift=1, drop_remainder=True)
        ds = ds.flat_map(lambda w: w.batch(self.WINDOW_SIZE + 1))
        if shuffle:
            ds = ds.shuffle(1000)
        ds = ds.map(lambda w: (w[:-1], w[-1]))
        return ds.batch(self.BATCH_SIZE).prefetch(1)

    def run_model(self, train_data, test_data, scaler_y):
        model = Sequential(
            [
                Conv1D(
                    filters=32,
                    kernel_size=5,
                    padding="causal",
                    activation="relu",
                    input_shape=[self.WINDOW_SIZE, 1],
                ),
                LSTM(16, activation="tanh"),
                Dense(16, activation="relu"),
                Dense(1),
            ]
        )

        optimizer = Adam(0.0005)
        model.compile(loss=Huber(), optimizer=optimizer, metrics=["mse"])

        model.compile(
            loss="mean_squared_error",
            optimizer="sgd",
            metrics=[metrics.mae, metrics.categorical_accuracy],
        )
        earlystopping = EarlyStopping(monitor="val_loss", patience=10)

        filename = os.path.join("tmp", "ckeckpointer.ckpt")
        checkpoint = ModelCheckpoint(
            filename,
            save_weights_only=True,
            save_best_only=True,
            monitor="val_loss",
            verbose=1,
        )

        history = model.fit(
            train_data,
            validation_data=(test_data),
            epochs=2,
            callbacks=[checkpoint, earlystopping],
        )
        print(history)
        model.load_weights(filename)

        y_pred = model.predict(test_data)
        rescaled_pred = scaler_y.inverse_transform(np.array(y_pred).reshape(-1, 1))
        return rescaled_pred, model

    def confirm_result(self, y_test, y_pred):
        index = self.WINDOW_SIZE
        y_test = y_test[
            index:,
        ]
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        msle = mean_squared_log_error(y_test, y_pred)
        rmsle = np.sqrt(mean_squared_log_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        metrics = {"mae": mae, "rmse": rmse, "msle": msle, "rmsle": rmsle, "r2": r2}
        return metrics
