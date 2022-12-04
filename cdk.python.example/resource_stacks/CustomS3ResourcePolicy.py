from aws_cdk import (
    Stack,
    aws_s3 as _s3,
    aws_iam as _iam  ,
    RemovalPolicy  
)
from constructs import Construct

class CustomS3ResourcePolicyStack(Stack):
    
    def __init__(self, scope: Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create an S3 Bucket
        hooman_bkt = _s3.Bucket(
            self,
            "hooman-s3.resource-policy",
            bucket_name="hoomans3resourcepolicy",
            versioned=False,
            # encryption=_s3.BucketEncryption.S3_MANAGED,
            # block_public_access=_s3.BlockPublicAccess.BLOCK_ALL,            
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # Add Bucket Resource policy
        hooman_bkt.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=[hooman_bkt.arn_for_objects("*.html")],
                principals=[_iam.AnyPrincipal()]
            )
        )

        hooman_bkt.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.DENY,
                actions=["s3:*"],
                resources=[f"{hooman_bkt.bucket_arn}/*"],
                principals=[_iam.AnyPrincipal()],
                conditions={ 
                    "Bool": {"aws:SecureTransport": False}
                }
            )
        )        