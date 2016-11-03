#!venv/bin/python
import os.path

from app import db, bcrypt
from models import User

db.create_all()

# Inserting data
username1 = User('username1', 'username1@foo.com', bcrypt.generate_password_hash('12345678'))
username2 = User('username2', 'username2@foo.com', bcrypt.generate_password_hash('12345678'))
username3 = User('username3', 'username3@foo.com', bcrypt.generate_password_hash('12345678'))
username4 = User('username4', 'username4@foo.com', bcrypt.generate_password_hash('12345678'))
username5 = User('username5', 'username5@foo.com', bcrypt.generate_password_hash('12345678'))
db.session.add(username1)
db.session.add(username2)
db.session.add(username3)
db.session.add(username4)
db.session.add(username5)
db.session.commit()
