#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.python.example.cdk.python.example_stack import CdkPythonExampleStack


app = cdk.App()
CdkPythonExampleStack(app, "cdk-python-example")

app.synth()
