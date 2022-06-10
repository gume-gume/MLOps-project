from slack_sdk import WebClient
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule

import sys

sys.path.append("/home/dahy949/airflow/project")

# from coin.config import settings


class SlackAlert:
    def __init__(self, channel):
        from coin.config import settings

        token = settings.token
        self.channel = channel
        self.token = token
        self.client = WebClient(token=token)

    def success_msg(self, msg):
        text = f"""
            =======================================
            date : {datetime.today().strftime('%Y-%m-%d')}
            alert : Success!
            ---------------------------------------
            task id : {msg.get('task_instance').task_id},
            dag id : {msg.get('task_instance').dag_id},
            log url : {msg.get('task_instance').log_url}
            =======================================
            """
        self.client.chat_postMessage(channel=self.channel, text=text)

    def fail_msg(self, msg):
        text = f"""
            =======================================
            date : {datetime.today().strftime('%Y-%m-%d')}
            alert : Fail!
            ---------------------------------------
            task id : {msg.get('task_instance').task_id},
            dag id : {msg.get('task_instance').dag_id},
            log url : {msg.get('task_instance').log_url}
            =======================================
        """
        self.client.chat_postMessage(channel=self.channel, text=text)


slack = SlackAlert("mlopsproject")

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
    dag_id="coin_pipelie",
    default_args=default_args,
    description="코인데이터 수집후 모델훈련",
    schedule_interval=timedelta(minutes=1),
    start_date=datetime(2022, 6, 1),
    tags=["coin"],
    on_success_callback=slack.success_msg,
    on_failure_callback=slack.fail_msg,
)


def add():
    from coin import data_collection

    data_collection.add_coin()


def verify():
    print("검증 완료~")


def train():
    from coin import coin_predict

    coin_predict.train()


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

    start >> coin_add
    start >> coin_verify >> coin_train
