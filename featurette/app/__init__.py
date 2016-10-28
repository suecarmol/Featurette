from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://featurette:br1teCor3@localhost/featurette'
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

from app import views, models
