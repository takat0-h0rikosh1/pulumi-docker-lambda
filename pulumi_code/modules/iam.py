from pulumi_aws import iam
from modules.config import AppConfig


def create_iam_role_and_policy(config: AppConfig) -> any:
    lambda_role = iam.Role(
        config.app_name,
        assume_role_policy={
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Effect": "Allow",
                }
            ],
        },
        managed_policy_arns=[
            "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
        ],
    )

    iam.RolePolicy(
        "inlinePolicy",
        role=lambda_role.id,
        policy={
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "secretsmanager:GetSecretValue",
                    ],
                    "Resource": [
                        f"arn:aws:secretsmanager:ap-northeast-1:{config.aws_account_id}:secret:{config.stack_name}/{config.base_app_name}/*",
                    ],
                    "Effect": "Allow",
                },
                {
                    "Action": ["ssm:GetParameter"],
                    "Resource": [
                        f"arn:aws:ssm:ap-northeast-1:{config.aws_account_id}:parameter/{config.box_config_ssm_param}"
                    ],
                    "Effect": "Allow",
                },
                {
                    "Action": [
                        "ec2:CreateNetworkInterface",
                        "ec2:DescribeNetworkInterfaces",
                        "ec2:DeleteNetworkInterface",
                    ],
                    "Resource": "*",
                    "Effect": "Allow",
                },
            ],
        },
    )

    return lambda_role
