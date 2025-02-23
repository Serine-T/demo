from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger(__name__)


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        """
        Validate the incoming request and return the required data or an error message.
        """
        path = event.get('path', '')
        method = event.get('httpMethod', '')

        if path == '/hello' and method == 'GET':
            return None  # No error, continue with processing
        else:
            return {
                'statusCode': 400,
                'body': f"Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}"
            }
        
    def handle_request(self, event, context):
        """
        Handle the incoming event and return a valid response or an error message.
        """
        validation_response = self.validate_request(event)
        if validation_response:
            return validation_response  # Return the error response if validation fails

        # Business logic for the /hello GET request
        return {
            'statusCode': 200,
            'body': '{"message": "Hello from Lambda"}'
        }

    

HANDLER = HelloWorld()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
