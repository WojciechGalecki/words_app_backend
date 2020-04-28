import os

from boto3.dynamodb.conditions import Key
from layers.httpResponse import create_response
from layers.logger import logger
from layers.dynamodb import dynamo_db


def lambda_handler(event, _) -> object:
    try:
        logger.info(f'Received an event: ${event}')
        query_params = event['queryStringParameters']
        validate_query_params(query_params)

        user_id = query_params['userId']

        logger.info(f'Getting all words for user ${user_id}')
        table = dynamo_db.Table(os.environ['DYNAMODB_TABLE'])

        result = table.query(
            KeyConditionExpression=Key('userId').eq(user_id)
        )
        logger.info(f'Successfully retrieved all words for user: ${user_id}')
        transformed_items = transform_items(result['Items'])
        return create_response(200, transformed_items)

    except ValueError:
        return create_response(400, {'message': 'Missing required parameter: userId'})
    except Exception as err:
        logger.error(err)
        return create_response(500, {'message': 'Unknown error occurred!'})


def transform_items(items: list) -> list:
    for i in items:
        del i['userId']

    return items


def validate_query_params(params: object):
    if (params is not None and 'userId' in params) is False:
        raise ValueError
