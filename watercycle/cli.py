import os
import json
import subprocess

import click 

from watercycle.environment.app import environment_app

# pylint: disable=missing-function-docstring
@click.group()
def cli():
    pass

@cli.command()
@click.argument("deploy_type", type=click.Choice(["environment", "job"]))
def synth(deploy_type):
    if deploy_type == "environment":
        environment_app()
    elif deploy_type == "job":
        pass

@cli.command()
def deploy():
    os.system("cdk deploy *-vpc-stack")
    os.system("cdk deploy *-ecr-stack")
    os.system("cdk deploy *-batch-stack")

@cli.command()
@click.argument("profile")
def login(profile):
    creds = json.loads(subprocess.getoutput(f'aws configure export-credentials --profile {profile}'))
    with open('/root/.aws/credentials', 'w') as f:
        f.write(f'[{profile}]\n')
        f.write(f'aws_access_key_id = {creds["AccessKeyId"]}\n')
        f.write(f'aws_secret_access_key = {creds["SecretAccessKey"]}\n')
        f.write(f'aws_session_token = {creds["SessionToken"]}\n')
