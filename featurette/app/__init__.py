from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://featurette:br1teCor3@localhost/featurette'

db = SQLAlchemy(app)

from app import views, models
