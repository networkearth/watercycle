# watercycle
for deploying apps to the cloud

## First Time Setup

```bash
nvm install 22
pip install .
```

## Running Deployments

### Logging Into AWS

```bash
aws sso configure
watercycle login <profile>
export AWS_PROFILE=<profile>
```

### Order of Operations

1. Deploy environment (defines your `scope`)
2. Deploy the execution-role (defines your `execution-role`)
3. Deploy your job
4. Deploy your container (note for this you have to be working on a machine with docker running)

## CDK Reference

https://docs.aws.amazon.com/cdk/api/v2/python/
