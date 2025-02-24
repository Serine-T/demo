import unittest
import json
from src.lambdas.hello_world.handler import handle_request  # Update import to use handle_request directly

class TestHelloWorld(unittest.TestCase):
    def test_success(self):
        event = {
            'path': '/hello',
            'httpMethod': 'GET'
        }
        response = handle_request(event, {})
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['message'], 'Hello from Lambda')

    def test_bad_request(self):
        event = {
            'path': '/student_id',
            'httpMethod': 'GET'
        }
        response = handle_request(event, {})
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Bad request syntax or unsupported method', response['message'])

        event = {
            'path': '/hello',
            'httpMethod': 'POST'
        }
        response = handle_request(event, {})
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Bad request syntax or unsupported method', response['message'])

if __name__ == '__main__':
    unittest.main()
