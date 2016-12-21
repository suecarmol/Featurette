import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

try:
    host = os.environ['MYSQL_HOST']
except:
    host = '127.0.0.1'

try:
    mysql_user_pass = os.environ['MYSQL_USER_PASS']
except:
    mysql_user_pass = 'root'


DB_URI = 'mysql://{}@{}/featurette'.format(mysql_user_pass, host)


class Auth:
    CLIENT_ID = ('1062419317374-re383eti1ebo6745h4nm3fq7in73aq65'
                 '.apps.googleusercontent.com')
    CLIENT_SECRET = '8IfhLwb8et7znsGsVKn0fPWm'
    REDIRECT_URI = 'https://localhost:5000/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'


class Config:
    APP_NAME = "Featurette"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "br1teCor3"
    REMEMBER_COOKIE_DURATION = timedelta(days=14)


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DB_URI
    TESTING = True
    LOGIN_DISABLED = False


class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DB_URI
    TESTING = False
    LOGIN_DISABLED = False


class TestConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DB_URI
    TESTING = True
    LOGIN_DISABLED = True

config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig,
    "test": TestConfig
}
