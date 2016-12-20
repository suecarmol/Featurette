from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from itsdangerous import URLSafeTimedSerializer
from flask_login import UserMixin
from config import Config
Base = declarative_base()
login_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    email = Column(String(120), index=True, unique=True)
    password = Column(String(255))
    authenticated = Column(Boolean, default=False)
    tokens = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.now(),
                        server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(),
                        server_default=text('NOW()'))
    feature_requests = relationship('FeatureRequest', cascade='delete')

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

    def get_auth_token(self):
        """
        Encode a secure token for cookie
        """
        data = [str(self.id), self.password]
        return login_serializer.dumps(data)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.now(),
                        server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(),
                        server_default=text('NOW()'))
    feature_requests = relationship('FeatureRequest', cascade='delete, \
        delete-orphan')

    def __init__(self, name):
        self.name = name


class ProductArea(Base):
    __tablename__ = 'product_areas'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.now(),
                        server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(),
                        server_default=text('NOW()'))
    feature_requests = relationship('FeatureRequest', cascade='delete, \
        delete-orphan')

    def __init__(self, name):
        self.name = name


class FeatureRequest(Base):
    __tablename__ = 'feature_requests'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(255))
    client_id = Column(Integer, ForeignKey('clients.id'))
    client_priority = Column(Integer)
    product_area_id = Column(Integer, ForeignKey('product_areas.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    target_date = Column(DateTime(timezone=True))
    ticket_url = Column(String(100))
    date_finished = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.now(),
                        server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(),
                        server_default=text('NOW()'))
    client = relationship('Client', foreign_keys=client_id)
    product_area = relationship('ProductArea', foreign_keys=product_area_id)
    user = relationship('User', foreign_keys=user_id)

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
