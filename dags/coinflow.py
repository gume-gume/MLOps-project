from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
import sys

sys.path.append("/home/dahy949/airflow/project")

default_args = {
    "owner": "leedaehyeong",
    "depends_on_past": False,
    "email": ["dahy949@gmail.com", "altu1996@gmail.com", "tjsrb63@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag_args = dict(
    dag_id="coin_test",
    default_args=default_args,
    description="코인데이터 수집후 모델",
    schedule_interval=timedelta(minutes=1),
    start_date=datetime(2022, 6, 1),
    tags=["btc"],
)


def add():

    from coin import data_collection

    data_collection.add_coin()


def verify():
    print("검증완료~")


def train():
    from coin import coin_predict

    coin_predict.train()
    print("종료~~")


with DAG(**dag_args) as dag:
    start = BashOperator(
        task_id="start",
        bash_command='echo "start!"',
    )

    coin_add = PythonOperator(task_id="add", python_callable=add)

    coin_verify = PythonOperator(task_id="verify", python_callable=verify)

    coin_train = PythonOperator(
        task_id="train", python_callable=train, trigger_rule=TriggerRule.ALL_DONE
    )

    start >> coin_add >> coin_verify >> coin_train
    # start >> coin_verify >> coin_end
