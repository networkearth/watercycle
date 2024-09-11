import os
import json
import subprocess

import click 

from watercycle.environment.app import environment_app
from watercycle.jobs.app import job_app
from watercycle.jobs.docker import build_image, push_image
from watercycle.execution_role.app import execution_role_app
from watercycle.bucket.app import bucket_app
from watercycle._lambda.app import lambda_app, deploy_lambda_code

from watercycle.utils import run_command


# pylint: disable=missing-function-docstring
@click.group()
def cli():
    pass


@cli.command()
@click.argument("deploy_type", type=click.Choice(["environment", "job", "execution-role", "bucket", "lambda"]))
def synth(deploy_type):
    if deploy_type == "environment":
        environment_app()
    elif deploy_type == "job":
        job_app()
    elif deploy_type == "execution-role":
        execution_role_app()
    elif deploy_type == "bucket":
        bucket_app()
    elif deploy_type == "lambda":
        lambda_app()


@cli.command()
@click.argument("deploy_type", type=click.Choice(["environment", "job", "container", "execution-role", "bucket", "lambda"]))
def deploy(deploy_type):
    if deploy_type == "environment":
        run_command("cdk deploy *-vpc-stack")
        run_command("cdk deploy *-ecr-stack")
        run_command("cdk deploy *-batch-stack")
    elif deploy_type == "container":
        with open('cdk.json', 'r') as f:
            config = json.load(f)['context']['config']
        build_image(config)
        push_image(config)
    elif deploy_type in ["job", "execution-role", "bucket"]:
        run_command("cdk deploy")
    elif deploy_type == "lambda":
        deploy_lambda_code()
        run_command("cdk deploy")
        

@cli.command()
@click.argument("profile")
def login(profile):
    creds = json.loads(subprocess.getoutput(f'aws configure export-credentials --profile {profile}'))
    with open(os.path.expanduser('~/.aws/credentials'), 'w') as f:
        f.write(f'[{profile}]\n')
        f.write(f'aws_access_key_id = {creds["AccessKeyId"]}\n')
        f.write(f'aws_secret_access_key = {creds["SecretAccessKey"]}\n')
        f.write(f'aws_session_token = {creds["SessionToken"]}\n')
