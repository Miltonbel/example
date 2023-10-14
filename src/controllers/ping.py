from flask import Blueprint

ping_blueprint = Blueprint('ping', __name__)

@ping_blueprint.route('/routes/ping', methods = ['GET'])
def ping():
    return "pong", 200