#!/usr/bin/env python3

import aws_cdk as cdk

from resource_stacks.CustomParametersSecretsStack import CustomParametersSecretsStack
from resource_stacks.CustomIamUsersGroups import CustomIamUsersGroupsStack
from resource_stacks.CustomS3ResourcePolicy import CustomS3ResourcePolicyStack

app = cdk.App()
# CustomParametersSecretsStack(app, "hooman-parameters-and-secrets")
# CustomIamUsersGroupsStack(app, "hooman-iam-user-and-group")
#CustomS3ResourcePolicyStack(app, "hooman-s3-resource-policy")


app.synth()
