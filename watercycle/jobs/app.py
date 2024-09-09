from aws_cdk import App, Environment
from watercycle.jobs.stacks import BatchJobStack

def job_app():
    app = App()
    config = app.node.try_get_context("config")

    env = Environment(account=config["account"], region=config["region"])

    batch_job_stack = BatchJobStack(
        app, "-".join([config["space"], config["job_name"], "fargate", "stack"]), 
        config=config, env=env
    )

    app.synth()
