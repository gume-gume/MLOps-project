from coin.coin_service import Coin_service
from coin.config import settings


def add_coin(ticker):
    coin_service = Coin_service()
    df = coin_service.update_ohlcv(ticker, settings.interval)
    coin_service.insert_df(df, ticker, exists="append")
