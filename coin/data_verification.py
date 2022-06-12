from coin.coin_service import conn, cursor, Coin_service
from coin.config import settings
import numpy as np
import pandas as pd
import re
import pyupbit

cursor = cursor
cursor.execute(f"""SELECT * FROM public."{settings.ticker}";""")
data = cursor.fetchall()
datetime_list = [time[0] for time in data]

coin_service = Coin_service()


def cleanText(readData):
    text = re.sub("[-]", "", readData)
    return text


def fill_data(null_date):
    df = pd.DataFrame()
    for date in null_date:
        df1 = pyupbit.get_ohlcv(
            ticker="KRW-BTC", interval="minutes240", count=6, to=f"{date}", period=0.1
        )
        df = pd.concat([df, df1])
    return df


def coin_date_check(datetime_list):
    datetime = []
    for i in range(len(datetime_list)):
        datetime.append(datetime_list[i].date())
    unique_date_list = np.unique(datetime)
    date_idx = pd.date_range(datetime_list[0].date(), datetime_list[-1].date())

    null_date = []

    if len(date_idx.date) != len(unique_date_list):
        print("결측 date 존재")
        for i in range(len(date_idx)):
            if date_idx[i].date() in unique_date_list:
                pass
            else:
                date = date_idx[i + 1].date().strftime("%Y-%m-%d")
                null_date.append(cleanText(date))
        coin_service.insert_df(fill_data(null_date), settings.ticker, exists="append")
        null_date = []
    else:
        pass

    for i in range(len(datetime_list) - 1):
        if (datetime_list[i + 1] - datetime_list[i]).seconds / 60 / 60 != 4:
            date = datetime_list[i + 1].date().strftime("%Y-%m-%d")
            null_date.append(date)
            coin_service.insert_df(
                fill_data(null_date), settings.ticker, exists="append"
            )
        else:
            pass

    cursor.execute(f"""SELECT * FROM public."{settings.ticker}" order by index;""")
    conn.commit()
    cursor.execute(
        f"""DELETE FROM public."{settings.ticker}" WHERE ctid IN
            (SELECT A.ctid FROM (SELECT ctid, ROW_NUMBER() over
            (PARTITION BY index ORDER BY index)
            AS num FROM public."{settings.ticker}")
            A WHERE A.num > 1);"""
    )
    conn.commit()


coin_date_check(datetime_list)
