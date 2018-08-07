from datetime import datetime
from app import bcrypt, login_manager
from db import session
from config import Config
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_login import current_user, login_user, logout_user, login_required
from models import User, FeatureRequest, ProductArea, Client, login_serializer


client_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

product_area_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
    'authenticated': fields.Boolean,
    'token': fields.String
}

feature_request_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'client_id': fields.Integer,
    'client_priority': fields.Integer,
    'product_area_id': fields.Integer,
    'user_id': fields.Integer,
    'target_date': fields.DateTime,
    'ticket_url': fields.String,
    'date_finished': fields.DateTime,
    'is_finished': fields.Boolean
}

feature_request_fields_user_friendly = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'client_id': fields.Integer,
    'client_name': fields.String,
    'client_priority': fields.Integer,
    'product_area_id': fields.Integer,
    'product_area_name': fields.String,
    'user_id': fields.Integer,
    'username': fields.String,
    'target_date': fields.DateTime,
    'ticket_url': fields.String,
    'date_finished': fields.DateTime,
    'is_finished': fields.Boolean
}

parser_login = reqparse.RequestParser()
parser_login.add_argument('email', type=str, required=True)
parser_login.add_argument('password', type=str, required=True)

parser_client = reqparse.RequestParser()
parser_client.add_argument('client_name', type=str, required=True)

parser_product_area = reqparse.RequestParser()
parser_product_area.add_argument('product_area_name', type=str, required=True)

parser_user = reqparse.RequestParser()
parser_user.add_argument('username', type=str, required=True)
parser_user.add_argument('email', type=str, required=True)
parser_user.add_argument('password', type=str, required=True)

parser_feature = reqparse.RequestParser()
parser_feature.add_argument('title', type=str, required=True)
parser_feature.add_argument('description', type=str, required=True)
parser_feature.add_argument('client_id', type=int, required=True)
parser_feature.add_argument('client_priority', type=int, required=True)
parser_feature.add_argument('product_area_id', type=int, required=True)
parser_feature.add_argument('target_date', required=True)
parser_feature.add_argument('ticket_url', type=str, required=True)


@login_manager.user_loader
def user_loader(user_id):
    try:
        return session.query(User).get(user_id)
    except:
        session.rollback()
        print("Could not get user")
        return {}, 500


@login_manager.token_loader
def load_token(token):
    max_age = Config.REMEMBER_COOKIE_DURATION.total_seconds()

    # Decrypt the Security Token, data = [username, hashpass]
    data = login_serializer.loads(token, max_age=max_age)

    # Find the User
    try:
        user = session.query(User).get(data[0])
    except:
        session.rollback()
        print("Could not get user")
        return {}, 500

    # Check Password and return user or None
    if user and data[1] == user.password:
        return user
    return None


class LoginResource(Resource):
    @marshal_with(user_fields)
    def post(self):
        parsed_args = parser_login.parse_args()
        email = parsed_args['email']
        password = parsed_args['password']
        try:
            user = session.query(User).filter_by(email=email).first()
        except:
            session.rollback()
            print("User Login query not found")
            return {}, 500
        if not user:
            abort(404, message="User {} doesn't exist".format(email))
        if bcrypt.check_password_hash(user.password, password):
            user.authenticated = True
            try:
                session.commit()
            except:
                session.rollback()
            print('User successfully logged in')
            login_user(user, remember=True)
            return {}, 200


class LogoutResource(Resource):
    @login_required
    @marshal_with(user_fields)
    def post(self):
        user = current_user
        user.authenticated = False
        try:
            session.commit()
        except:
            session.rollback()
        logout_user()
        return {}, 204


class ClientResource(Resource):
    @login_required
    @marshal_with(client_fields)
    def get(self, id):
        try:
            client = session.query(Client).get(id)
        except:
            session.rollback()
            print("Client in GET not found")
            return {}, 500
        if not client:
            abort(404, message="Client {} doesn't exist".format(id))
        return client

    @login_required
    def delete(self, id):
        try:
            client = session.query(Client).get(id)
        except:
            session.rollback()
            print("Client in DELETE not found")
            return {}, 500
        if not client:
            abort(404, message="Client {} doesn't exist".format(id))
        try:
            session.delete(client)
            session.commit()
        except:
            session.rollback()
        return {}, 204

    @login_required
    @marshal_with(client_fields)
    def put(self, id):
        parsed_args = parser_client.parse_args()

        try:
            client = session.query(Client).get(id)
        except:
            session.rollback()
            print("Error in PUT client")
            return {}, 500

        client_name = parsed_args['client_name']
        if not client_name:
            return 418
        else:
            client.name = parsed_args['client_name']
            try:
                session.add(client)
                session.commit()
            except:
                session.rollback()
            return client, 201


