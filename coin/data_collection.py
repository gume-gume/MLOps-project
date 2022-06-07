from coin_service import Coin_service
from config import settings

coin_service = Coin_service()
ticker = settings.ticker
df = coin_service.update_ohlcv(ticker, settings.interval)
coin_service.insert_df(df, ticker, exists="append")
