from flask import Flask
from .extensions import api , db
from .views import ns

app = Flask(__name__)
# initialisation de la BD
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
# initialisation de restx
api.init_app(app)
db.init_app(app)
# ajout du namespace defini dans views
api.add_namespace(ns)