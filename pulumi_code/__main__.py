from modules.ecr import build_and_push_ecr_image
from modules.iam import create_iam_role_and_policy
from modules.aws_lambda import create_lambda_function
from modules.cloudwatch import create_cloudwatch_events
from modules.config import ConfigLoader


config_loader = ConfigLoader()
app_config = config_loader.load_app_config()

image = build_and_push_ecr_image(app_config)
iam_role = create_iam_role_and_policy(app_config)
lambda_configs = app_config.lambda_configs

for _, config in enumerate(lambda_configs):
    lambda_function = create_lambda_function(
        image, 
        iam_role, 
        config
    )
    
    if config.cron:
        create_cloudwatch_events(
            lambda_function.arn,
            config.function_name,
            config.cron)
