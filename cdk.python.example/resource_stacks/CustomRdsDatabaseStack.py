import json
from aws_cdk import (
    Duration,
    Stack,
    aws_rds as _rds,
    aws_ec2 as _ec2,
    aws_secretsmanager as _ssm,
    RemovalPolicy    
)
from constructs import Construct

class CustomRdsDatabaseStack(Stack):
    
    def __init__(self, scope: Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        default_vpc = _ec2.Vpc.from_lookup(self, "importedDefaultVPC", vpc_id="vpc-0905e462")
        
        #################################################
        # Security Group      
        postgresql_SG = _ec2.SecurityGroup(self, id="postgresql_SG", vpc=default_vpc, allow_all_outbound=True, description="security group for a RDS")
        postgresql_SG.add_ingress_rule(peer=_ec2.Peer.any_ipv4(), connection=_ec2.Port.tcp(5432), description="allow Postgresql traffic from anywhere")
        #################################################
        # Templated secret with username and password fields
        db_secret = _ssm.Secret(self, "DBSecret",
                    generate_secret_string=_ssm.SecretStringGenerator(
                        secret_string_template=json.dumps({"username": "hooman"}),
                        generate_string_key="password",
                        password_length=16,
                        exclude_punctuation=True
                    )
        )
        #################################################                
        # Create an RDS Database
        konstone_db = _rds.DatabaseInstance(
            self, "HoomanPostgreSQL",
            instance_identifier="Hooman-RDS-CDK",
            database_name="konstone_db",
            engine=_rds.DatabaseInstanceEngine.postgres(version=_rds.PostgresEngineVersion.VER_13_7),
            instance_type=_ec2.InstanceType.of(
                _ec2.InstanceClass.T3,
                _ec2.InstanceSize.MICRO
            ),
            credentials=_rds.Credentials.from_secret(db_secret, username="username"),
            publicly_accessible=True,
            vpc=default_vpc,
            vpc_subnets=_ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PUBLIC),
            port=5432,
            allocated_storage=20,
            security_groups=[postgresql_SG],
            multi_az=False,
            #cloudwatch_logs_exports=["audit", "error", "general", "slowquery"],
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,
            delete_automated_backups=True,
            backup_retention=Duration.days(7) 
        )
