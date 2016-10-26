from app import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self):
        self.username = username
        self.email = email
        self.password = password

class Client(db.Model):
    __tablename__='clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self):
        self.name = name

class ProductArea(db.Model):
    __tablename__='product_areas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self):
        self.name = name

class FeatureRequest(db.Model):
    __tablename__='feature_requests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'))
    client_priority = db.Column(db.Integer)
    product_area_id = db.Column(db.Integer, db.ForeignKey('ProductArea.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    date_finished = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    client = db.relationship('Client', foreign_keys=client_id)
    product_area_id = db.relationship('ProductArea', foreign_keys=product_area_id)
    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self):
        self.title = title
        self.description = description
        self.client_id = client_id
        self.client_priority = client_priority
        self.product_area_id = product_area_id
        self.user_id = user_id
        self.date_finished = null
