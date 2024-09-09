from aws_cdk import App, Environment
from watercycle.execution_role.stacks import ExecutionRoleStack

def execution_role_app():
    app = App()
    config = app.node.try_get_context("config")

    env = Environment(account=config["account"], region=config["region"])

    execution_role_stack = ExecutionRoleStack(
        app, "-".join([config["space"], config["execution_role"], "execution-role", "stack"]), 
        config=config, env=env
    )

    app.synth()
