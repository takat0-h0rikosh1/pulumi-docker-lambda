import json
import boto3
import requests
from config import SlackConfig
from dataclasses import dataclass

class SlackNotifier:
    def __init__(self, config: SlackConfig):
        self.config = config
        self.webhook_url = self._fetch_slack_webhook_url()

    def _fetch_slack_webhook_url(self) -> str:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager')
        secret_value = client.get_secret_value(SecretId=self.config.slack_webhook_url_secret)
        return json.loads(secret_value['SecretString'])[self.config.slack_webhook_url_secret_key]

    def send_message(self, message: str):
        if not self.config.slack_notify_enabled:
            print("Slack notification is disabled.")
            return

        response = requests.post(self.webhook_url, json={'text': message})
        if response.status_code != 200:
            raise ValueError(f"Slack notification failed: {response.content}")
        else:
            print("Slack notification sent successfully.")
