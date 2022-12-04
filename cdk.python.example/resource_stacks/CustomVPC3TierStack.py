from aws_cdk import (
    Stack,
    aws_ec2 as _ec2,
    aws_ssm as _ssm,
    CfnOutput,   
)
from constructs import Construct

class CustomVPC3TierStack(Stack):
    def __init__(self, scope: Construct, id: str,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        cdk_config = self.node.try_get_context('vpc_configs')

        default_vpc = _ec2.Vpc.from_lookup(self, "importedDefaultVPC", vpc_id="vpc-0905e462")
        
        # Create a 3 tier vpc
        custom_vpc = _ec2.Vpc(
            self,
            "customVpcId",
            ip_addresses=_ec2.IpAddresses.cidr(cdk_config['vpc_cidr']),
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="public", cidr_mask=cdk_config['cidr_mask'], subnet_type=_ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name="app", cidr_mask=cdk_config['cidr_mask'], subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
                _ec2.SubnetConfiguration(
                    name="db", cidr_mask=cdk_config['cidr_mask'], subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
                )
            ]
        )
        
        # create an SSM parameters which store export VPC ID
        _ssm.StringParameter(
            self,
            "parameter1",
            description="export VPC ID",
            parameter_name="/VpcProvider/VPCID",
            string_value=custom_vpc.vpc_id,
            tier=_ssm.ParameterTier.STANDARD
        )
        
        CfnOutput(self, "customVpcIdOut", value=custom_vpc.vpc_id, export_name="customVpcIdOut")
        
        i = 0
        for sub in custom_vpc.select_subnets(subnet_group_name="public").subnets:
            i += 1
            subnetName = "SubnetPublic{}".format(str(i))
            CfnOutput(self,subnetName, value=sub.subnet_id, export_name=subnetName)
        
        i = 0
        for sub in custom_vpc.select_subnets(subnet_group_name="app").subnets:
            i += 1
            subnetName = "SubnetApp{}".format(str(i))
            CfnOutput(self,subnetName, value=sub.subnet_id, export_name=subnetName)
        i = 0
        for sub in custom_vpc.select_subnets(subnet_group_name="db").subnets:
            i += 1
            subnetName = "SubnetDb{}".format(str(i))
            CfnOutput(self,subnetName, value=sub.subnet_id, export_name=subnetName)
        
        
        peer_vpc = _ec2.CfnVPCPeeringConnection(
            self, 
            "peerVpnDefaultAndCustom", 
            peer_vpc_id=custom_vpc.vpc_id, 
            vpc_id=default_vpc.vpc_id
        )