from aws_cdk import (
    Stack,
    aws_ssm as _ssm,
    aws_secretsmanager as _secretsmanager,
    RemovalPolicy,
    CfnOutput    
)
from constructs import Construct

import json

class CustomParametersSecretsStack(Stack):

    def __init__(self, scope: Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Let us create AWS secrets & SSM Parameters
        param1 = _ssm.StringParameter(
            self,
            "parameter1",
            description="Load Testing Configuration",
            parameter_name="NoOfConcurrentUsers",
            string_value="100",
            tier=_ssm.ParameterTier.STANDARD
        )
        param2 = _ssm.StringParameter(
            self,
            "parameter2",
            description="Load Testing Configuration",
            parameter_name="/hooman/configs/NoOfConcurrentUsers",
            string_value="200",
            tier=_ssm.ParameterTier.STANDARD
        )
        param3 = _ssm.StringParameter(
            self,
            "parameter3",
            description="Load Testing Configuration",
            parameter_name="/hooman/configs/DurationInSec",
            string_value="300",
            tier=_ssm.ParameterTier.STANDARD
        )

        secret1 = _secretsmanager.Secret(
            self,
            "secret1",
            description="Customer DB password",
            secret_name="cust_db_pass",
            removal_policy=RemovalPolicy.DESTROY
        )

        templated_secret = _secretsmanager.Secret(
            self,
            "secret2",
            description="A Templated secret for user data",
            secret_name="user_hooman_attributes",
            generate_secret_string=_secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps(
                    {"username": "hooman"}
                ),
                generate_string_key="password"
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        output_1 = CfnOutput(
            self,
            "param1",
            description="NoOfConcurrentUser",
            value=f"{param1.string_value}"
        )
        output_2 = CfnOutput(
            self,
            "secret1Value",
            description="secret1",
            value=f"{secret1.secret_value}"
        )
