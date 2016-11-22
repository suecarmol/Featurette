import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from models import Base

try:
    host = os.environ['MYSQL_HOST']
except:
    host = '127.0.0.1'

try:
    mysql_user_pass = os.environ['MYSQL_USER_PASS']
except:
    mysql_user_pass = 'root'

DB_URI = 'mysql://{}@{}/featurette'.format(mysql_user_pass, host)

engine = create_engine(DB_URI)

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine)
session = scoped_session(Session)


def create_db_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
