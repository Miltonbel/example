import os
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import uuid
from sqlalchemy import create_engine
from src.controllers.route import route_blueprint
from src.models.route import Route
from flask import Flask, jsonify
import json
from src.database import database


class TestRoute(unittest.TestCase):

    def setUp(self):
        os.environ['is_test'] = 'True'
        self.engine = create_engine('sqlite:///:memory:')
        database.db.create_all()
        self.session = database.db.Session()

        self.app = Flask(__name__)
        self.app.register_blueprint(route_blueprint)
        self.client = self.app.test_client()
        valid_uuid = 'c4bbabb1-0000-0000-0000-000000000000'
        self.headers = {'Authorization': f'Bearer {valid_uuid}'}

    def tearDown(self):
        self.session.close()
        database.db.drop_all()

    def test_create_invalid_token(self):
        # Arrange               
        invalid_uuid = 'invalid_uuid'
        headers = {'Authorization': f'Bearer {invalid_uuid}'}
        # Act
        response = self.client.post('/routes', headers=headers)
        # Assert
        self.assertEqual(response.status_code, 401) 

    def test_create_empty_token(self):
        # Arrange 
        # Act
        response = self.client.post('/routes')
        
        self.assertEqual(response.status_code, 403) 


    @patch('src.services.user_service.UserService.get_user_me',
           return_value= ("ok", 200))
    def test_create_route_success(self, mock_user):
        # Arrange
        # Act
        response = self.client.post('/routes', json={
            "flightId": "FL123",
            "sourceAirportCode": "ABC",
            "sourceCountry": "CountryA",
            "destinyAirportCode": "XYZ",
            "destinyCountry": "CountryB",
            "bagCost": 50,
            "plannedStartDate": (datetime.now() + timedelta(days=1)).isoformat(),
            "plannedEndDate": (datetime.now() + timedelta(days=2)).isoformat()
        }, headers=self.headers)

        data = json.loads(response.data)
        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertTrue("id" in data)
        self.assertTrue("createdAt" in data)
    @patch('src.services.user_service.UserService.get_user_me',
           return_value= ("ok", 200))
    def test_create_route_missing_fields(self, mock_user):
        # Arrange
        # Act
        response = self.client.post('/routes', json={
            "sourceAirportCode": "ABC",
            "sourceCountry": "CountryA",
            "destinyAirportCode": "XYZ",
            "destinyCountry": "CountryB",
            "bagCost": 50,
            "plannedStartDate": (datetime.now() - timedelta(days=1)).isoformat(),
            "plannedEndDate": (datetime.now() + timedelta(days=1)).isoformat()
        }, headers=self.headers)
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json, {'error': "El campo 'flightId' es obligatorio"})
    @patch('src.services.user_service.UserService.get_user_me',
           return_value= ("ok", 200))
    def test_create_route_flightId_exists(self, mock_user):
        # Arrange
        # Act
        response1 = self.client.post('/routes', json={
            "flightId": "FL123",
            "sourceAirportCode": "ABC",
            "sourceCountry": "CountryA",
            "destinyAirportCode": "XYZ",
            "destinyCountry": "CountryB",
            "bagCost": 50,
            "plannedStartDate": (datetime.now() + timedelta(days=1)).isoformat(),
            "plannedEndDate": (datetime.now() + timedelta(days=2)).isoformat()
        }, headers=self.headers)

        response = self.client.post('/routes', json={
            "flightId": "FL123",
            "sourceAirportCode": "ABC",
            "sourceCountry": "CountryA",
            "destinyAirportCode": "XYZ",
            "destinyCountry": "CountryB",
            "bagCost": 50,
            "plannedStartDate": (datetime.now() + timedelta(days=1)).isoformat(),
            "plannedEndDate": (datetime.now() + timedelta(days=2)).isoformat()
        }, headers=self.headers)
        # Assert
        self.assertEqual(response.status_code, 412)
        self.assertEqual(response.json, {"msg": "El flightId ya existe"})

    @patch('src.services.user_service.UserService.get_user_me',
           return_value= ("ok", 200))
    def test_create_route_invalid_dates(self, mock_user):
        # Arrange 
        # Act
        response = self.client.post('/routes', json={
            "flightId": "FL123",
            "sourceAirportCode": "ABC",
            "sourceCountry": "CountryA",
            "destinyAirportCode": "XYZ",
            "destinyCountry": "CountryB",
            "bagCost": 50,
            "plannedStartDate": (datetime.now() - timedelta(days=1)).isoformat(),
            "plannedEndDate": (datetime.now() + timedelta(days=1)).isoformat()
        }, headers=self.headers)
        # Assert
        self.assertEqual(response.status_code, 412)
        self.assertEqual(
            response.json, {"msg": "Las fechas del trayecto no son válidas"})

    def test_get_routes_invalid_token(self):
        # Arrange 
        invalid_uuid = 'invalid_uuid'
        headers = {'Authorization': f'Bearer {invalid_uuid}'}
        # Act
        response = self.client.get('/routes', headers=headers)
        # Assert
        self.assertEqual(response.status_code, 401) 


    def test_get_routes_empty_token(self):
        # Arrange
        # Act
        response = self.client.get('/routes')
        # Assert
        self.assertEqual(response.status_code, 403) 
    @patch('src.services.user_service.UserService.get_user_me',
    return_value= ("ok", 200))
    def test_get_routes_without_flight_id(self, mock_user):
        # Arrange 
        new_route = Route(
            str(uuid.uuid4()),
            "ABC123",
            "AAA",
            "AAA",
            "BBB",
            "AAA",
            50,
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        )
        new_route1 = Route(
            str(uuid.uuid4()),
            "DEF456",
            "CCC",
            "AAA",
            "DDD",
            "AAA",
            50,
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        )
        self.session.add(new_route)
        self.session.add(new_route1)
        self.session.commit()
        # Act
        response = self.client.get('/routes', headers=self.headers)
        response_dict = json.loads(response.text)
        # Assert
        self.assertEqual(len(response_dict), 2)
        self.assertEqual(response_dict[0]["flightId"], "ABC123")
        self.assertEqual(response_dict[1]["flightId"], "DEF456")

    @patch('src.services.user_service.UserService.get_user_me',
    return_value= ("ok", 200))
    def test_get_routes_with_valid_flight_id(self, mock_user):
        # Arrange 
        new_route = Route(
            str(uuid.uuid4()),
            "XYZ789",
            "AAA",
            "AAA",
            "BBB",
            "AAA",
            50,
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        )
        new_route1 = Route(
            str(uuid.uuid4()),
            "DEF456",
            "CCC",
            "AAA",
            "DDD",
            "AAA",
            50,
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        )
        self.session.add(new_route)
        self.session.add(new_route1)
        self.session.commit()
        # Act
        response = self.client.get('/routes?flight=XYZ789', headers=self.headers)
        response_dict = json.loads(response.text)
        # Assert
        self.assertEqual(len(response_dict), 1)
        self.assertEqual(response_dict[0]["flightId"], "XYZ789")

    @patch('src.services.user_service.UserService.get_user_me',
        return_value= ("ok", 200))
    def test_get_routes_with_invalid_flight_id(self, mock_user):
        # Arrange
        # Act
        response = self.client.get('/routes?flight=InvalidFlightId', headers=self.headers)
        # Assert
        self.assertEqual(response.status_code, 200)

    def test_get_routes_by_invalid_token(self):
        # Arrange 
        invalid_uuid = 'invalid_uuid'
        headers = {'Authorization': f'Bearer {invalid_uuid}'}        
        guid = str(uuid.uuid4())
        # Act
        response = self.client.get(f'/routes/{guid}', headers=headers)
        # Assert
        self.assertEqual(response.status_code, 401) 

    def test_get_routes_by_empty_token(self):
        # Arrange 
        guid = str(uuid.uuid4())
        # Act
        response = self.client.get(f'/routes/{guid}')
        # Assert
        self.assertEqual(response.status_code, 403) 
    @patch('src.services.user_service.UserService.get_user_me',
        return_value= ("ok", 200))
    def test_get_route_by_valid_id(self, mock_user):
        # Arrange 
        guid = str(uuid.uuid4())
        new_route = Route(
            guid,
            "XYZ789",
            "AAA",
            "AAA",
            "BBB",
            "AAA",
            50,
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        )
        self.session.add(new_route)
        self.session.commit()
        # Act
        route_data = self.client.get(f'/routes/{guid}', headers=self.headers)
        response_dict = json.loads(route_data.text)
        # Assert
        self.assertEqual(response_dict["id"], guid)
        self.assertEqual(response_dict["flightId"], "XYZ789")

    @patch('src.services.user_service.UserService.get_user_me',
        return_value= ("ok", 200))
    def test_get_route_by_invalid_id(self, mock_user):
        # Arrange 
        guid = 'f4409575-07e1-4bc0-b5f8-3eba16442446'
        new_route = Route(
            str(uuid.uuid4()),
            "XYZ789",
            "AAA",
            "AAA",
            "BBB",
            "AAA",
            50,
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        )
        self.session.add(new_route)
        self.session.commit()
        # Act
        route_data = self.client.get(f'/routes/{guid}', headers=self.headers)
        # Assert
        self.assertEqual(route_data.status_code, 404)

    @patch('src.services.user_service.UserService.get_user_me',
        return_value= ("ok", 200))
    def test_get_route_by_not_exist_id(self, mock_user):
        # Arrange 
        guid = str(32)
        new_route = Route(
            guid,
            "XYZ789",
            "AAA",
            "AAA",
            "BBB",
            "AAA",
            50,
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        )
        self.session.add(new_route)
        self.session.commit()
        # Act
        route_data = self.client.get(f'/routes/{guid}', headers=self.headers)
        # Assert
        self.assertEqual(route_data.status_code, 400)

    def test_delete_invalid_token(self):
        # Arrange 
        invalid_uuid = 'invalid_uuid'
        headers = {'Authorization': f'Bearer {invalid_uuid}'}        
        guid = str(uuid.uuid4())
        # Act
        response = self.client.delete(f'/routes/{guid}', headers=headers)
        
        self.assertEqual(response.status_code, 401) 

    def test_delete_empty_token(self):
        # Arrange 
        guid = str(uuid.uuid4())
        # Act
        response = self.client.delete(f'/routes/{guid}')
        # Assert
        self.assertEqual(response.status_code, 403) 

    @patch('src.services.user_service.UserService.get_user_me',
        return_value= ("ok", 200))
    def test_delete_route_with_valid_id(self, mock_user):
        # Arrange 
        guid = str(uuid.uuid4())
        new_route = Route(
            guid,
            "XYZ789",
            "AAA",
            "AAA",
            "BBB",
            "AAA",
            50,
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        )
        self.session.add(new_route)
        self.session.commit()
        # Act
        route_data = self.client.delete(f'/routes/{guid}', headers=self.headers)
        # Assert
        self.assertTrue(route_data)
        self.assertEqual(route_data.status_code,200)

    @patch('src.services.user_service.UserService.get_user_me',
        return_value= ("ok", 200))
    def test_delete_route_with_invalid_id(self, mock_user):
        # Arrange 
        guid = str(32)
        new_route = Route(
            str(uuid.uuid4()),
            "XYZ789",
            "AAA",
            "AAA",
            "BBB",
            "AAA",
            50,
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        )
        self.session.add(new_route)
        self.session.commit()
        # Act
        route_data = self.client.delete(f'/routes/{guid}', headers=self.headers)
        # Assert
        self.assertEqual(route_data.status_code,400)

    @patch('src.services.user_service.UserService.get_user_me',
        return_value= ("ok", 200))
    def test_delete_route_with_not_exist_id(self, mocke_user):
        # Arrange 
        guid = str(uuid.uuid4())
        new_route = Route(
            str(uuid.uuid4()),
            "XYZ789",
            "AAA",
            "AAA",
            "BBB",
            "AAA",
            50,
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        )
        self.session.add(new_route)
        self.session.commit()
        # Act
        route_data = self.client.delete(f'/routes/{guid}', headers=self.headers)
        # Assert
        self.assertEqual(route_data.status_code,404)
       
if __name__ == '__main__':
    unittest.main()
