from watercycle.jobs.stacks import get_job_name
from watercycle.utils import run_command

def build_image(config: dict) -> None:
    job_name = get_job_name(config)
    command = f"docker build --platform linux/amd64 -t {job_name}:latest ."
    run_command(command)

def push_image(config: dict) -> None:
    job_name = get_job_name(config)
    run_command(f"aws ecr get-login-password --region {config['region']} | docker login --username AWS --password-stdin {config['account']}.dkr.ecr.{config['region']}.amazonaws.com")
    run_command(f"docker tag {job_name}:latest {config['account']}.dkr.ecr.{config['region']}.amazonaws.com/{job_name}:latest")
    run_command(f"docker push {config['account']}.dkr.ecr.{config['region']}.amazonaws.com/{job_name}:latest")
