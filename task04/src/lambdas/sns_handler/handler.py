import json

def lambda_handler(event, context):
    print("Received event: ", json.dumps(event, indent=2))

    for record in event['Records']:
        sns_message = record['Sns']['Message']
        print(f"Message received from SNS: {sns_message}")
    

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'SNS message processed successfully'})
    }
