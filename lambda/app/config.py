import os
from dataclasses import dataclass
import boto3
import json
from typing import Dict, Any


@dataclass
class RDSConfig:
    query: str
    host: str
    port: int
    username: str
    password: str
    database: str


@dataclass
class BoxConfig:
    jwt_config: Dict[str, Any]
    box_dist_file_name: str
    box_dist_folder_id: int


@dataclass
class SlackConfig:
    slack_webhook_url_secret: str
    slack_webhook_url_secret_key: str
    slack_notify_enabled: bool


class ConfigLoader:
    def __init__(self):
        self.session = boto3.session.Session()
        self.env = os.environ.get("ENV")
        self.query = os.environ.get("QUERY")
        self.slack_webhook_url_secret = os.environ.get("SLACK_WEBHOOK_URL_SECRET")
        self.slack_webhook_url_secret_key = os.environ.get("SLACK_WEBHOOK_URL_SECRET_KEY")
        self.slack_notify_enabled = bool(os.environ.get("SLACK_NOTIFY_ENABLED"))
        self.box_dist_file_name = os.environ.get("BOX_DIST_FILE_NAME")
        self.box_dist_folder_id = int(os.environ.get("BOX_DIST_FOLDER_ID", 0))
        self.box_config_ssm_param = os.environ.get("BOX_CONFIG_SSM_PARAM")
        self.rds_secret_name = os.environ.get("RDS_CONNECTION_SECRET")

    def load_slack_config(self) -> SlackConfig:
        slack_notify_env = os.environ.get("SLACK_NOTIFY_ENABLED", "").lower()
        return SlackConfig(
            slack_webhook_url_secret=self.slack_webhook_url_secret,
            slack_webhook_url_secret_key=self.slack_webhook_url_secret_key,
            slack_notify_enabled=False if slack_notify_env == "false" else bool(slack_notify_env),
        )

    def load_rds_config(self) -> RDSConfig:
        client = self.session.client(service_name="secretsmanager")
        secret_value = client.get_secret_value(SecretId=self.rds_secret_name)
        secret_data = json.loads(secret_value["SecretString"])

        return RDSConfig(
            query=self.query,
            host=os.environ.get("MYSQL_HOST", "host.docker.internal")
            if self.env == "local"
            else secret_data.get("host"),
            port=int(os.environ.get("MYSQL_TCP_PORT", "3306"))
            if self.env == "local"
            else secret_data.get("port"),
            username=secret_data.get("username"),
            password=secret_data.get("password"),
            database=secret_data.get("dbName"),
        )

    def load_box_config(self) -> BoxConfig:
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(Name=self.box_config_ssm_param, WithDecryption=True)
        return BoxConfig(
            jwt_config=json.loads(parameter["Parameter"]["Value"]),
            box_dist_file_name=self.box_dist_file_name,
            box_dist_folder_id=self.box_dist_folder_id,
        )
