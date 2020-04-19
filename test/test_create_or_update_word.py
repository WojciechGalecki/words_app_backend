import pytest

from lambda_function import create_or_update_word as _lambda


# TODO mock dynamodb
def test_lambda_handler():
    # given
    event = {
        'body': '{"userId": "1", "word": "postman", "definitions": ["test1"]}'
    }

    expected_response = {
        'statusCode': 500,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': '{"error": "Unknown error occurred!"}'
    }

    # when
    actual_response = _lambda.lambda_handler(event, {})

    # then
    assert actual_response == expected_response
