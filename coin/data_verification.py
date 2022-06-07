from coin_service import Coin_service
from config import settings


cursor = Coin_service.cursor
cursor.execute(f"""SELECT * FROM public."{settings.ticker}";""")
data = cursor.fetchall()
datetime_list = [time[0] for time in data]


def verify():
    print("no problem~")


# 1  counting
outlier = 10
(len(datetime_list) / 6 - outlier) <= (
    datetime_list[-1].date() - datetime_list[0].date()
).days <= (len(datetime_list) / 6 + outlier)


# 2 timedelta
a = datetime_list[0]
print(len(datetime_list))
for i in datetime_list[1:]:
    if (i - a).seconds / 60 / 60 == 4:
        pass
    else:
        print("차이시간 : ", (i - a).seconds / 60 / 60)
    a = i
