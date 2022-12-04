from aws_cdk import (
    Stack,
    aws_ec2 as _ec2,
    aws_iam as _iam,
    aws_ssm as _ssm,
    CfnOutput,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_elasticloadbalancingv2_targets as _elbtarget
)
from constructs import Construct

class CustomSimpleEc2Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        default_vpc = _ec2.Vpc.from_lookup(self, "importedDefaultVPC", vpc_id="vpc-0905e462")
        
        vpc_id_from_ssm = _ssm.StringParameter.value_from_lookup(self, parameter_name="/VpcProvider/VPCID")
        imported_webServer_vpc = _ec2.Vpc.from_lookup(self, "importedWebServerVPC", vpc_id=vpc_id_from_ssm)
        
        used_VPC = imported_webServer_vpc
        #################################################
        # Webserver IAM Role
        web_server_role = _iam.Role(self, "webServerRoleId",
            assumed_by=_iam.ServicePrincipal('ec2.amazonaws.com'),
            managed_policies=[
                _iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'),
                _iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3ReadOnlyAccess')
            ]
        )        
        #################################################
        # Read BootStrap Script
        try:
            with open("resource_stacks/scripts/simpleEc2InstallHttpd.sh", mode="r") as file:
                installHttpd = file.read()
        except OSError:
            print('Unable to read bootstrap script')
        #################################################
        # Security Group      
        webserver_SG = _ec2.SecurityGroup(self, id="simpleEc2-1_SG", vpc=used_VPC, allow_all_outbound=True, description="security group for a web server")
        webserver_SG.add_ingress_rule(peer=_ec2.Peer.any_ipv4(), connection=_ec2.Port.tcp(22), description="allow SSH traffic from anywhere")
        webserver_SG.add_ingress_rule(peer=_ec2.Peer.any_ipv4(), connection=_ec2.Port.tcp(80), description="allow HTTP traffic from anywhere")
        webserver_SG.add_ingress_rule(peer=_ec2.Peer.any_ipv4(), connection=_ec2.Port.tcp(443), description="allow HTTPS traffic from anywhere")
        #################################################        
        # WebServer Instance
        linux_ami = _ec2.AmazonLinuxImage(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            virtualization=_ec2.AmazonLinuxVirt.HVM,
            storage=_ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )        
        web_server = _ec2.Instance(
            self, "simpleEc2-1", 
            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="SimpleEc2-1",
            # machine_image=_ec2.MachineImage.generic_linux({"eu-central-1": "ami-076309742d466ad69"}),
            machine_image=linux_ami,
            vpc=used_VPC,
            vpc_subnets=_ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PUBLIC),
            role=web_server_role,
            security_group=webserver_SG,
            user_data=_ec2.UserData.custom(installHttpd)
        )
        #################################################
        # Create Application Load Balancer
        alb = _elbv2.ApplicationLoadBalancer(
            self, "myAlbId",
            vpc=used_VPC,
            internet_facing=True,
            load_balancer_name="WebServerAlb"
        )
        alb.connections.allow_from_any_ipv4(_ec2.Port.tcp(80), description="Allow Internet access on ALB Port 80")
        # listener.connections.allow_default_port_from_any_ipv4("Open to the world")
        web_server.connections.allow_from(alb, _ec2.Port.tcp(80), description="Allows ASG Security Group receive traffic from ALB")
        # Add Listerner to ALB
        listener = alb.add_listener("Listener", port=80, open=True)
        listener.add_targets("Target", port=80, targets=[
            _elbtarget.InstanceIdTarget(instance_id=web_server.instance_id, port=80)]
        )
        #################################################
        output_webserver_1 = CfnOutput(
            self, "SimpleEc2-1_Ip",
            description="Simple Ec2 Webserver Public Ip Address",
            value=f"http://{web_server.instance_public_ip}"
        )
        # Output of the ALB Domain Name
        output_ApplicationLoadBalancer = CfnOutput(
            self, "albDomainName",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Web Server ALB Domain Name"
        )    