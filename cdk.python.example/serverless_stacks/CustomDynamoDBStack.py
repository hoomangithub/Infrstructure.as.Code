from aws_cdk import (
    Stack,
    aws_dynamodb as _dynamodb,
    RemovalPolicy
)
from constructs import Construct

class CustomDynamoDBStack(Stack):
    
    def __init__(self, scope: Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # DynamoDB: Key-Value Database
        
        konstone_assets_table = _dynamodb.Table(
            self,
            "konstoneAssetsDDBTable",
            table_name='Movies',
            partition_key=_dynamodb.Attribute(
                name='year',
                type=_dynamodb.AttributeType.NUMBER
            ),
            sort_key=_dynamodb.Attribute(
                name='title',
                type=_dynamodb.AttributeType.STRING
            ),
            billing_mode=_dynamodb.BillingMode.PROVISIONED,
            read_capacity=1,
            write_capacity=1,
            encryption=_dynamodb.TableEncryption.DEFAULT,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        konstone_assets_table.add_global_secondary_index(
            index_name="MoviesInvertIndex",
            partition_key=_dynamodb.Attribute(
                name='title',
                type=_dynamodb.AttributeType.STRING
            ),
            sort_key=_dynamodb.Attribute(
                name='year',
                type=_dynamodb.AttributeType.NUMBER
            ),
            projection_type=_dynamodb.ProjectionType.ALL,
            read_capacity=1,
            write_capacity=1
        )