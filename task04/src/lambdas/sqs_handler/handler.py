import json
import boto3

def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    
    print("AWS SDK (boto3) is available in Lambda environment.")
    
    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'SDK loaded successfully'})
    }
