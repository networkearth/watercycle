from copy import copy

from aws_cdk import (
    aws_lambda as _lambda,
    Stack,
)
from constructs import Construct

from watercycle.bucket.stacks import get_bucket_name
from watercycle.execution_role.stacks import get_role_name

def get_lambda_name(config: dict) -> str:
    return "-".join([config["space"], config["lambda_name"]])

class LambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_name = get_lambda_name(config)

        bucket_name = get_bucket_name(config)

        lambda_role_name = get_role_name(config)
        
        hello_lambda = _lambda.CfnFunction(
            self, lambda_name, function_name=lambda_name,
            runtime='python3.10',
            handler='function.handler',
            code={
                's3Bucket': bucket_name,
                's3Key': f"{config['lambda_name']}.zip",
            },
            memory_size=int(config["memory_size"]),
            role=f"arn:aws:iam::{config['account']}:role/{lambda_role_name}",
        )