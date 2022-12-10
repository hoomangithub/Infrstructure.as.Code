from aws_cdk import (
    Stack,
    aws_s3 as _s3,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    Duration,
    RemovalPolicy
)
from constructs import Construct

class CustomLambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Serverless Event Processor using Lambda
        
        # Import an S3 Bucket:
        # konstone_bkt = _s3.Bucket.from_bucket_attributes(self, "konstoneAssetsBucket", bucket_name="bucket-list-files")
        
        # Read Lambda Code
        try:
            with open("serverless_stacks/lambda_src/konstone_processor.py", mode="r") as f:
                konstone_fn_code = f.read()
        except OSError:
            print("Unable to read Lambda Function Code")

        lambda_role = _iam.Role(
            self,
            "LambdaRoleId",
            assumed_by=_iam.ServicePrincipal('lambda.amazonaws.com'), 
            managed_policies=[
                _iam.ManagedPolicy.from_managed_policy_arn(self, "AWSLambdaBasicExecutionRoleId", 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'),
                _iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),
                _iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')
            ]
        )

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html    
        konstone_fn = _lambda.Function(
            self,
            "konstoneFunction",
            function_name="konstone_function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(konstone_fn_code),
            # code=_lambda.S3Code(bucket=konstone_bkt, key="konstone_processor.zip"),
            memory_size=256,
            role=lambda_role,
            timeout=Duration.seconds(3),
            reserved_concurrent_executions=1,
            environment={
                "DYNAMODB_TABLE": "Movies",
                "LOG_LEVEL": "INFO"
            }
        )
    
        # Create Custom Loggroup
        konstone_lg = _logs.LogGroup(
            self,
            "konstoneLoggroup",
            log_group_name=f"/aws/lambda/{konstone_fn.function_name}",
            removal_policy=RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.ONE_DAY
        )