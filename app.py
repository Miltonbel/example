from src.database.database import db
from flask import Flask
from src.controllers.ping import ping_blueprint
from src.controllers.reset import reset_blueprint
from src.controllers.route import route_blueprint
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(ping_blueprint)
app.register_blueprint(reset_blueprint)
app.register_blueprint(route_blueprint)
db.create_all()
#app.run(debug=True) 
