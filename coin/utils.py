from slack_sdk import WebClient
from datetime import datetime
from mlflow.tracking import MlflowClient


class SlackAlert:
    def __init__(self, channel):
        from coin.config import settings

        token = settings.token
        self.channel = channel
        self.token = token
        self.client = WebClient(token=token)

    def success_msg(self, msg):
        text = f"""

date : {datetime.today().strftime('%Y-%m-%d')}
alert : Success!
---------------------------------------
task id : {msg.get('task_instance').task_id},
dag id : {msg.get('task_instance').dag_id},
log url : {msg.get('task_instance').log_url}
==============================
            """
        self.client.chat_postMessage(channel=self.channel, text=text)

    def fail_msg(self, msg):
        text = f"""

date : {datetime.today().strftime('%Y-%m-%d')}
alert : Fail!
---------------------------------------
task id : {msg.get('task_instance').task_id},
dag id : {msg.get('task_instance').dag_id},
log url : {msg.get('task_instance').log_url}
==============================
        """
        self.client.chat_postMessage(channel=self.channel, text=text)


def get_production_model_uri(model_name):
    client = MlflowClient(tracking_uri="http://172.26.0.9:5000")

    filter_string = "name='{}'".format(model_name)
    results = client.search_model_versions(filter_string)
    for res in results:
        if res.current_stage == "Production":
            deploy_version = res.version

    model_uri = client.get_model_version_download_uri(model_name, deploy_version)
    return model_uri
