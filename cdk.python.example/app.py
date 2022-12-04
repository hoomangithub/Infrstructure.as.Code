#!/usr/bin/env python3

import aws_cdk as cdk
from aws_cdk import (
    Environment
)

# from resource_stacks.CustomIamUsersGroups import CustomIamUsersGroupsStack
# from resource_stacks.CustomS3ResourcePolicy import CustomS3ResourcePolicyStack
# from resource_stacks.CustomParametersSecretsStack import CustomParametersSecretsStack

# from resource_stacks.CustomVPC3TierStack import CustomVPC3TierStack
# from resource_stacks.CustomSimpleEc2Stack import CustomSimpleEc2Stack

from resource_stacks.CustomRdsDatabaseStack import CustomRdsDatabaseStack

app = cdk.App()

env_configs = Environment(account=app.node.try_get_context('envs')['account'], region=app.node.try_get_context('envs')['region'])

# CustomIamUsersGroupsStack(app, "hooman-iam-user-and-group")
# CustomS3ResourcePolicyStack(app, "hooman-s3-resource-policy")
# CustomParametersSecretsStack(app, "hooman-parameters-and-secrets")

# CustomVPC3TierStack(app, "hooman-customVpc", env=env_configs)
# CustomSimpleEc2Stack(app, "simpleEc2", env=env_configs)

CustomRdsDatabaseStack(app, "RDS-POSTGRES", env=env_configs)

app.synth()
