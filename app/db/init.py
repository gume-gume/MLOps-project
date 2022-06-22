import sys

sys.path.append("/home/dahy949/airflow/project")
from psycopg2 import connect, extensions
from minio import Minio
from app.config import settings


DB_ID = settings.DB_ID
DB_PASSWORD = settings.DB_PASSWORD
DB_PORT = 5432
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_ADDRESS = "172.26.0.6"
MINIO_PORT = 9000


def create_bk(bucket_name):
    minio_client = Minio(
        f"{MINIO_ADDRESS}:{MINIO_PORT}",
        MINIO_ACCESS_KEY,
        MINIO_SECRET_KEY,
        secure=False,
    )

    if minio_client.bucket_exists(bucket_name):
        print("bucket exists")
    else:
        minio_client.make_bucket(bucket_name)
        print("bucket does not exist")


def create_db(DB_NAME):
    conn = connect(
        database="postgres",
        user=DB_ID,
        password=DB_PASSWORD,
        host="172.26.0.7",
        port=DB_PORT,
    )
    cursor = conn.cursor()

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    print("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_isolation_level(autocommit)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE " + str(DB_NAME))
    print(f"{DB_NAME} Database created successfully...!")

    cursor.close
    conn.close()


if __name__ == "__main__":
    create_db("income_db")
    create_db("airflow_db")
    create_db("upbit")

    create_bk("upbit")
