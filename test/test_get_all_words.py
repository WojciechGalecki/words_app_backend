import pytest

from lambda_function import get_all_words as _lambda


def test_lambda_handler():
    # no dynamodb mocking - when error from boto3 client expect Internal Server Error
    # given
    event = {
        'queryStringParameters': {
            "userId": "1"
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
        'body': '{"error": "Missing required parameter: userId"}'
    }

    # when
    actual_response = _lambda.lambda_handler(event, {})

    # then
    assert actual_response == expected_response


def test_validate_query_params():
    # when no required parameter expect ValueError
    with pytest.raises(ValueError):
        _lambda.validate_query_params(None)

    # when required parameter expect expect no response
    actual_response = _lambda.validate_query_params({'userId': 'test'})

    # then
    assert actual_response is None


def test_transform_items():
    # given
    items = [
        {'userId': '1', 'test': 'test'},
        {'userId': '1', 'foo': 'bar'}
    ]

    expected_items = [
        {'test': 'test'},
        {'foo': 'bar'}
    ]

    # when
    actual_items = _lambda.transform_items(items)

    # then
    assert actual_items == expected_items