from tests.test_hello_world import HelloWorldLambdaTestCase


class TestSuccess(HelloWorldLambdaTestCase):
    def test_success(self):
        event = {
            'path': '/hello',
            'httpMethod': 'GET'
        }
        response = self.HANDLER.handle_request(event, dict())
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], '{"message": "Hello from Lambda"}')

    def test_bad_request(self):
        event = {
            'path': '/student_id',
            'httpMethod': 'GET'  
        }
        response = self.HANDLER.handle_request(event, dict())
        self.assertEqual(response['statusCode'], 400)
        self.assertTrue('Bad request syntax or unsupported method' in response['body'])
        
        event = {
            'path': '/hello',
            'httpMethod': 'POST' 
        }
        response = self.HANDLER.handle_request(event, dict())
        self.assertEqual(response['statusCode'], 400)
        self.assertTrue('Bad request syntax or unsupported method' in response['body'])