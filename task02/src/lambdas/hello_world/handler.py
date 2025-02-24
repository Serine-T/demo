import logging
from commons.exception import ApplicationException

logging.basicConfig(level=logging.INFO)

def handle_request(event, context):
    try:
        path = event.get("path")
        method = event.get("httpMethod")

        if path == "/hello" and method == "GET":
            return {
                "statusCode": 200,
                "message": "Hello from Lambda"
            }

        raise ApplicationException(
            400,
            {
                "statusCode": 400,
                "message": "Bad request syntax or unsupported method. Request path: /cmtr-5f9b79e5. HTTP method: GET"
            }
        )

    except ApplicationException as e:
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

lambda_handler = handle_request
