from coin.coin_service import cursor
from coin.config import settings
import numpy as np
import pandas as pd

cursor = cursor
cursor.execute(f"""SELECT * FROM public."{settings.ticker}";""")
data = cursor.fetchall()
datetime_list = [time[0] for time in data]
print("=====" * 10)


def verify():
    print("no problem~")


# 1  counting
def coin_date_check(datetime_list):
    datetime = []
    for i in range(len(datetime_list)):
        datetime.append(datetime_list[i].date())
    unique_date_list = np.unique(datetime)
    date_idx = pd.date_range(datetime_list[0].date(), datetime_list[-1].date())

    no_data_idx = []
    if len(date_idx) != len(unique_date_list):
        print("결측 date 존재")
        for i in range(len(date_idx)):
            if date_idx[i].date() in unique_date_list:
                pass
            else:
                no_data_idx.append(i)
    return no_data_idx


# 2 timedelta
def coin_time_check(datetime_list):
    datetime_list = np.unique(datetime_list)
    for i in range(len(datetime_list) - 1):
        if (datetime_list[i + 1] - datetime_list[i]).seconds / 60 / 60 != 4:
            print(i, (datetime_list[i + 1] - datetime_list[i]).seconds / 60 / 60)


coin_date_check(datetime_list)
coin_time_check(datetime_list)
