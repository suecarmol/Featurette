import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

try:
    host = os.environ['MYSQL_HOST']
except:
    host = '127.0.0.1'

try:
    mysql_user_pass = os.environ['MYSQL_USER_PASS']
except:
    mysql_user_pass = 'root'

DB_URI = 'mysql://{}@{}/featurette'.format(mysql_user_pass, host)


Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI))
session = scoped_session(Session)
