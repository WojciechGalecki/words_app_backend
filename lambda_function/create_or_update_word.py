import json
import logging
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamo_db = boto3.resource('dynamodb')

DYNAMODB_TABLE = 'DYNAMODB_TABLE'


def lambda_handler(event, _):
    try:
        logger.info(f'Received an event: ${event}')

        body = json.loads(event['body'])
        logger.info(f'Saving new definitions: {body}')

        user_id = body['userId']
        word = body['word']
        definitions = body['definitions']

        table = dynamo_db.Table(os.environ[DYNAMODB_TABLE])

        result = table.put_item(
            Item={
                'userId': user_id,
                'word': word,
                'definitions': definitions
            }
        )

        logger.info(f'Response from dynamo_db: ${result}')

        return create_response(200, None)

    except Exception as err:
        logger.error(err)
        return create_response(500, {'error': 'Unknown error occurred!'})


def create_response(status, body):
    if body is None:
        return {'statusCode': status}
    else:
        return {
            'statusCode': status,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(body)
        }
