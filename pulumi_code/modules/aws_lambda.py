from pulumi_aws import lambda_
from modules.config import LambdaConfig


def create_lambda_function(image, lambda_role, config: LambdaConfig) -> any:
    return lambda_.Function(
        config.function_name,
        name=config.function_name,
        image_uri=image.image_name,
        role=lambda_role.arn,
        package_type="Image",
        memory_size=1024,
        timeout=300,
        vpc_config=lambda_.FunctionVpcConfigArgs(
            subnet_ids=config.subnet_ids,
            security_group_ids=config.security_group_ids,
        ),
        environment={
            "variables": {
                "ENV": config.env,
                "QUERY": config.query,
                "SLACK_WEBHOOK_URL_SECRET": config.slack_webhook_url_secret,
                "SLACK_WEBHOOK_URL_SECRET_KEY": config.slack_webhook_url_secret_key,
                "SLACK_NOTIFY_ENABLED": str(config.slack_notify_enabled),
                "BOX_DIST_FILE_NAME": config.box_dist_file_name,
                "BOX_DIST_FOLDER_ID": str(config.box_dist_folder_id),
                "RDS_CONNECTION_SECRET": config.rds_connection_secret,
                "BOX_CONFIG_SSM_PARAM": config.box_config_ssm_param,
            }
        }
    )
