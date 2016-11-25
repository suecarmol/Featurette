from config import config
from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(config['dev'])
app.secret_key = 'br1teCor3'
bcrypt = Bcrypt(app)
api = Api(app, catch_all_404s=True)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)

from services import ClientResource
from services import ClientListResource
from services import UserResource
from services import UserListResource
from services import ProductAreaResource
from services import ProductAreaListResource
from services import FeatureRequestResource
from services import FeatureRequestListResource
from services import LoginResource
from services import LogoutResource
# db = SQLAlchemy(app)

api.add_resource(LoginResource, '/api/v1/login')
api.add_resource(LogoutResource, '/api/v1/logout')
api.add_resource(ClientListResource, '/api/v1/clients')
api.add_resource(ClientResource, '/api/v1/client/<id>')
api.add_resource(UserListResource, '/api/v1/users')
api.add_resource(UserResource, '/api/v1/user/<id>')
api.add_resource(ProductAreaListResource, '/api/v1/productAreas')
api.add_resource(ProductAreaResource, '/api/v1/productArea/<id>')
api.add_resource(FeatureRequestListResource, '/api/v1/featureRequests')
api.add_resource(FeatureRequestResource, '/api/v1/featureRequest/<id>')
# api.add_resource(FeatureRequestResource, '/api/v1/featureRequest/<id>/finishFeature')
