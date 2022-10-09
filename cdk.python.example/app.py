#!/usr/bin/env python3

import aws_cdk as cdk

from resource_stacks.CustomParametersSecretsStack import CustomParametersSecretsStack
from resource_stacks.CustomIamUsersGroups import CustomIamUsersGroupsStack

app = cdk.App()
CustomParametersSecretsStack(app, "hooman-parameters-and-secrets")
CustomIamUsersGroupsStack(app, "hooman-iam-user-and-group")

app.synth()
