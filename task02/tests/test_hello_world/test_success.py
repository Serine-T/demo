import unittest
from src.lambdas.hello_world.handler import HelloWorld
from commons.exception import ApplicationException

class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        self.HANDLER = HelloWorld()

    def test_success(self):
        event = {
            'path': '/hello',
            'httpMethod': 'GET'
        }
        response = self.HANDLER.handle_request(event, dict())
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['message'], 'Hello from Lambda')  # Fixed message check

    def test_bad_request(self):
        event = {
            'path': '/student_id',
            'httpMethod': 'GET'
        }
        with self.assertRaises(ApplicationException) as context:
            self.HANDLER.handle_request(event, dict())

        self.assertEqual(context.exception.statusCode, 400)
        self.assertIn('Bad request syntax or unsupported method', context.exception.message['message'])

        event = {
            'path': '/hello',
            'httpMethod': 'POST'
        }
        with self.assertRaises(ApplicationException) as context:
            self.HANDLER.handle_request(event, dict())

        self.assertEqual(context.exception.statusCode, 400)
        self.assertIn('Bad request syntax or unsupported method', context.exception.message['message'])

if __name__ == '__main__':
    unittest.main()
