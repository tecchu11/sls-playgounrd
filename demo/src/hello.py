import json

from aws_lambda_powertools import Logger

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    body = {"message": "hello", "input": event}

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
