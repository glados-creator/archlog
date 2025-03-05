### template flask app.py from the template of templates for templating

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
### JWT ? bash giuud
app.config['SECRET_KEY'] = "8e202471-f369-40b7-a917-516553e1b4c3"
### CORS
cors = CORS(app , resources =
            {"/todo/api/v1.0/*": {"origins": "*"}
            ,"/quizz/api/v1.0/*": {"origins": "*"}}
            )

### bootstrap
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)
### SQLlite flask sql alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///db.sqllite') 
db = SQLAlchemy(app)

### login manager because there do still an mock user
login_manager = LoginManager(app)
login_manager.login_view = "login"