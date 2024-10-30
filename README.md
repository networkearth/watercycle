# watercycle
Cloud development kit gives us a way to define our infrastructure as code. 
Normally that code comprises roughly three parts. 

1. A Stack (python)
2. An App (python)
3. Context and Configuration (json + python)

`watercycle` makes life easier by allowing you to ignore the stack and app and just focus on the configuration.
Once your configuration is setup (see below) you can run `watercycle deploy <deployment>` and it will take care of the rest.

## First Time Setup

```bash
nvm install 22
pip install .
```

## Logging Into AWS

```bash
aws sso configure
export AWS_PROFILE=<profile>
watercycle login <profile>
```

## Deployments

All deployments have the follow these (3) steps:

1. Create a directory for your deployment
2. Fill out configuration
3. Run `watercycle deploy <deployment>`

The following just describe what configuration needs to be provided. 

### Environment

Fill out a `cdk.json` like the following:

```json
{
    "app": "watercycle synth environment",
    "context": {
        "config": {
            "account": "575101084097",
            "region": "us-east-1",
            "space": "watercycle-example",
            "max_vcpus": 64
        }
    }
}
```

The `space` should be treated as a namespace. Everything else in your environment is going to refer
to this in one way or another. The `max_vcpus` is the maximum number of vcpus that can be used in
your environment. You can always come back and change `max_vcpus` later.

This will create an environment with the name `<space>-environment`. The environment consists of a VPC,
a security group, batch compute environment, and a job queue.

### Execution Role

Fill out a `cdk.json` like the following:

```json
{
    "app": "watercycle synth execution-role",
    "context": {
        "config": {
            "account": "575101084097",
            "region": "us-east-1",
            "space": "watercycle-example",
            "execution_role": "example-role",
            "databases": ["example"],
            "buckets": ["example-bucket"],
            "run_batch": true
        }
    }
}
```

`databases` are which `haven` databases you want to give access to. `buckets` are which `s3` buckets. Note that the names should be whatever comes after the `space` you've chosen. so in the example above we are actually giving access to `watercycle-example-example-bucket`. `run_batch` is whether or not you want to be able to run batch jobs.

This will create an execution role with the name `<space>-<execution_role>`.

### Bucket

Fill out a `cdk.json` like the following:

```json
{
    "app": "watercycle synth bucket",
    "context": {
        "config": {
            "account": "575101084097",
            "region": "us-east-1",
            "space": "watercycle-example",
            "bucket_name": "bucket"
        }
    }
}
```

This will create a bucket `<space>-<bucket_name>`. 

### Job 

Fill out a `cdk.json` like the following:

```json
{
    "app": "watercycle synth job",
    "context": {
        "config":{
            "space": "watercycle-example",
            "job_name": "example-batch-job",
            "memory": "2048",
            "vcpu": "1",
            "ephemeral_storage": "21",
            "account": "575101084097",
            "region": "us-east-1",
            "execution_role": "example-role"
        }
        
    }
}
```

`memory` is the amount of memory in MB, `vcpu` is the number of vcpus, and `ephemeral_storage` is the amount of storage in GB. You'll get a job of the name `<space>-<job_name>`. Note that the execution role should only 
include the part of the role name that comes after the `space`.

In addition to building a job definition this will also build an ECR repository for your container.

Note this is just a job definition, to complete building a batch job you'll need to deploy a container as well.

### Container

In the same directory as the `cdk.json` of your job you'll create a Dockerfile whose entry point is your application (see the example in `watercycle/examples/job`).

Then on an instance with access to docker you'll run:

```bash
watercycle deploy container
```

Which will build and deploy the image. Note that you can only do this after you've deployed the job. 

### Lambda 

Fill out a `cdk.json` like the following:

```json
{
    "app": "watercycle synth lambda",
    "context": {
        "config": {
            "account": "575101084097",
            "region": "us-east-1",
            "space": "watercycle-example",
            "lambda_name": "hello-world",
            "bucket_name": "bucket",
            "memory_size": "128",
            "execution_role": "example-role"
        }
    }
}
```

`memory_size` is the amount of memory in MB. You'll get a lambda of the name `<space>-<lambda_name>`. Note that the `execution_role` should only be the part of the role name that comes after the `space`. `bucket_name` is the name of the bucket where the lambda code is stored.

In addition to the `cdk.json` described above you'll also need to create a `function.py` file like the following:

```python
def handler(event, context):
    print("Hello, CDK!")
    return {
        'statusCode': 200,
        'body': 'Hello, World!'
    }
```

whatever is in `handler` will be the entry point for your lambda.

### EMR (Elastic Map Reduce Application)

Fill out a `config.json` like the following:

```json
{
    "name": "watercycle-example",
    "max_vcpus": 8,
    "max_memory": 32,
    "max_disk": 100
}
```

`name` is the name of the application. `max_vcpus` is the maximum number of vcpus that can be used in the application. `max_memory` is the maximum amount of memory in GB. `max_disk` is the maximum amount of disk space in GB.

This will create an EMR application with the name `<name>`.

Note that recreating an application actually deletes the old application and creates a new one.

### Spark Venv

Fill out a `config.json` like the following:

```json
{
    "application_name": "watercycle-example",
    "space": "watercycle-example",
    "bucket": "bucket",
    "name": "example-venv"
}
```

`application_name` is the name of the application. `space` is the namespace. `bucket` is the name of the bucket where the virtual environment is stored. `name` is the name of the virtual environment.

Then update the dockerfile in the examples to include what you want in your venv. Then watercycle will build 
and export the venv to the bucket.

## Submissions

All submissions have the follow these (3) steps:

1. Create a directory for your submission
2. Fill out configuration
3. Run `watercycle submit <deployment>`

The following just describe what configuration needs to be provided. 

### Spark (Job)

You'll need to fill out a `config.json` like the following:

```json
{
    "account": "575101084097",
    "application_name": "watercycle-example",
    "space": "watercycle-example",
    "execution_role": "example-role",
    "bucket": "bucket",
    
    "name": "example-spark-job",
    "entrypoint": "wordcount.py",
    "arguments": ["s3://watercycle-example-bucket/spark/output"],
    "venv": "example-venv"
}
```

`account` is the account number. `application_name` is the name of the application. `space` is the namespace. `execution_role` is the name of the execution role. `bucket` is the name of the bucket where the job is stored. `name` is the name of the job. `entrypoint` is the entrypoint for the job. `arguments` are the arguments to the job. `venv` is the name of the virtual environment to use. 

You'll also need the file pointed to by `entrypoint` in the same directory as the `config.json`. And that file
will contain your actual spark job code. 

Upon submission, `watercycle` will put your entrypoint code into the bucket at `spark/<application_name>/<name>/` and then
submit the job to the EMR application. 
