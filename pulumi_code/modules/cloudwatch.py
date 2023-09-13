from pulumi_aws import cloudwatch, lambda_


def create_cloudwatch_events(lambda_function_arn, lambda_name, cron):
    event_rule_name = f"{lambda_name}"
    event_target_name = f"{lambda_name}"

    event_rule = cloudwatch.EventRule(
        event_rule_name,
        schedule_expression=cron,
    )

    cloudwatch.EventTarget(
        event_target_name,
        rule=event_rule.name,
        arn=lambda_function_arn,
    )

    lambda_.Permission(
        f"allow-cloudwatch-event-trigger-{lambda_name}",
        action="lambda:InvokeFunction",
        function=lambda_function_arn,
        principal="events.amazonaws.com",
    )
