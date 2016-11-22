from db import session
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from models import User, FeatureRequest, ProductArea, Client

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
    'date_finished': fields.DateTime
}

parser_client = reqparse.RequestParser()
parser_client.add_argument('name', type=str)

parser_product_area = reqparse.RequestParser()
parser_product_area.add_argument('name', type=str)

parser_user = reqparse.RequestParser()
parser_user.add_argument('username', type=str)
parser_user.add_argument('email', type=str)
parser_user.add_argument('password', type=str)

parser_feature = reqparse.RequestParser()
parser_feature.add_argument('title', type=str)
parser_feature.add_argument('description', type=str)
parser_feature.add_argument('client_id', type=int)
parser_feature.add_argument('client_priority', type=int)
parser_feature.add_argument('product_area_id', type=int)
parser_feature.add_argument('user_id', type=int)
parser_feature.add_argument('ticket_url', type=str)


class ClientResource(Resource):
    @marshal_with(client_fields)
    def get(self, id):
        client = session.query(Client).get(id)
        if not client:
            abort(404, message="Client {} doesn't exist".format(id))
        return client

    def delete(self, id):
        client = session.query(Client).get(id)
        if not client:
            abort(404, message="Client {} doesn't exist".format(id))
        session.delete(client)
        session.commit()
        return {}, 204

    @marshal_with(client_fields)
    def put(self, id):
        parsed_args = parser_client.parse_args()
        client = session.query(Client).get(id)
        client.name = parsed_args['client_name']
        session.add(client)
        session.commit()
        return client, 201


class ClientListResource(Resource):
    @marshal_with(client_fields)
    def get(self):
        clients = session.query(Client).all()
        return clients

    @marshal_with(client_fields)
    def post(self):
        parsed_args = parser_client.parse_args()
        client = Client(name=parsed_args['client_name'])
        session.add(client)
        session.commit()
        return client, 201


class ProductAreaResource(Resource):
    @marshal_with(product_area_fields)
    def get(self, id):
        product_area = session.query(ProductArea).get(id)
        if not product_area:
            abort(404, message="Product Area {} doesn't exist".format(id))
        return product_area

    def delete(self, id):
        product_area = session.query(ProductArea).get(id)
        if not product_area:
            abort(404, message="Product Area {} doesn't exist".format(id))
        session.delete(product_area)
        session.commit()
        return {}, 204

    @marshal_with(product_area_fields)
    def put(self, id):
        parsed_args = parser_product_area.parse_args()
        product_area = session.query(ProductArea).get(id)
        product_area.name = parsed_args['product_area_name']
        session.add(product_area)
        session.commit()
        return product_area, 201


class ProductAreaListResource(Resource):
    @marshal_with(product_area_fields)
    def get(self):
        product_areas = session.query(ProductArea).all()
        return product_areas

    @marshal_with(product_area_fields)
    def post(self):
        parsed_args = parser_product_area.parse_args()
        product_area = ProductArea(name=parsed_args['product_area_name'])
        session.add(product_area)
        session.commit()
        return product_area, 201


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = session.query(User).get(id)
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        return user

    def delete(self, id):
        user = session.query(User).get(id)
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        session.delete(user)
        session.commit()
        return {}, 204

    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = parser_user.parse_args()
        user = session.query(User).get(id)
        user.username = parsed_args['username']
        user.email = parsed_args['email']
        user.password = parsed_args['password']
        session.add(user)
        session.commit()
        return user, 201


class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = session.query(User).all()
        return users

    @marshal_with(user_fields)
    def post(self):
        parsed_args = parser_user.parse_args()
        user = User(username=parsed_args['username'], email=parsed_args
                    ['email'], password=parsed_args['password'])
        session.add(user)
        session.commit()
        return user, 201


class FeatureRequestResource(Resource):
    @marshal_with(feature_request_fields)
    def get(self, id):
        feature_request = session.query(FeatureRequest).get(id)
        if not feature_request:
            abort(404, message="Feature request {} doesn't exist".format(id))
        return feature_request

    def delete(self, id):
        feature_request = session.query(FeatureRequest).get(id)
        if not feature_request:
            abort(404, message="Feature request {} doesn't exist".format(id))
        session.delete(feature_request)
        session.commit()
        return {}, 204


class FeatureRequestListResource(Resource):
    @marshal_with(feature_request_fields)
    def get(self):
        feature_requests = session.query(FeatureRequest).all()
        return feature_requests

    def checkPriorities(client_id, new_client_priority, new_title):
        # initializing priorities dictionary
        priorities_dict = {}
        # find all active feature requests (with date_finished = None)
        features_same_client = FeatureRequest.query.filter(FeatureRequest.client_id == client_id)\
            .filter(FeatureRequest.date_finished == None)
        # filling dictionary
        for feature_same_client in features_same_client:
            priorities_dict[str(feature_same_client.client_priority)] = feature_same_client.title
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
            feature_request = FeatureRequest.query.filter(FeatureRequest.title == old_title)\
                .filter(FeatureRequest.client_priority == new_client_priority)\
                .filter(FeatureRequest.client_id == client_id)\
                .one()

            feature_request.client_priority = int(old_key)
            session.add(feature_request)
            session.commit()