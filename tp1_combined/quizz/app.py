

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = "8e202471-f369-40b7-a917-516553e1b4c3"
cors = CORS(app , resources ={r"/todo/api/v1.0/*": {"origins": "*"}})

bootstrap = Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///db.sqllite') 
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"