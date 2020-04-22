import json


def create_response(status: int, body: object = None) -> object:
    if body:
        return {
            'statusCode': status,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(body)
        }
    return {'statusCode': status}
