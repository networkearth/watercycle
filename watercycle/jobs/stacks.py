from aws_cdk import (
    aws_batch as batch,
    aws_ecr as ecr,
    Stack
)
from constructs import Construct

from watercycle.execution_role.stacks import get_role_name

def get_job_name(config: dict) -> str:
    return "-".join([config["space"], config["job_name"]])

class BatchJobStack(Stack):
    def __init__(self, scope: Construct, stack_id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        job_name = get_job_name(config)

        repository = ecr.CfnRepository(
            self, job_name + "-ecr",
            repository_name=job_name
        )

        vcpu_property = batch.CfnJobDefinition.ResourceRequirementProperty(
            type="VCPU",
            value=config["vcpu"]
        )

        memory_property = batch.CfnJobDefinition.ResourceRequirementProperty(
            type="MEMORY",
            value=config["memory"]
        )

        ephemeral_storage_property = batch.CfnJobDefinition.EphemeralStorageProperty(
            size_in_gib=int(config["ephemeral_storage"])
        )

        fargate_platform_configuration_property = batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
            platform_version="1.4.0"
        )

        job_role_name = get_role_name(config)

        container_properties = batch.CfnJobDefinition.ContainerPropertiesProperty(
            image=f"{config['account']}.dkr.ecr.{config['region']}.amazonaws.com/{job_name}:latest",
            resource_requirements=[vcpu_property, memory_property],
            ephemeral_storage=ephemeral_storage_property,
            execution_role_arn=f"arn:aws:iam::{config['account']}:role/{job_role_name}",
            job_role_arn=f"arn:aws:iam::{config['account']}:role/{job_role_name}",
            fargate_platform_configuration=fargate_platform_configuration_property,
            network_configuration=batch.CfnJobDefinition.NetworkConfigurationProperty(
                assign_public_ip="ENABLED"
            )
        )

        _batch_job = batch.CfnJobDefinition(
            self, job_name,
            job_definition_name=job_name,
            type="container",
            container_properties=container_properties,
            platform_capabilities=["FARGATE"]
        )
