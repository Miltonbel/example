import uuid
from flask import Blueprint, jsonify, request
from ..database.database import db


from ..services.route_service import RouteService
from ..services.user_service import UserService

route_blueprint = Blueprint('route', __name__)

@route_blueprint.route('/routes', methods=['POST'])
def create():
    
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'No hay token en la solicitud'}), 403
    
    token = auth_header.split(' ')[1]
    if not is_valid_uuid(token):
        return jsonify({'message': 'El token no es válido o está vencido.'}), 401
    
    data = request.json
    route_service = RouteService()
    return route_service.create_route(data)

@route_blueprint.route('/routes', methods=['GET'])
def get_routes():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'message': 'No hay token en la solicitud'}), 403
    
    token = auth_header.split(' ')[1]
    if not is_valid_uuid(token):
        return jsonify({'message': 'El token no es válido o está vencido.'}), 401

    flight_id = request.args.get('flight')
    route_service = RouteService()
    try:
        routes = route_service.get_routes(flight_id)
        return jsonify(routes), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor"}), 500
    
@route_blueprint.route('/routes/<string:id>', methods=['GET'])
def get_route_by_id(id):
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'No hay token en la solicitud'}), 403
        
        token = auth_header.split(' ')[1]
        if not is_valid_uuid(token):
            return jsonify({'message': 'El token no es válido o está vencido.'}), 401
        route_service = RouteService()
        route = route_service.get_route_by_id(id)
        return jsonify(route), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except FileNotFoundError:
        return jsonify({"error": "El trayecto con ese id no existe"}), 404
    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor"}), 500

@route_blueprint.route('/routes/<string:id>', methods=['DELETE'])
def delete_route(id):
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'No hay token en la solicitud'}), 403
        
        token = auth_header.split(' ')[1]
        if not is_valid_uuid(token):
            return jsonify({'message': 'El token no es válido o está vencido.'}), 401
        route_service = RouteService()
        success = route_service.delete_route(id)
        if success:
            return jsonify({"msg": "el trayecto fue eliminado"}), 200
        else:
            return jsonify({"error": "El trayecto con ese id no existe"}), 404
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor"}), 500

def is_valid_uuid(id):
    try:
        user_service = UserService()
        return user_service.get_user_me(id)
    except ValueError:
        return False