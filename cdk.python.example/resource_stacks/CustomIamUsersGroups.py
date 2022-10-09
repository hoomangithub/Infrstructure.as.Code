from aws_cdk import (
    Stack,
    aws_iam as _iam,
    aws_secretsmanager as _secretsmanager,
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

        # Add User2 with Literal Password
        user2 = _iam.User(
            self, 
            "user2",
            password=SecretValue.unsafe_plain_text(
                "Dont-Use-B@d-Passw0rds"
            ),
            user_name="user2"
        )

        # Add IAM Group
        konstone_group = _iam.Group(
            self,
            "konStoneGroup",
            group_name="konstone_group"
        )
        konstone_group.add_user(user2)

        output_1 = CfnOutput(
            self,
            "user2LoginUrl",
            description="LoginUrl for User2",
            value=f"https://{Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
        )