from createOrUpdateWord import lambda_handler


def test_lambda_handler():
    # no dynamodb mocking - when error from boto3 client expect Internal Server Error
    # given
    event = {
        'body': '{"userId": "1", "word": "postman", "definitions": ["test1"]}'
    }

    expected_response = {
        'statusCode': 500,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': '{"message": "Unknown error occurred!"}'
    }

    # when
    actual_response = lambda_handler(event, {})

    # then
    assert actual_response == expected_response
