import click

from aws_cdk import App, Environment
from watercycle.environment.stacks import VPCStack, BatchStack, ECRStack

def environment_app():
    app = App()
    config = app.node.try_get_context("config")

    env = Environment(account=config["account"], region=config["region"])

    vpc_stack = VPCStack(app, "-".join([config["space"], "vpc", "stack"]), config=config, env=env)

    batch_stack = BatchStack(app, "-".join([config["space"], "batch", "stack"]), config=config, env=env)

    ecr_stack = ECRStack(app, "-".join([config["space"], "ecr", "stack"]), config=config, env=env)

    app.synth()
