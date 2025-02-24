import logging
from commons.exception import ApplicationException

# Configure logging
logging.basicConfig(level=logging.INFO)

class HelloWorld:
    def handle_request(self, event, context):
        logging.info(f"Received event: {event}")  # Log the incoming event
        self.validate_request(event)  # Validate the request
        return {
            'statusCode': 200,
            'message': 'Hello from Lambda'  # Ensure the correct message
        }

    def validate_request(self, event):
        path = event.get('path')
        method = event.get('httpMethod')
        logging.info(f"Request path: {path}, HTTP method: {method}")

        if path == '/hello' and method == 'GET':
            logging.info(f"Received valid request: {path}")
            return  # Valid request, no action needed

        # Raise an ApplicationException for invalid requests
        raise ApplicationException(
            400,
            {
                'statusCode': 400,
                'message': f'Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}'
            }
        )

def lambda_handler(event, context):
    handler = HelloWorld()
    try:
        return handler.handle_request(event, context)
    except ApplicationException as e:
        logging.error(f"Application error: {e.message}")
        return {
            'statusCode': e.statusCode,
            'message': e.message["message"]  # Ensure correct message formatting
        }
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'message': f"Internal server error: {str(e)}"
        }
