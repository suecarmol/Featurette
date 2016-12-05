import sys
import os
import unittest
import requests

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from app.models import User, FeatureRequest # noqa
from app import app, bcrypt # noqa
from app.db import session # noqa
from app.db import create_db_tables # noqa


class FeatureRequestUnitTest(unittest.TestCase):

    def setUp(self):
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def test_restricted_feature_request_endpoints_without_auth(self):
        response_features = requests.get('http://127.0.0.1:5000/api/v1/featureRequests')
        response_add_features = requests.get('http://127.0.0.1:5000/api/v1/featureRequests')
        self.assertEqual(401, response_features.status_code)
        self.assertEqual(401, response_add_features.status_code)

    def test_restricted_feature_request_endpoints_with_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash
                    ('12345678'))
        session.add(user)
        session.commit()
        assert user in session
        response = requests.post('http://127.0.0.1:5000/api/v1/login', data={
                                 'email': user.email,
                                 'password': user.password})
        self.assertTrue(user.authenticated)
        self.assertEqual(200, response.status_code)
        # response_features = self.client.get('/')
        # response_add_features = self.client.get('/addFeature')
        # response_delete_features = self.client.get('/deleteFeature')
        # self.assert200(response_features)
        # self.assert200(response_add_features)
        # self.assert200(response_delete_features)

if __name__ == '__main__':
    unittest.main()
