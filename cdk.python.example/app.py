#!/usr/bin/env python3

import aws_cdk as cdk

from resource_stacks.CustomParametersSecretsStack import CustomParametersSecretsStack


app = cdk.App()
CustomParametersSecretsStack(app, "cdk-python-example")

app.synth()
