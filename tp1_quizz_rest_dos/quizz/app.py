

from flask import Flask
from flask_bootstrap import Bootstrap5
import os.path
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = "8e202471-f369-40b7-a917-516553e1b4c3"
bootstrap = Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///db.sqllite') 
db = SQLAlchemy(app)

