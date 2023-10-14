import unittest
from flask import Flask
from src.controllers.ping import ping_blueprint
import unittest


class TestPing(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(ping_blueprint)
        self.client = self.app.test_client()
    
    def test_ping_route(self):
        # Arrange               
        # Act
        response = self.client.get('/routes/ping')
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "pong")

if __name__ == '__main__':
    unittest.main()