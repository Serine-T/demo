from tests.test_hello_world import HelloWorldLambdaTestCase


class TestSuccess(HelloWorldLambdaTestCase):
    def test_success(self):
        # Mocking a valid event for the /hello GET request
        event = {
            'path': '/hello',
            'httpMethod': 'GET'
        }
        # Call the Lambda handler and assert the successful response
        response = self.HANDLER.handle_request(event, dict())
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], '{"message": "Hello from Lambda"}')

    def test_bad_request(self):
        # Mocking an invalid event with a different path
        event = {
            'path': '/student_id',  # Invalid path
            'httpMethod': 'GET'  # Valid method, but the path is invalid
        }
        # Call the Lambda handler and assert the error response
        response = self.HANDLER.handle_request(event, dict())
        self.assertEqual(response['statusCode'], 400)
        self.assertTrue('Bad request syntax or unsupported method' in response['body'])
        
        # Mocking an invalid event with a different HTTP method
        event = {
            'path': '/hello',
            'httpMethod': 'POST'  # Invalid method, should be GET
        }
        # Call the Lambda handler and assert the error response
        response = self.HANDLER.handle_request(event, dict())
        self.assertEqual(response['statusCode'], 400)
        self.assertTrue('Bad request syntax or unsupported method' in response['body'])