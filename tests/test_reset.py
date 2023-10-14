import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from src.controllers.reset import reset_blueprint, get_session

class TestReset(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)      
        self.app.register_blueprint(reset_blueprint, url_prefix='') 
        self.client = self.app.test_client()
    
    @patch('src.controllers.reset.get_session')
    def test_reset(self, mock_Session):
        # Arrange 
        mock_session_instance = mock_Session.return_value
        mock_query_delete = mock_session_instance.query.return_value.delete
        mock_commit = mock_session_instance.commit
        # Act
        response = self.client.post('/routes/reset')
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"msg": "Todos los datos fueron eliminados"})

        mock_Session.assert_called_once()
        mock_query_delete.assert_called_once_with()
        mock_commit.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()