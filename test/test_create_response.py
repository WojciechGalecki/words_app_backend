from lambda_function.create_response import create_response


def test_create_response():
    # when no body expect only given status code
    expected_response = {'statusCode': 200}

    actual_response = create_response(200)

    assert actual_response == expected_response

    # when body expect proper json response
    expected_response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': '{"test": "test"}'
        }

    actual_response = create_response(200, {'test': 'test'})

    assert actual_response == expected_response