class ClientListResource(Resource):
    @login_required
    @marshal_with(client_fields)
    def get(self):
        try:
            clients = session.query(Client).all()
        except:
            session.rollback()
            print("Error in GET all clients")
            return {}, 500
        return clients

    @login_required
    @marshal_with(client_fields)
    def post(self):
        parsed_args = parser_client.parse_args()
        client_name = parsed_args['client_name']
        if not client_name:
            return 418
        else:
            client = Client(name=client_name)
            try:
                session.add(client)
                session.commit()
            except:
                session.rollback()
        return client, 201


class ProductAreaResource(Resource):
    @login_required
    @marshal_with(product_area_fields)
    def get(self, id):
        try:
            product_area = session.query(ProductArea).get(id)
        except:
            session.rollback()
            print("Error in GET product Area")
            return {}, 500
        if not product_area:
            abort(404, message="Product Area {} doesn't exist".format(id))
        return product_area

    @login_required
    def delete(self, id):
        try:
            product_area = session.query(ProductArea).get(id)
        except:
            session.rollback()
            print("Error in DELETE product area, product area not found")
            return {}, 500
        if not product_area:
            abort(404, message="Product Area {} doesn't exist".format(id))
        try:
            session.delete(product_area)
            session.commit()
        except:
            session.rollback()
        return {}, 204

    @login_required
    @marshal_with(product_area_fields)
    def put(self, id):
        parsed_args = parser_product_area.parse_args()
        try:
            product_area = session.query(ProductArea).get(id)
        except:
            session.rollback()
            print("Product area PUT failed, no product area found")
            return {}, 500
        product_area_name = parsed_args['product_area_name']
        if not product_area_name:
            return 418
        else:
            product_area.name = product_area_name
            try:
                session.add(product_area)
                session.commit()
            except:
                session.rollback()
            return product_area, 201


class ProductAreaListResource(Resource):
    @login_required
    @marshal_with(product_area_fields)
    def get(self):
        try:
            product_areas = session.query(ProductArea).all()
        except:
            session.rollback()
            print("Product Areas not found")
            return {}, 500
        return product_areas

    @login_required
    @marshal_with(product_area_fields)
    def post(self):
        parsed_args = parser_product_area.parse_args()
        product_area_name = parsed_args['product_area_name']
        if not product_area_name:
            return 418
        else:
            product_area = ProductArea(name=product_area_name)
            try:
                session.add(product_area)
                session.commit()
            except:
                session.rollback()
            return product_area, 201


class UserResource(Resource):
    @login_required
    @marshal_with(user_fields)
    def get(self, id):
        try:
            user = session.query(User).get(id)
        except:
            session.rollback()
            print("Error in GET user")
            return {}, 500
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        return user

    @login_required
    def delete(self, id):
        try:
            user = session.query(User).get(id)
        except:
            session.rollback()
            print("Error in DELETE user")
            return {}, 500
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        # current_user is not enabled during unit tests
        if current_user.is_authenticated:
            if user.id == current_user.id:
                abort(403, message="You cannot delete yourself")
        try:
            session.delete(user)
            session.commit()
        except:
            session.rollback()
        return {}, 204

    @login_required
    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = parser_user.parse_args()
        try:
            user = session.query(User).get(id)
        except:
            session.rollback()
            print("Error in PUT user")
            return {}, 500
        username = parsed_args['username']
        email = parsed_args['email']
        password = bcrypt.generate_password_hash(parsed_args['password'])
        if not username or not email or not password:
            return 418
        else:
            user.username = username
            user.email = email
            user.password = password
            try:
                session.add(user)
                session.commit()
            except:
                session.rollback()
            return user, 201


class UserListResource(Resource):
    @login_required
    @marshal_with(user_fields)
    def get(self):
        try:
            users = session.query(User).all()
        except:
            session.rollback()
            print("Could not GET all users")
            return {}, 500
        return users

    @login_required
    @marshal_with(user_fields)
    def post(self):
        parsed_args = parser_user.parse_args()
        username = parsed_args['username']
        email = parsed_args['email']
        password = bcrypt.generate_password_hash(parsed_args['password'])
        if not username or not email or not password:
            return 418
        else:
            user = User(username=username, email=email, password=password)
            try:
                session.add(user)
                session.commit()
            except:
                session.rollback()
            return user, 201


