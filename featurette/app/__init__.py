from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://featurette:br1teCor3@localhost/featurette'
app.secret_key = 'br1teCor3'
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
db = SQLAlchemy(app)

from app import views, models
