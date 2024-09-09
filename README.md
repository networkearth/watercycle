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

## CDK Reference

https://docs.aws.amazon.com/cdk/api/v2/python/
