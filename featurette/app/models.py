import datetime
from app import db
from sqlalchemy.sql import func, text


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(255))
    authenticated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=datetime.
                           now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.
                           current_timestamp(), server_default=text
                           ('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    feature_requests = db.relationship('FeatureRequest', cascade='delete')

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.
                           current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.
                           current_timestamp())
    feature_requests = db.relationship('FeatureRequest', cascade='delete, \
        delete-orphan')

    def __init__(self, name):
        self.name = name


class ProductArea(db.Model):
    __tablename__ = 'product_areas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.
                           current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.
                           current_timestamp())
    feature_requests = db.relationship('FeatureRequest', cascade='delete, \
        delete-orphan')

    def __init__(self, name):
        self.name = name


class FeatureRequest(db.Model):
    __tablename__ = 'feature_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client_priority = db.Column(db.Integer)
    product_area_id = db.Column(db.Integer, db.ForeignKey('product_areas.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_date = db.Column(db.DateTime(timezone=True))
    ticket_url = db.Column(db.String(100))
    date_finished = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.
                           current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.
                           current_timestamp())
    client = db.relationship('Client', foreign_keys=client_id)
    product_area = db.relationship('ProductArea', foreign_keys=product_area_id)
    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, title, description, client_id, client_priority,
                 product_area_id, user_id, target_date, ticket_url,
                 date_finished):
        self.title = title
        self.description = description
        self.client_id = client_id
        self.client_priority = client_priority
        self.product_area_id = product_area_id
        self.user_id = user_id
        self.target_date = target_date
        self.ticket_url = ticket_url
        self.date_finished = date_finished
