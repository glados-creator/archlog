from flask import Flask
from flask_cors import CORS
from .extensions import api , db
from .views import ns

app = Flask(__name__)

app.config['SECRET_KEY'] = "8e202471-f369-40b7-a917-516553e1b4c3"
### CORS
cors = CORS(app , resources =
            {"/api/v1.0.0/*": {"origins": "*"}}
            )

# initialisation de la BD
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
# initialisation de restx
api.init_app(app)
db.init_app(app)
# ajout du namespace defini dans views
api.add_namespace(ns)