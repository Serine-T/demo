def handle_request(event, context):
    import json
    import logging

    logging.basicConfig(level=logging.INFO)
    logging.info(f"Received event: {json.dumps(event, indent=2)}")

    path = event.get("rawPath", "")
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    logging.info(f"Extracted path: {path}, method: {method}")

    if path.rstrip("/") == "/hello" and method == "GET":
        return {
            "statusCode": 200,
            "body": json.dumps({
                "statusCode": 200,
                "message": "Hello from Lambda"
            })
        }

    return {
        "statusCode": 400,
        "body": json.dumps({
            "statusCode": 400,
            "message": f"Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}"
        })
    }

def lambda_handler(event, context):
    return handle_request(event, context)
