import yaml
import pulumi
import pulumi_aws as aws
from dataclasses import dataclass, field
from typing import Optional
from typing import List


@dataclass
class LambdaConfig:
    env: str
    query: str
    function_name: str
    slack_webhook_url_secret: str
    slack_webhook_url_secret_key: str
    slack_notify_enabled: bool
    box_dist_file_name: str
    box_dist_folder_id: int
    subnet_ids: List[str]
    security_group_ids: List[str]
    rds_connection_secret: str
    box_config_ssm_param: str
    cron: Optional[str] = None


@dataclass
class DockerConfig:
    app_src_path: str = "../lambda/app"
    docker_build_context: str = "../lambda"


@dataclass
class AppConfig:
    app_name: str
    base_app_name: str
    stack_name: str
    lambda_configs: List[LambdaConfig]
    docker_config: DockerConfig = field(default_factory=DockerConfig)
    aws_account_id: str = aws.get_caller_identity().account_id


class ConfigLoader:
    def __init__(self, yaml_file: str = f"config/{pulumi.get_stack()}.yaml"):
        with open(yaml_file, "r") as f:
            self.config = yaml.safe_load(f)
            self.stack_name = pulumi.get_stack()
            self.base_app_name = "rds-box-query-uploader"
            self.app_name = f"{self.stack_name}-{self.base_app_name}"

    def load_app_config(self) -> AppConfig:
        return AppConfig(
            app_name=self.app_name,
            base_app_name=self.base_app_name,
            stack_name=self.stack_name,
            lambda_configs=self.load_lambda_configs(),
        )

    def load_lambda_configs(self) -> List[LambdaConfig]:
        lambda_configs_raw = self.config.get("lambda_configs", [])
        return [
            LambdaConfig(
                env=self.config.get("env"),
                query=self._read_sql_from_file(item["sql_file"]),
                function_name=f"{self.app_name}-{item['subject']}",
                slack_webhook_url_secret=self.config.get("slack_webhook_url_secret"),
                slack_webhook_url_secret_key=item["slack_webhook_url_secret_key"],
                slack_notify_enabled=item["slack_notify_enabled"],
                box_dist_file_name=item["box_dist_file_name"],
                box_dist_folder_id=item["box_dist_folder_id"],
                subnet_ids=[self.config.get("subnet_id")],
                security_group_ids=[self.config.get("security_group_id")],
                rds_connection_secret=self.config.get("rds_connection_secret"),
                box_config_ssm_param=self.config.get("box_config_ssm_param"),
                cron=item.get("cron"),
            )
            for item in lambda_configs_raw
        ]

    def _read_sql_from_file(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            return file.read()
