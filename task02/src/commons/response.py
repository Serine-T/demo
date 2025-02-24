from commons.exception import ApplicationException

RESPONSE_OK_CODE = 200
RESPONSE_BAD_REQUEST_CODE = 400

def build_response(content, code=200):
    if code == RESPONSE_OK_CODE:
        return {
            'statusCode': code,
            'message': content
        }
    raise ApplicationException(code=code, content=content)

def raise_error_response(code, content):
    raise ApplicationException(code=code, content=content)
