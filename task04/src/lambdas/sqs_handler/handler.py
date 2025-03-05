import json

def lambda_handler(event, context):
    print("Received event: ", json.dumps(event, indent=2))

    for record in event['Records']:
        sqs_message = record['body']  # Extracting message body
        print(f"Message received from SQS: {sqs_message}")

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'SQS message processed successfully'})
    }
