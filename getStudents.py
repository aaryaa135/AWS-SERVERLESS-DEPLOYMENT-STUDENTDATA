import json
import boto3

def lambda_handler(event, context):
    # Correct region for your setup
    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')

    # DynamoDB table
    table = dynamodb.Table('studentData')

    # Scan table
    response = table.scan()
    data = response['Items']

    # Pagination handling
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    # Return properly formatted API Gateway response
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        },
        "body": json.dumps(data)
    }
