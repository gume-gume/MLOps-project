from datetime import datetime, timedelta
import sys

sys.path.append("/home/dahy949/airflow/project")
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule

from coin.utils import SlackAlert


ticker = "KRW-ETH"
slack = SlackAlert("mlopsproject")

default_args = {
    "owner": "Daehyeong Lee",
    "depends_on_past": False,
    "email": ["dahy949@gmail.com", "altu1996@gmail.com", "tjsrb63@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=10),
}

dag_args = dict(
    dag_id=f"{ticker}_PIPELINE",
    default_args=default_args,
    description="코인데이터 수집후 모델훈련",
    schedule_interval=timedelta(minutes=240),
    start_date=datetime(2022, 6, 1),
    tags=[ticker],
    on_success_callback=slack.success_msg,
    on_failure_callback=slack.fail_msg,
)


def add():

    from coin import data_collection

    data_collection.add_coin(ticker)


def verify():
    print("검증 완료~")


def train(ticker):
    from coin import coin_predict

    coin_predict.train(ticker)


with DAG(**dag_args) as dag:
    start = BashOperator(
        task_id="start",
        bash_command='echo "start!"',
    )

    coin_add = PythonOperator(task_id="add", python_callable=add)
    coin_verify = PythonOperator(task_id="verify", python_callable=verify)
    coin_op = DummyOperator(
        task_id="all_done", dag=dag, trigger_rule=TriggerRule.ALL_DONE
    )
    coin_train = PythonOperator(
        task_id="train",
        python_callable=train,
        trigger_rule=TriggerRule.ALL_DONE,
        op_kwargs={"ticker": ticker},
    )

    start >> coin_add >> coin_op >> coin_train
    start >> coin_verify >> coin_op >> coin_train

    # +서브댁
    # 더미오퍼레이터
    # ml / data: s나눠서 확정성 좀 더 고려~

    # 시총별로 3단계~ 코인~
