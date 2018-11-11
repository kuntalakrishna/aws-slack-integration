import json
import logging
import os
from urllib2 import Request, urlopen, URLError, HTTPError
# Read environment variables
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
SLACK_USER = os.environ['SLACK_USER']
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    # Read message posted on SNS Topic
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))
# Construct a slack message
    slack_message = {
        'channel': SLACK_CHANNEL,
        'username': SLACK_USER,
        'text': "%s" % (message)
    }
# Post message on SLACK_WEBHOOK_URL
    req = Request(SLACK_WEBHOOK_URL, json.dumps(slack_message))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)