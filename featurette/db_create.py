#!venv/bin/python
from app import db, bcrypt
from app.models import User, Client, ProductArea, FeatureRequest
from app.db import create_db_tables

create_db_tables()

# Inserting data
username1 = User('username1', 'username1@foo.com',
                 bcrypt.generate_password_hash('12345678'))
username2 = User('username2', 'username2@foo.com',
                 bcrypt.generate_password_hash('12345678'))
username3 = User('username3', 'username3@foo.com',
                 bcrypt.generate_password_hash('12345678'))
username4 = User('username4', 'username4@foo.com',
                 bcrypt.generate_password_hash('12345678'))
username5 = User('username5', 'username5@foo.com',
                 bcrypt.generate_password_hash('12345678'))
user = User('username', 'username@foo.com',
            bcrypt.generate_password_hash('12345678'))
db.session.add(user)
db.session.add(username1)
db.session.add(username2)
db.session.add(username3)
db.session.add(username4)
db.session.add(username5)

clientA = Client('Client A')
clientB = Client('Client B')
clientC = Client('Client C')
clientD = Client('Client D')
db.session.add(clientA)
db.session.add(clientB)
db.session.add(clientC)
db.session.add(clientD)

policies = ProductArea('Policies')
claims = ProductArea('Claims')
billing = ProductArea('Billing')
reports = ProductArea('Reports')
db.session.add(policies)
db.session.add(claims)
db.session.add(billing)
db.session.add(reports)

feat_req = FeatureRequest('This is a title',
                          'This is not the description you are looking for',
                          1, 1, 1, 1, '2017-06-01', 'www.wired.com', None)
feat_req2 = FeatureRequest('This is another title', 'Another description',
                           1, 1, 1, 1, '2017-06-01', 'www.google.com', None)
db.session.add(feat_req)
db.session.add(feat_req2)

db.session.commit()
