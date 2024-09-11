import click

from aws_cdk import App, Environment
from watercycle.bucket.stacks import BucketStack

def bucket_app():
    app = App()
    config = app.node.try_get_context("config")

    env = Environment(account=config["account"], region=config["region"])

    bucket_stack = BucketStack(app, "-".join([config["space"], config["bucket_name"], "bucket", "stack"]), config=config, env=env)

    app.synth()
