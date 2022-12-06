
from aws_cdk import (
    Stack,
    aws_sns as _sns,
    aws_sns_subscriptions as _subs,
    aws_sqs as _sqs,
    Duration,
    CfnOutput
)
from constructs import Construct

class CustomSNSandSQS(Stack):

    def __init__(self, scope: Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create SNS Topic
        hooman_topic = _sns.Topic(
            self,
            "hoomanHotTopics",
            display_name="Latest topics on Hooman",
            topic_name="hoomanHotTopic"
        )

        # Add Subscription to SNS Topic
        hooman_topic.add_subscription(
            _subs.EmailSubscription("humi222@hotmail.com")
        )
        
        # Create hooman Hot SQS Queue):
        hooman_Queue = _sqs.Queue(
            self,
            "hoomanQueue",
            queue_name="hooman_queue.fifo",
            fifo=True,
            encryption=_sqs.QueueEncryption.KMS_MANAGED,
            retention_period=Duration.days(4),
            visibility_timeout=Duration.seconds(45)
        )