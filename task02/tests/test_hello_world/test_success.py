import unittest
from src.lambdas.hello_world.handler import handle_request
from commons.exception import ApplicationException

class TestHelloWorld(unittest.TestCase):
    def test_success(self):
        event = {
            "path": "/hello",
            "httpMethod": "GET"
        }
        response = handle_request(event, dict())
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["message"], "Hello from Lambda")

    def test_bad_request(self):
        event = {
            "path": "/student_id",
            "httpMethod": "GET"
        }
        response = handle_request(event, dict())
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(
            response["message"],
            "Bad request syntax or unsupported method. Request path: /cmtr-5f9b79e5. HTTP method: GET"
        )

        event = {
            "path": "/hello",
            "httpMethod": "POST"
        }
        response = handle_request(event, dict())
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(
            response["message"],
            "Bad request syntax or unsupported method. Request path: /cmtr-5f9b79e5. HTTP method: GET"
        )

if __name__ == "__main__":
    unittest.main()