class FeatureRequestResource(Resource):
    @login_required
    @marshal_with(feature_request_fields_user_friendly)
    def get(self, id):
        try:
            feature_request = session.query(FeatureRequest).get(id)
        except:
            session.rollback()
            print("Error in GET feature request")
            return {}, 500
        if not feature_request:
            abort(404, message="Feature request {} doesn't exist".format(id))
        feature_request_user_friendly = {}
        feature_request_user_friendly['id'] = int(feature_request.id)
        feature_request_user_friendly['title'] = str(feature_request.title)
        feature_request_user_friendly['description'] = str(feature_request.description)
        feature_request_user_friendly['client_id'] = feature_request.client_id
        feature_request_user_friendly['client_name'] = str(feature_request.client.name)
        feature_request_user_friendly['client_priority'] = str(feature_request.client_priority)
        feature_request_user_friendly['product_area_id'] = feature_request.product_area_id
        feature_request_user_friendly['product_area_name'] = str(feature_request.product_area.name)
        feature_request_user_friendly['user_id'] = feature_request.user_id
        feature_request_user_friendly['username'] = str(feature_request.user.username)
        feature_request_user_friendly['target_date'] = feature_request.target_date
        feature_request_user_friendly['ticket_url'] = str(feature_request.ticket_url)
        feature_request_user_friendly['date_finished'] = feature_request.date_finished
        feature_request_user_friendly['is_finished'] = feature_request.is_finished

        return feature_request_user_friendly

    @login_required
    def delete(self, id):
        try:
            feature_request = session.query(FeatureRequest).get(id)
        except:
            session.rollback()
            print("Error in DELETE feature request")
            return {}, 500
        if not feature_request:
            abort(404, message="Feature request {} doesn't exist".format(id))
        try:
            session.delete(feature_request)
            session.commit()
        except:
            session.rollback()
        return {}, 204

    @login_required
    @marshal_with(feature_request_fields)
    def put(self, id):
        parsed_args = parser_feature.parse_args()
        title = parsed_args['title']
        client_id = parsed_args['client_id']
        client_priority = parsed_args['client_priority']
        conv_target_date = datetime.strptime(parsed_args['target_date'],
                                             "%Y-%m-%d %H:%M")
        try:
            feature_request = session.query(FeatureRequest).get(id)
        except:
            session.rollback()
            print("Error in PUT feature request")
            return {}, 500
        feature_request.title = title
        feature_request.description = parsed_args['description']
        feature_request.client_id = client_id
        feature_request.client_priority = client_priority
        feature_request.product_area_id = parsed_args['product_area_id']
        # current_user is not enabled during unit tests
        if current_user.is_authenticated:
            feature_request.user_id = current_user.id
        else:
            feature_request.user_id = 1
        feature_request.target_date = conv_target_date
        feature_request.ticket_url = parsed_args['ticket_url']
        feature_request.date_finished = None
        # priority algorithm
        self.checkPriorities(client_id, client_priority, title)
        try:
            session.add(feature_request)
            session.commit()
        except:
            session.rollback()
        return feature_request, 201

    def checkPriorities(self, client_id, new_client_priority, new_title):
        # initializing priorities dictionary
        priorities_dict = {}
        # find all active feature requests (with date_finished = None)
        try:
            features_same_client = session.query(FeatureRequest).filter(FeatureRequest.client_id == client_id).filter(FeatureRequest.date_finished == None) # noqa
        except:
            session.rollback()
            print("Error in check priorities feature request")
        # filling dictionary
        for feature_same_client in features_same_client:
            priorities_dict[str(feature_same_client.client_priority)] = feature_same_client.title # noqa
        # checking if priority number exists
        if str(new_client_priority) in priorities_dict:
            # get data of existing priority (removing the key)
            old_key = new_client_priority
            old_title = priorities_dict[str(old_key)]
            # while key exists continue incrementing by 1
            while str(old_key) in priorities_dict:
                aux = int(old_key)
                aux = aux + 1
                old_key = str(aux)
            del priorities_dict[str(new_client_priority)]
            # add new priority and title
            priorities_dict[str(new_client_priority)] = new_title
            # add old priority and title
            priorities_dict[str(old_key)] = old_title
            # get old Feature Request that matches the parameters
            try:
                feature_request = session.query(FeatureRequest).filter(FeatureRequest.title == old_title).filter(FeatureRequest.client_priority == new_client_priority).filter(FeatureRequest.client_id == client_id).first() # noqa
            except:
                session.rollback()
                print("Error in second query of check priorities")


