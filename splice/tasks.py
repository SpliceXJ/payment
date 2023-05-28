import os
import json
import boto3
from splicePayments.celery import app


sqs = boto3.client('sqs', region_name='eu-north-1')


@app.task
def request_queue_messages() -> None:

    messages_dict: dict = sqs.receive_message(
        QueueUrl = os.getenv('AWS_QUEUE_URL') + 'testing',
        MaxNumberOfMessages = 10,
        
        # The duration (in seconds) that the received messages are 
        # hidden from subsequent retrieve requests after being retrieved
        VisibilityTimeout = 150,
        
        # The duration (in seconds) for which the call waits for 
        # a message to arrive in the queue before returning
        WaitTimeSeconds = 20,
        )

    # process responses here
    if 'Messages' in messages_dict.keys(): 
        messages: list = messages_dict['Messages']

        for message in messages:
            body = json.loads(message['Body'])
            try:
                # perform account task from body

                # acknoledge to the queue (delete message)
                response = sqs.delete_message(
                    QueueUrl = os.getenv('AWS_QUEUE_URL') + 'testing',
                    ReceiptHandle = body['ReceiptHandle'],
                    )
            except:
                pass 
