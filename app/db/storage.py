from minio import Minio
from io import BytesIO
from datetime import datetime
import pyupbit

ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
minio_client = Minio("localhost:9000", ACCESS_KEY, SECRET_KEY, secure=False)


coin_bucket = "upbit"
initial = "KRW-BTC"
interval = "day"
crawling_date = datetime.now().date().strftime("%Y-%m-%d")

if minio_client.bucket_exists(coin_bucket):
    print("bucket exists")
else:
    minio_client.make_bucket(coin_bucket)
    print("bucket does not exist")

btc = pyupbit.get_ohlcv(initial, interval=interval)

csv_bytes = btc.to_csv().encode("utf-8")
csv_buffer = BytesIO(csv_bytes)

minio_client.put_object(
    coin_bucket,
    f"{initial}_{crawling_date}.csv",
    data=csv_buffer,
    length=len(csv_bytes),
    content_type="application/csv",
)
