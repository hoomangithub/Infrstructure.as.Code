from aws_cdk import (
    Stack,
    aws_iam as _iam,
    aws_secretsmanager as _secretsmanager,
    aws_ssm as _ssm,
    SecretValue,
    RemovalPolicy,
    CfnOutput,
    Aws    
)
from constructs import Construct

class CustomIamUsersGroupsStack(Stack):

    def __init__(self, scope: Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Let us IAM Users & Groups
        user1_pass = _secretsmanager.Secret(
            self,
            "user1Pass",
            description="Password for User1",
            secret_name="user1_pass",
            removal_policy=RemovalPolicy.DESTROY
        )

        # Add User1 with SecretsManager Password
        user1 = _iam.User(
            self, 
            "user1",
            password=user1_pass.secret_value,
            user_name="user1"
        )
        ##############################################
        # Add User2 with Literal Password
        user2 = _iam.User(
            self, 
            "user2",
            password=SecretValue.unsafe_plain_text(
                "Dont-Use-B@d-Passw0rds"
            ),
            user_name="user2"
        )
        ##############################################
        # Add IAM Group
        konstone_group = _iam.Group(
            self,
            "konStoneGroup",
            group_name="konstone_group"
        )
        konstone_group.add_user(user1)
        ##############################################
        # Add Managed Policy to Group
        konstone_group.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
        )
        ##############################################
        # SSM parameter 1
        param1 = _ssm.StringParameter(
            self,
            "parameter1",
            description="Keys To KonStone",
            parameter_name="/konstone/keys/fish",
            string_value="0123456789",
            tier=_ssm.ParameterTier.STANDARD
        )

        # Grant Konstone group permission to Param 1
        param1.grant_read(konstone_group)
        ##############################################  
        # Grant Group to LIST ALL SSM Parameters in Console
        grpStmt1 = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ssm:DescribeParameters"
            ]
        )
        grpStmt1.sid = "DescribeAllParametersInConsole"

        # Add Permissions To Group
        konstone_group.add_to_policy(grpStmt1)
        ##############################################
        # Create IAM Role
        konstone_ops_role = _iam.Role(
            self,
            'konstoneOpsRole',
            assumed_by=_iam.AccountPrincipal(f"{Aws.ACCOUNT_ID}"),
            # '_iam.AccountPrincipal' add Trust relationships:
            # { "Version": "2012-10-17",
            #   "Statement": [{
            #      "Effect": "Allow",
            #      "Principal": {
            #          "AWS": "arn:aws:iam::006044462692:root"
            #      },
            #      "Action": "sts:AssumeRole"
            #   }]
            # }
            #
            role_name="konstone_ops_role"
        )

        # Create Managed Policy & Attach to Role
        list_ec2_policy = _iam.ManagedPolicy(
            self,
            "listEc2Instances",
            description="list ec2 isntances in the account",
            managed_policy_name="list_ec2_policy",
            statements=[
                _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW,
                    actions=[
                        "ec2:Describe*",
                        "cloudwatch:Describe*",
                        "cloudwatch:Get*"
                    ],
                    resources=["*"]
                )
            ],
            roles=[
                konstone_ops_role
            ]
        )
        ##############################################
        output_1 = CfnOutput(
            self,
            "user1LoginUrl",
            description="LoginUrl for User1",
            value=f"https://{Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
        )