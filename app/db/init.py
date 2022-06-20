import sys
from psycopg2 import connect, extensions
from minio import Minio
from app.config import settings

sys.path.append("/home/dahy949/airflow/project")
DB_ID = settings.DB_ID
DB_PASSWORD = settings.DB_PASSWORD
DB_PORT = 5432
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_ADDRESS = "localhost"
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
        host="127.0.0.1",
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
    create_db("airlfow_db")
    create_db("upbit")

    create_bk("upbit")
