import os

from lambda_functions.layers.http_response import create_response
from lambda_functions.layers.logger import logger
from lambda_functions.layers.dynamodb import dynamo_db


def lambda_handler(event, _) -> object:
    try:
        logger.info(f'Received an event: ${event}')
        query_params = event['queryStringParameters']
        validate_query_params(query_params)

        user_id = query_params['userId']
        word = query_params['word']

        logger.info(f'Deleting word: ${word} from user ${user_id} dictionary')
        table = dynamo_db.Table(os.environ['DYNAMODB_TABLE'])

        result = table.delete_item(
            Key={
                'userId': user_id,
                'word': word,
            },
            ReturnValues='ALL_OLD'
        )
        logger.info(f'Response from dynamo_db: ${result}')

        attributes = 'Attributes'
        if attributes not in result:
            return create_response(404)

        logger.info(f'Successfully deleted item: ${attributes}')
        return create_response(200)
    except ValueError:
        return create_response(400, {'error': 'Missing required parameters: userId, word'})
    except Exception as err:
        logger.error(err)
        return create_response(500, {'error': 'Unknown error occurred!'})


def validate_query_params(params: object):
    if (params is not None and all(key in params for key in ('userId', 'word'))) is False:
        raise ValueError
