import json
import os

from libs.httpResponse import create_response
from libs.logger import logger
from libs.dynamodb import dynamo_db


def lambda_handler(event, _) -> object:
    try:
        logger.info(f'Received an event: ${event}')

        body = json.loads(event['body'])
        logger.info(f'Saving new definitions: {body}')

        user_id = body['userId']
        word = body['word']
        definitions = body['definitions']

        table = dynamo_db.Table(os.environ['DYNAMODB_TABLE'])

        result = table.put_item(
            Item={
                'userId': user_id,
                'word': word,
                'definitions': definitions
            }
        )

        logger.info(f'Response from dynamo_db: ${result}')

        return create_response(200)

    except Exception as err:
        logger.error(err)
        return create_response(500, {'message': 'Unknown error occurred!'})
