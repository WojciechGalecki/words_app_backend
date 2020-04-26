import pytest

from lambda_functions import delete_word as _lambda


def test_lambda_handler():
    # no dynamodb mocking - when error from boto3 client expect Internal Server Error
    # given
    event = {
        'queryStringParameters': {
            "userId": "1",
            "word": "test"
        }
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

    # when no required query parameters expect Bad Request
    # given
    event = {
        'queryStringParameters': None
    }

    expected_response = {
        'statusCode': 400,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': '{"error": "Missing required parameters: userId, word"}'
    }

    # when
    actual_response = _lambda.lambda_handler(event, {})

    # then
    assert actual_response == expected_response


def test_validate_query_params():
    # when no parameters expect ValueError
    with pytest.raises(ValueError):
        _lambda.validate_query_params(None)

    # when only one required parameters expect ValueError
    with pytest.raises(ValueError):
        _lambda.validate_query_params({'userId': 'test'})

    # when all parameters expect no response
    actual_response = _lambda.validate_query_params({'userId': 'test', 'word': 'test'})

    # then
    assert actual_response is None
