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
    outputs_dir = f"{prefix}/output"

    s3.Bucket(bucket).upload_file(config["entrypoint"], entrypoint_key)

    execution_role_arn = f"arn:aws:iam::{config['account']}:role/{get_role_name(config)}"

    response = client.start_job_run(
        applicationId=application_id,
        name=config['name'],
        executionRoleArn=execution_role_arn,
        jobDriver={
            'sparkSubmit': {
                'entryPoint': f"s3://{bucket}/{entrypoint_key}",
                'entryPointArguments': [f"s3://{bucket}/{outputs_dir}"],
                'sparkSubmitParameters': "--conf spark.executor.cores=1 --conf spark.executor.memory=4g --conf spark.driver.cores=1 --conf spark.driver.memory=4g --conf spark.executor.instances=1"
            },
        },
    )