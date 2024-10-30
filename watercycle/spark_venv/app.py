import boto3

from watercycle.utils import run_command

def build_spark_venv(config):
    run_command("docker build --output . .")

    s3 = boto3.resource('s3')
    bucket = f"{config['space']}-{config['bucket']}"
    key = f"spark-venv/{config['application_name']}/{config['name']}.tar.gz"

    s3.Bucket(bucket).upload_file("pyspark_ge.tar.gz", key)