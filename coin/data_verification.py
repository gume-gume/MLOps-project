from coin_service import conn, cursor, engine, Coin_service
from config import settings
import pandas as pd
import re
import pyupbit
import datetime

coin_service = Coin_service()

cursor.execute(f"""SELECT * FROM public."{settings.ticker}";""")
data = cursor.fetchall()
datetime_list = [time[0] for time in data]


def cleanText(readData):
    text = re.sub("[-]", "", readData)
    return text


def fill_data(null_date):
    list_of_df = []
    for date in null_date:
        df_temp = pyupbit.get_ohlcv(
            ticker=settings.ticker,
            interval="minutes240",
            count=6,
            to=f"{date}",
            period=0.1,
        )
        list_of_df.append(df_temp)
    df_accum = pd.concat(list_of_df)
    return df_accum


def db_manage_command(cursor, text):
    cursor.execute(text)
    conn.commit()


def coin_date_check(datetime_list, engine):

    db_date = pd.Series(datetime_list)
    db_date = db_date.apply(lambda x: x.date()).drop_duplicates()
    db_date.reset_index(drop=True, inplace=True)

    continue_date = pd.date_range(
        datetime_list[0].date(), datetime_list[-1].date()
    ).to_series()
    continue_date.reset_index(drop=True, inplace=True)
    continue_date = continue_date.apply(lambda x: x.date())

    if len(db_date) != len(continue_date):
        print("결측 date 존재")
        check_df = pd.concat([db_date, continue_date]).reset_index(drop=True)
        check_df.drop_duplicates(keep=False, inplace=True)
        check_df.reset_index(drop=True, inplace=True)
        check_df = check_df.apply(lambda x: x + datetime.timedelta(days=1))
        check_df = check_df.apply(lambda x: cleanText(x.strftime("%Y-%m-%d")))
        coin_service.insert_df(fill_data(check_df), settings.ticker, exists="append")

    postgres_df = pd.read_sql("""SELECT * FROM public."{settings.ticker}";""", engine)
    postgres_df.set_index("index", inplace=True)
    postgres_df.drop_duplicates(inplace=True)
    postgres_df = postgres_df.sort_index()
    datetime_list = postgres_df.index

    null_time = []
    for i in range(len(datetime_list) - 1):
        if (datetime_list[i + 1] - datetime_list[i]).seconds / 60 / 60 != 4:
            date = datetime_list[i + 1].date().strftime("%Y-%m-%d")
            null_time.append(date)
            coin_service.insert_df(
                fill_data(null_time), settings.ticker, exists="append"
            )

    postgres_df = pd.read_sql(f"""SELECT * FROM public."{settings.ticker}";""", engine)
    postgres_df.set_index("index", inplace=True)
    postgres_df.drop_duplicates(inplace=True)

    coin_service.insert_df(postgres_df, settings.ticker, exists="append")

    return postgres_df


coin_date_check(datetime_list, engine)
