import sys

sys.path.append("/home/dahy949/airflow/project/coin")
from coin_service import Coin_service
from config import settings


def add_coin(ticker):
    coin_service = Coin_service()
    df = coin_service.update_ohlcv(ticker, settings.interval)
    print(df)
    coin_service.insert_df(df, ticker, exists="append")


add_coin("KRW-BTC")
add_coin("KRW-ETH")
