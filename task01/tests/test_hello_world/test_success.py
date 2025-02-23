from tests.test_hello_world import HelloWorldLambdaTestCase


class TestSuccess(HelloWorldLambdaTestCase):

    def test_success(self):
        # Now inside the method, self is valid
        response = self.HANDLER.handle_request(dict(), dict())
        
        # Check the response structure
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['message'], 'Hello from Lambda')