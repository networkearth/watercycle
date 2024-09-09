from aws_cdk import (
    aws_batch as batch,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    Stack,
)
from constructs import Construct


def get_vpc_name(config: dict) -> str:
    return "-".join([config["name"], "vpc"])

def get_compute_environment_name(config: dict) -> str:
    return "-".join([config["name"], "compute"])

def get_job_queue_name(config: dict) -> str:
    return "-".join([config["name"], "job", "queue"])

def get_repository_name(config: dict) -> str:
    return config["name"]


class VPCStack(Stack):

    def __init__(self, scope: Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc_name = get_vpc_name(config)

        vpc = ec2.Vpc(
            self, vpc_name,
            max_azs=2,  # Number of availability zones to use
            cidr="10.0.0.0/16",  # CIDR block for the VPC
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24  # Each public subnet will get a /24 block
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask=24  # Each private subnet will get a /24 block
                )
            ],
            nat_gateways=1  # Number of NAT gateways for the private subnets
        )


class BatchStack(Stack):
    def __init__(self, scope: Construct, stack_id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        vpc_name = get_vpc_name(config)

        vpc = ec2.Vpc.from_lookup(
            self,
            vpc_name,
            vpc_name=vpc_name
        )

        private_subnets = [
            subnet.subnet_id for subnet in vpc.private_subnets
        ]

        compute_environment_name = get_compute_environment_name(config)

        security_group_name = "-".join([compute_environment_name, "security-group"])
        security_group = ec2.SecurityGroup(
            self,
            security_group_name,
            vpc=vpc,
            allow_all_outbound=True,
        )

        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow SSH Access"
        )

        compute_environment = batch.CfnComputeEnvironment(
            self, 
            compute_environment_name,
            type="MANAGED",
            compute_environment_name=compute_environment_name,
            service_role=f"arn:aws:iam::{config['account']}:role/aws-service-role/batch.amazonaws.com/AWSServiceRoleForBatch",
            compute_resources=batch.CfnComputeEnvironment.ComputeResourcesProperty(
                type="FARGATE",
                security_group_ids=[security_group.security_group_id],
                subnets=private_subnets,
                maxv_cpus=config["max_vcpus"],
            )
        )

        job_queue_name = get_job_queue_name(config)
        job_queue = batch.CfnJobQueue(
            self, 
            job_queue_name,
            job_queue_name=job_queue_name,
            compute_environment_order=[
                batch.CfnJobQueue.ComputeEnvironmentOrderProperty(
                    compute_environment = compute_environment.ref, order=1
                )
            ],
            priority=1
        )

        job_queue.node.add_dependency(compute_environment)


class ECRStack(Stack):
    def __init__(self, scope: Construct, stack_id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        repository_name = get_repository_name(config)

        ecr.Repository(
            self,
            repository_name,
            repository_name=repository_name
        )