class FinishFeatureResource(Resource):
    @login_required
    @marshal_with(feature_request_fields)
    def post(self, id):
        try:
            feature_request = session.query(FeatureRequest).get(id)
        except:
            session.rollback()
            print("Error in finish feature request")
            return {}, 500
        if not feature_request:
            abort(404, message="Feature request {} doesn't exist".format(id))
        feature_request.date_finished = str(datetime.now())
        feature_request.client_priority = 0
        feature_request.is_finished = True
        try:
            session.commit()
        except:
            session.rollback()


class FeatureRequestListResource(Resource):
    @login_required
    @marshal_with(feature_request_fields_user_friendly)
    def get(self):
        try:
            feature_requests = session.query(FeatureRequest).all()
        except:
            session.rollback()
            print("Error in GET all feature requests")
            return {}, 500
        format_feature_requests = []
        for feature_request in feature_requests:
            tmp_feature_request = {}
            tmp_feature_request['id'] = int(feature_request.id)
            tmp_feature_request['title'] = str(feature_request.title)
            tmp_feature_request['description'] = str(feature_request.description)
            tmp_feature_request['client_id'] = feature_request.client_id
            tmp_feature_request['client_name'] = str(feature_request.client.name)
            tmp_feature_request['client_priority'] = str(feature_request.client_priority)
            tmp_feature_request['product_area_id'] = feature_request.product_area_id
            tmp_feature_request['product_area_name'] = str(feature_request.product_area.name)
            tmp_feature_request['user_id'] = feature_request.user_id
            tmp_feature_request['username'] = str(feature_request.user.username)
            tmp_feature_request['target_date'] = feature_request.target_date
            tmp_feature_request['ticket_url'] = str(feature_request.ticket_url)
            tmp_feature_request['date_finished'] = feature_request.date_finished
            tmp_feature_request['is_finished'] = feature_request.is_finished
            format_feature_requests.append(tmp_feature_request)

        # print(format_feature_requests)

        return format_feature_requests

    @login_required
    @marshal_with(feature_request_fields)
    def post(self):
        parsed_args = parser_feature.parse_args()
        # checking if priority exists
        title = parsed_args['title']
        client_id = parsed_args['client_id']
        client_priority = parsed_args['client_priority']
        conv_target_date = datetime.strptime(parsed_args['target_date'],
                                             "%Y-%m-%d %H:%M")
        # current_user is not enabled during unit tests
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            user_id = 1
        # priority algorithm
        self.checkPriorities(client_id, client_priority, title)
        feature_request = FeatureRequest(title=title,
                                         description=parsed_args['description'], # noqa
                                         client_id=client_id,
                                         client_priority=client_priority,
                                         product_area_id=parsed_args['product_area_id'], # noqa
                                         user_id=user_id,
                                         target_date=conv_target_date,
                                         ticket_url=parsed_args['ticket_url'],
                                         date_finished=None,
                                         is_finished=False)

        try:
            session.add(feature_request)
            session.commit()
            print("Session committed")
        except:
            session.rollback()
            print("Session rolled back")
        return feature_request, 201

    def checkPriorities(self, client_id, new_client_priority, new_title):
        # initializing priorities dictionary
        priorities_dict = {}
        # find all active feature requests (with date_finished = None)
        try:
            features_same_client = session.query(FeatureRequest).filter(FeatureRequest.client_id == client_id).filter(FeatureRequest.date_finished == None) # noqa
        except:
            session.rollback()
            print("Error in check priorities pt 2 - 1")
        # filling dictionary
        for feature_same_client in features_same_client:
            priorities_dict[str(feature_same_client.client_priority)] = feature_same_client.title # noqa
        # checking if priority number exists
        if str(new_client_priority) in priorities_dict:
            # get data of existing priority (removing the key)
            old_key = new_client_priority
            old_title = priorities_dict[str(old_key)]
            # while key exists continue incrementing by 1
            while str(old_key) in priorities_dict:
                aux = int(old_key)
                aux = aux + 1
                old_key = str(aux)
            del priorities_dict[str(new_client_priority)]
            # add new priority and title
            priorities_dict[str(new_client_priority)] = new_title
            # add old priority and title
            priorities_dict[str(old_key)] = old_title
            # get old Feature Request that matches the parameters
            try:
                feature_request = session.query(FeatureRequest).filter(FeatureRequest.title == old_title).filter(FeatureRequest.client_priority == new_client_priority).filter(FeatureRequest.client_id == client_id).first() # noqa
            except:
                session.rollback()
                print("Error in check prioritues pt 2 - 2")

            feature_request.client_priority = int(old_key)
            try:
                session.add(feature_request)
                session.commit()
            except:
                session.rollback()
