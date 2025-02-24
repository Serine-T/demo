import logging
import json

def handle_request(event, context):
    try:
        path = event.get("path")
        method = event.get("httpMethod")

        if path == "/hello" and method == "GET":
            return {
                "statusCode": 200,
                "message": "Hello from Lambda"
            }

        return {
            "statusCode": 400,
            "message": "Bad request syntax or unsupported method. Request path: /cmtr-5f9b79e5. HTTP method: GET"
        }

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "message": "Internal server error"
        }

def lambda_handler(event, context):
    response = handle_request(event, context)
    return json.loads(json.dumps(response))  # Ensure correct JSON formatting
