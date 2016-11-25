from config import config
from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from api import ClientResource
from api import ClientListResource
from api import UserResource
from api import UserListResource
from api import ProductAreaResource
from api import ProductAreaListResource
from api import FeatureRequestResource
from api import FeatureRequestListResource

app = Flask(__name__)
app.config.from_object(config['dev'])
app.secret_key = 'br1teCor3'
bcrypt = Bcrypt(app)
api = Api(app, catch_all_404s=True)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
# db = SQLAlchemy(app)

api.add_resource(ClientListResource, '/api/v1/clients')
api.add_resource(ClientResource, '/api/v1/client/<id>')
api.add_resource(UserListResource, '/api/v1/users')
api.add_resource(UserResource, '/api/v1/user/<id>')
api.add_resource(ProductAreaListResource, '/api/v1/productAreas')
api.add_resource(ProductAreaResource, '/api/v1/productArea/<id>')
api.add_resource(FeatureRequestListResource, '/api/v1/featureRequests')
api.add_resource(FeatureRequestResource, '/api/v1/featureRequest/<id>')

from app import views, models
