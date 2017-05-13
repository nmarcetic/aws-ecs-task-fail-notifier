import requests
import json
from requests_aws_sign import AWSV4Sign
from boto3 import session, client
from elasticsearch import Elasticsearch, RequestsHttpConnection

# IMPORTANT: Change this values to fit your AWS account and Slack data
es_host = '' # Elasticsearch end point
sns_topic = '' # AWS SNS topic ARN
slack_webhookurl = "" # Slack webhook URL
slack_channel = '' # Slack channel where you want to bot post alerts
slack_username = ''  # Slack bot name
aws_region = '' # AWS region of your cluster

def lambda_handler(event, context):
    # Establish credentials
    session_var = session.Session()
    credentials = session_var.get_credentials()
    region = session_var.region_name or aws_region

    # Check to see if this event is a task event and, if so, if it contains
    # information about an event failure. If so, send an SNS notification.
    if "detail-type" not in event:
        raise ValueError("ERROR: event object is not a valid CloudWatch Logs event")
    else:
        if event["detail-type"] == "ECS Task State Change":
            detail = event["detail"]
            if detail["lastStatus"] == "STOPPED":
                if detail["stoppedReason"] == "Essential container in task exited":
                  # Send an error status message.
                  sns_client = client('sns')
                  sns_client.publish(
                      TopicArn=sns_topic,
                      Subject="ECS task failure detected for container",
                      Message=json.dumps(detail)
                  )

                  # Send msg to slack_webhookurl
                  url = slack_webhookurl
                  Subject="ECS task failure detected for container",
                  Message=json.dumps(detail)
                  messagedata = json.loads(Message)
                  # Break out Cloudwatch payload into variables that we use
                  taskArn = messagedata['taskArn']
                  desiredStatus = messagedata['desiredStatus']
                  lastStatus = messagedata['lastStatus']
                  stoppedReason = messagedata['stoppedReason']
                  clusterArn = messagedata['clusterArn']
                  # Get service name
                  serviceName = messagedata['containers'][0]['name']

                  taskDefinitionArn = messagedata['taskDefinitionArn']

                  #Only post to slack with specific data from cloudwatch ##
                  payload = {'channel': slack_channel, 'username': slack_username, 'text': '%s \n Task ARN: %s \n Desired Status: %s \n Last Status: %s \n Stopped Reason: %s \n Cluster ARN: %s \n Service: %s ' % (Subject, taskArn, desiredStatus, lastStatus, stoppedReason, clusterArn, serviceName ), 'icon_emoji': 'ghostwn:', 'username': slack_username, 'channel': slack_channel }
                  headers = {"content-type": "application/json" }
                  r = requests.put(url, data=json.dumps(payload), headers=headers)

                  print r.status_code
                  print r.content
                  note = "Post of data to slack was attempted"

    # Elasticsearch connection. Note that you must sign your requests in order
    # to call the Elasticsearch API anonymously. Use the requests_aws_sign
    # package for this.
    service = 'es'
    auth=AWSV4Sign(credentials, region, service)
    es_client = Elasticsearch(host=es_host,
                              port=443,
                              connection_class=RequestsHttpConnection,
                              http_auth=auth,
                              use_ssl=True,
                              verify_ssl=True)

    es_client.index(index="ecs-index", doc_type="eventstream", body=event)
