import re
import uuid
from flask import jsonify
from ..database.database import db
from ..models.route import Route
from datetime import datetime, timezone
from dateutil.parser import isoparse

class RouteService:

    def create_route(self, data):
        try:
            required_fields = ["flightId", "sourceAirportCode", "sourceCountry", "destinyAirportCode", "destinyCountry", "bagCost", "plannedStartDate", "plannedEndDate"]
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"El campo '{field}' es obligatorio"}), 400

            flight_id = data["flightId"]
            source_airport_code = data["sourceAirportCode"]
            source_country = data["sourceCountry"]
            destiny_airport_code = data["destinyAirportCode"]
            destiny_country = data["destinyCountry"]
            bag_cost = data["bagCost"]
            planned_start_date = isoparse(data["plannedStartDate"]).replace(tzinfo=timezone.utc)
            
            planned_end_date = isoparse(data["plannedEndDate"]).replace(tzinfo=timezone.utc)

            if planned_start_date >= planned_end_date or planned_start_date < datetime.now(timezone.utc):
                return jsonify({"msg": "Las fechas del trayecto no son válidas"}), 412

            session = db.get_session()
            _route = session.query(Route).filter(Route.flightId == flight_id).first()

            if _route:
                return jsonify({"msg": "El flightId ya existe"}), 412

            created_at = datetime.now()

            new_route = Route(
                str(uuid.uuid4()),
                flight_id,
                source_airport_code,
                source_country,
                destiny_airport_code,
                destiny_country,
                bag_cost,
                planned_start_date,
                planned_end_date,
                created_at,
                created_at
            )

            session.add(new_route)
            session.commit()
            return jsonify({"id": new_route.id, "createdAt": created_at.isoformat()}), 201

        except Exception as e:
            return jsonify({"error": "Ocurrió un error en el servidor"}), 500

    def get_routes(self, flight_id=None):
            try:
                if flight_id and not self.is_valid_flight_id(flight_id):
                    raise ValueError("El formato del flightId no es válido")
                
                session = db.get_session()
                if flight_id:
                    routes = session.query(Route).filter(Route.flightId == flight_id).all()
                else:
                    routes = session.query(Route).all()

                route_list = []
                for route in routes:
                    route_data = {
                        "id": route.id,
                        "flightId": route.flightId,
                        "sourceAirportCode": route.sourceAirportCode,
                        "sourceCountry": route.sourceCountry,
                        "destinyAirportCode": route.destinyAirportCode,
                        "destinyCountry": route.destinyCountry,
                        "bagCost": route.bagCost,
                        "plannedStartDate": route.plannedStartDate,
                        "plannedEndDate": route.plannedEndDate,
                        "createdAt": route.createdAt.isoformat()
                    }
                    route_list.append(route_data)

                return route_list

            except Exception as e:
                raise e
        
    def is_valid_flight_id(self, flight_id):
        if isinstance(flight_id, str):
            return True
        else:
            return False

    def is_valid_iata_code(self, code):
        iata_pattern = re.compile(r"^[A-Z]{3}$")
        return iata_pattern.match(code) is not None
    
    def get_route_by_id(self, id):
        try:
            if not self.is_valid_uuid(id):
                raise ValueError("El id no es un valor string con formato uuid")

            session = db.get_session()
            route = session.query(Route).filter(Route.id == id).first()

            if not route:
                raise FileNotFoundError

            route_data = {
                    "id": route.id,
                    "flightId": route.flightId,
                    "sourceAirportCode": route.sourceAirportCode,
                    "sourceCountry": route.sourceCountry,
                    "destinyAirportCode": route.destinyAirportCode,
                    "destinyCountry": route.destinyCountry,
                    "bagCost": route.bagCost,
                    "plannedStartDate": route.plannedStartDate.isoformat(),
                    "plannedEndDate": route.plannedEndDate.isoformat(),
                    "createdAt": route.createdAt.isoformat()
            }

            return route_data

        except Exception as e:
            raise e
    
    def is_valid_uuid(self, id):
        try:
            uuid_obj = uuid.UUID(id)
            return str(uuid_obj) == id
        except ValueError:
            return False
        
    def delete_route(self, id):
        try:
            if not self.is_valid_uuid(id):
                raise ValueError("El id no es un valor string con formato uuid")

            session = db.get_session()
            route = session.query(Route).filter(Route.id == id).first()

            if not route:
                return False

            session.delete(route)
            session.commit()
            return True

        except Exception as e:
            raise e