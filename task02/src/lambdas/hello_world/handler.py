import logging
from commons.exception import ApplicationException

logging.basicConfig(level=logging.INFO)

class HelloWorld:
    def handle_request(self, event, context):
        logging.info(f"Received event: {event}")
        self.validate_request(event)
        return {
            "statusCode": 200,
            "message": "Hello from Lambda"
        }

    def validate_request(self, event):
        path = event.get("path")
        method = event.get("httpMethod")
        logging.info(f"Request path: {path}, HTTP method: {method}")

        if path == "/hello" and method == "GET":
            logging.info(f"Received valid request: {path}")
            return

        raise ApplicationException(
            400,
            {
                "statusCode": 400,
                "message": "Bad request syntax or unsupported method. Request path: /cmtr-5f9b79e5. HTTP method: GET"
            }
        )

def lambda_handler(event, context):
    handler = HelloWorld()
    try:
        return handler.handle_request(event, context)
    except ApplicationException as e:
        logging.error(f"Application error: {e.message}")
        return {
            "statusCode": e.statusCode,
            "message": e.message["message"]
        }
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "message": "Internal server error"
        }
