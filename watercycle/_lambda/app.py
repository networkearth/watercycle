import os
import json

from aws_cdk import App, Environment
from watercycle._lambda.stacks import LambdaStack
from watercycle.bucket.stacks import get_bucket_name
from watercycle.utils import run_command

def deploy_lambda_code():
    with open('cdk.json', 'r') as f:
        config = json.load(f)['context']['config']

    bucket_name = get_bucket_name(config)

    key = f"{config['lambda_name']}.zip"
    run_command(f"zip -r {key} function.py")
    run_command(f"aws s3 cp {key} s3://{bucket_name}")
    os.remove(key)

def lambda_app():
    app = App()
    config = app.node.try_get_context("config")

    env = Environment(account=config["account"], region=config["region"])

    lambda_stack = LambdaStack(
        app, "-".join([config["space"], config["lambda_name"], "lambda", "stack"]), 
        config=config, env=env
    )

    app.synth()
