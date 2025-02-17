import boto3

from ..execution_role.stacks import get_role_name

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless/client/start_job_run.html

def submit_spark_job(config):
    client = boto3.client('emr-serverless')
    response = client.list_applications()
    application_id = next(
        app['id'] for app in response['applications'] 
        if app['name'] == config['application_name']
    )

    s3 = boto3.resource('s3')
    bucket = f"{config['space']}-{config['bucket']}"
    prefix = f"spark/{config['application_name']}/{config['name']}"
    entrypoint_key = f"{prefix}/{config['entrypoint']}"

    s3.Bucket(bucket).upload_file(config["entrypoint"], entrypoint_key)

    execution_role_arn = f"arn:aws:iam::{config['account']}:role/{get_role_name(config)}"

    resource_conf = "--conf spark.executor.cores=4 --conf spark.executor.memory=16g --conf spark.driver.cores=4 --conf spark.driver.memory=16g --conf spark.executor.instances=1 --conf spark.dynamicAllocation.enabled=true --conf spark.dynamicAllocation.minExecutors=1"
    
    venv_key = f"spark-venv/{config['application_name']}/{config['venv']}.tar.gz"
    venv_conf = f"--conf spark.archives=s3://{bucket}/{venv_key}#environment --conf spark.emr-serverless.driverEnv.PYSPARK_DRIVER_PYTHON=./environment/bin/python --conf spark.emr-serverless.driverEnv.PYSPARK_PYTHON=./environment/bin/python --conf spark.executorEnv.PYSPARK_PYTHON=./environment/bin/python"

    jars_conf = f"--conf spark.jars=s3://{bucket}/jars/AthenaJDBC42-2.0.33.jar"

    response = client.start_job_run(
        applicationId=application_id,
        name=config['name'],
        executionRoleArn=execution_role_arn,
        jobDriver={
            'sparkSubmit': {
                'entryPoint': f"s3://{bucket}/{entrypoint_key}",
                'entryPointArguments': config["arguments"],
                'sparkSubmitParameters': ' '.join([resource_conf, venv_conf, jars_conf]),
            },
        },
    )