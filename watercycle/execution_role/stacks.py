from aws_cdk import (
    aws_iam as iam,
    Stack,
)
from constructs import Construct

def get_role_name(config: dict) -> str:
    return "-".join([config["space"], config["execution_role"]])

class ExecutionRoleStack(Stack):
    def __init__(self, scope: Construct, stack_id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, stack_id, **kwargs)

        role_name = get_role_name(config)

        execution_role = iam.Role(
            self, role_name, role_name=role_name,
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
                iam.ServicePrincipal("batch.amazonaws.com"),
                iam.ServicePrincipal("ecs.amazonaws.com"),
                iam.ServicePrincipal("lambda.amazonaws.com"),
                iam.ServicePrincipal("emr-serverless.amazonaws.com"),
            )
        )

        if config.get("run_batch", False):
            execution_role.add_to_policy(
                iam.PolicyStatement(
                    actions=[
                        "batch:SubmitJob",
                    ],
                    resources=["*"]
                )
            )

        execution_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "ecr:GetAuthorizationToken",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=["*"]
            )
        )

        for bucket in config.get("buckets", []):
            bucket_name = "-".join([config["space"], bucket])
            execution_role.add_to_policy(
                iam.PolicyStatement(
                    actions=[
                        "s3:*",
                    ],
                    resources=[f"arn:aws:s3:::{bucket_name}*"]
                )
            )

        if config.get("databases", []):
            execution_role.add_to_policy(
                iam.PolicyStatement(
                    actions=[
                        "glue:*",
                    ],
                    resources=["*"]
                )
            )
            execution_role.add_to_policy(
                iam.PolicyStatement(
                    actions=[
                        "athena:*",
                    ],
                    resources=["*"]
                )
            )
            execution_role.add_to_policy(
                iam.PolicyStatement(
                    actions=[
                        "s3:*",
                    ],
                    resources=["arn:aws:s3:::aws-athena-query-results*"]
                )
            )
            for database in config["databases"]:
                execution_role.add_to_policy(
                    iam.PolicyStatement(
                        actions=[
                            "s3:*",
                        ],
                        resources=[f"arn:aws:s3:::{database}-database*"]
                    )
                )

        if config.get("run_emr", False):
            execution_role.add_to_policy(
                iam.PolicyStatement(
                    actions=[
                        "s3:GetObject",
                        "s3:ListBucket"
                    ],
                    resources=[
                        "arn:aws:s3:::*.elasticmapreduce",
                        "arn:aws:s3:::*.elasticmapreduce/*"
                    ]
                )
            )

            execution_role.add_to_policy(
                iam.PolicyStatement(
                    actions=[
                        "glue:GetDatabase",
                        "glue:CreateDatabase",
                        "glue:GetDataBases",
                        "glue:CreateTable",
                        "glue:GetTable",
                        "glue:UpdateTable",
                        "glue:DeleteTable",
                        "glue:GetTables",
                        "glue:GetPartition",
                        "glue:GetPartitions",
                        "glue:CreatePartition",
                        "glue:BatchCreatePartition",
                        "glue:GetUserDefinedFunctions"
                    ],
                    resources=["*"]
                )
            )

        for arn in config.get("bucket_arns", []):
            execution_role.add_to_policy(
                iam.PolicyStatement(
                    actions=[
                        "s3:*",
                    ],
                    resources=[f"{arn}*"]
                )
            )
