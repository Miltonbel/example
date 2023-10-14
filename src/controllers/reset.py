from flask import Blueprint, jsonify
from ..database.database import db
from ..models.route import Route
reset_blueprint = Blueprint('reset', __name__)

@reset_blueprint.route('/routes/reset', methods=['POST'])
def reset():
    session = get_session()
    session.query(Route).delete()
    session.commit()
    return jsonify({"msg": "Todos los datos fueron eliminados"}), 200

def get_session():
    return db.get_session()